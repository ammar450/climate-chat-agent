"""
FastAPI application for climate chat agent.
Enhanced with caching, rate limiting, and security controls.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import os
import requests

from src.llm.llm_client import test_connection as test_llm
from src.query.sparql_client import run_sparql, test_endpoint, SPARQLSecurityError
from src.query.query_templates import render_template
from src.agent.state import session_store
from src.parsers.property_resolver import property_resolver
from src.agent.graph_agent import run_agent

app = FastAPI(
    title="Climate Chat Agent",
    description="Secure ChatGPT-like interface for querying climate observations",
    version="2.0.0"
)

# Add CORS middleware (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache for common queries
_query_cache = {}
_cache_lock = threading.Lock()
CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", "15"))

# Rate limiting
_rate_limit_data = defaultdict(list)  # session_id -> [timestamps]
_rate_limit_lock = threading.Lock()
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "30"))


def check_rate_limit(session_id: str) -> bool:
    """
    Check if session has exceeded rate limit.
    
    Args:
        session_id: Session identifier
        
    Returns:
        True if within limit, False if exceeded
    """
    with _rate_limit_lock:
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        # Remove old timestamps
        _rate_limit_data[session_id] = [
            ts for ts in _rate_limit_data[session_id]
            if ts > one_minute_ago
        ]
        
        # Check count
        if len(_rate_limit_data[session_id]) >= MAX_REQUESTS_PER_MINUTE:
            return False
        
        # Add current timestamp
        _rate_limit_data[session_id].append(now)
        return True


def get_cached_query(cache_key: str) -> Optional[Dict]:
    """Get cached query result if not expired."""
    with _cache_lock:
        if cache_key in _query_cache:
            result, timestamp = _query_cache[cache_key]
            age_minutes = (datetime.now() - timestamp).total_seconds() / 60
            if age_minutes < CACHE_TTL_MINUTES:
                print(f"[CACHE HIT] {cache_key}")
                return result
            else:
                # Expired, remove it
                del _query_cache[cache_key]
    return None


def cache_query(cache_key: str, result: Dict):
    """Cache query result with timestamp."""
    with _cache_lock:
        _query_cache[cache_key] = (result, datetime.now())
        print(f"[CACHE SET] {cache_key}")


# Prefetch and cache common queries at startup
@app.on_event("startup")
async def startup_event():
    """Initialize caches and prefetch common data."""
    print("[STARTUP] Initializing Climate Chat Agent...")
    print(f"[CONFIG] SPARQL Endpoint: {os.getenv('SPARQL_ENDPOINT', 'default')}")
    print(f"[CONFIG] Graph IRI: {os.getenv('GRAPH_IRI', 'default')}")
    print(f"[CONFIG] Cache TTL: {CACHE_TTL_MINUTES} minutes")
    print(f"[CONFIG] Rate Limit: {MAX_REQUESTS_PER_MINUTE} requests/minute")
    
    # Prefetch properties
    property_resolver.prefetch_properties()
    
    # Pre-cache common queries
    try:
        # Cache list_properties
        from src.query.query_templates import TEMPLATES
        if "list_properties" in TEMPLATES:
            query = render_template("list_properties", {})
            result = run_sparql(query)
            cache_query("template:list_properties", result)
        
        # Cache list_features
        if "list_features" in TEMPLATES:
            query = render_template("list_features", {})
            result = run_sparql(query)
            cache_query("template:list_features", result)
        
        print("[STARTUP] Common queries cached successfully")
    except Exception as e:
        print(f"[STARTUP WARNING] Could not pre-cache queries: {e}")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    history: Optional[List[Message]] = []
    model: Optional[str] = None  # User-selected model


class ChatResponse(BaseModel):
    answer: str
    technical_details: Optional[str] = None  # Technical response with debug info
    context: Optional[str] = None
    sparql: str
    rows: List[Dict]
    used_template: str


@app.get("/")
def read_root():
    """Serve the chat UI."""
    return FileResponse("static/index.html")


@app.get("/models")
def get_available_models():
    """Return list of available LLM models - dynamically fetched from Ollama."""
    models = []
    
    # Fetch available Ollama models dynamically
    try:
        import requests
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        response = requests.get(f"{ollama_url.replace('/api/chat', '')}/api/tags", timeout=2)
        if response.status_code == 200:
            ollama_data = response.json()
            for model in ollama_data.get("models", []):
                model_name = model.get("name", "").replace(":latest", "")
                # Extract base name (e.g., "llama3.2" from "llama3.2:latest")
                base_name = model_name.split(":")[0]
                display_name = base_name.replace(".", " ").title()
                models.append({
                    "id": f"ollama:{base_name}",
                    "name": f"{display_name} (Local)",
                    "provider": "ollama"
                })
    except Exception as e:
        print(f"[WARNING] Could not fetch Ollama models: {e}")
        # Fallback to default model
        models.append({
            "id": "ollama:llama3.2",
            "name": "Llama 3.2 (Local - Default)",
            "provider": "ollama"
        })
    
    # OpenAI models (if API key is configured)
    if os.getenv("OPENAI_API_KEY"):
        models.append({
            "id": "openai:gpt-4o-mini",
            "name": "GPT-4o Mini (OpenAI) ⭐",
            "provider": "openai"
        })
        models.append({
            "id": "openai:gpt-4o",
            "name": "GPT-4o (OpenAI)",
            "provider": "openai"
        })
        models.append({
            "id": "openai:gpt-4-turbo",
            "name": "GPT-4 Turbo (OpenAI)",
            "provider": "openai"
        })
        models.append({
            "id": "openai:gpt-4",
            "name": "GPT-4 (OpenAI)",
            "provider": "openai"
        })
        models.append({
            "id": "openai:gpt-3.5-turbo",
            "name": "GPT-3.5 Turbo (OpenAI)",
            "provider": "openai"
        })
    
    # If no models found, add default
    if not models:
        models.append({
            "id": "ollama:llama3.2",
            "name": "Llama 3.2 (Default)",
            "provider": "ollama"
        })
    
    # Determine the default model based on current configuration
    backend = os.getenv('LLM_BACKEND', 'openai').lower()
    if backend == 'openai':
        default_model = f"openai:{os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}"
    else:
        default_model = f"ollama:{os.getenv('OLLAMA_MODEL', 'llama3.2')}"
    
    return {"models": models, "default": default_model}


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Verifies LLM provider and SPARQL endpoint are reachable.
    """
    from llm_provider import llm, LLM_BACKEND
    
    health_status = {
        "status": "healthy",
        "llm_backend": LLM_BACKEND,
        "llm": "unknown",
        "sparql": "unknown"
    }
    
    # Check LLM
    try:
        if llm is None:
            health_status["llm"] = "not_initialized"
            health_status["status"] = "degraded"
        else:
            # Quick test - just check if LLM is initialized
            health_status["llm"] = "ok"
            health_status["llm_type"] = type(llm).__name__
    except Exception as e:
        health_status["llm"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check SPARQL endpoint
    try:
        if test_endpoint():
            health_status["sparql"] = "ok"
        else:
            health_status["sparql"] = "unreachable"
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["sparql"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    if health_status["status"] == "degraded":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat endpoint with rate limiting and security controls.
    Now powered by LangGraph for stateful conversation management.
    
    Frontend ONLY calls this endpoint - never calls SPARQL directly.
    
    Args:
        request: ChatRequest with message, session_id, and optional history
        
    Returns:
        ChatResponse with answer, context, SPARQL query, results, and template used
        
    Raises:
        HTTPException: On rate limit, security violation, or processing error
    """
    # Rate limiting
    if not check_rate_limit(request.session_id):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {MAX_REQUESTS_PER_MINUTE} requests per minute."
        )
    
    try:
        # Convert history to simple list of dicts if needed
        history = []
        if request.history:
            history = [{"role": msg.role, "content": msg.content} for msg in request.history]
        
        # Use model from request, or default to environment config
        model = request.model
        if not model:
            provider = os.getenv("LLM_PROVIDER", "ollama")
            model_name = os.getenv("OLLAMA_MODEL" if provider == "ollama" else "SAIA_MODEL", "llama3.2")
            model = f"{provider}:{model_name}"
        
        print(f"\n[CHAT] Session: {request.session_id}")
        print(f"[CHAT] Message: {request.message}")
        print(f"[CHAT] Model: {model}")
        print(f"[CHAT] History length: {len(history)}")
        
        # Run LangGraph agent
        result = run_agent(
            session_id=request.session_id,
            user_message=request.message,
            history=history,
            model=model
        )
        
        print(f"[CHAT] Success! Answer length: {len(result.get('answer', ''))}")
        
        # Return response
        return ChatResponse(
            answer=result.get("answer", "Sorry, I couldn't generate a response."),
            technical_details=result.get("technical_details"),  # Include technical details
            context=result.get("evidence"),  # Evidence text for context
            sparql=result.get("sparql", ""),
            rows=result.get("rows", [])[:20],  # Limit to 20 rows
            used_template=result.get("used_template", "unknown")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Chat processing failed: {str(e)}"
        print(f"\n{'='*60}")
        print(f"[ERROR] {error_detail}")
        print(f"{'='*60}")
        print(traceback.format_exc())
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=error_detail)


@app.post("/reset")
def reset_session(request: dict):
    """
    Reset a session's conversation context.
    
    Args:
        request: Dict with session_id
        
    Returns:
        Success message
    """
    session_id = request.get("session_id", "default")
    session_store.reset(session_id)
    return {"status": "success", "message": f"Session {session_id} has been reset"}


@app.get("/")
def read_root():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

