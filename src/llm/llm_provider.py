"""
LLM Provider abstraction layer.
Returns appropriate LLM instance based on LLM_BACKEND environment variable.
Supports: local llama (via Ollama) and SAIA (OpenAI-compatible).
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
LLM_BACKEND = os.getenv("LLM_BACKEND", "openai")  # openai | ollama
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Export for health checks
__all__ = ["get_llm", "llm", "chat", "LLM_BACKEND"]


def get_llm():
    """
    Get the configured LLM instance based on LLM_BACKEND environment variable.
    
    Returns:
        LLM instance (either Ollama ChatOllama or OpenAI ChatOpenAI)
        
    Raises:
        ValueError: If LLM_BACKEND is invalid or required configuration is missing
    """
    backend = LLM_BACKEND.lower()
    
    if backend == "openai":
        return _get_openai_llm()
    elif backend == "ollama":
        return _get_ollama_llm()
    else:
        raise ValueError(
            f"Invalid LLM_BACKEND: {backend}. Must be 'openai' or 'ollama'."
        )


def _get_openai_llm():
    """Get OpenAI LLM instance."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI backend. "
            "Please set it in your .env file."
        )
    
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        raise ImportError(
            "langchain-openai required for OpenAI. "
            "Install: pip install langchain-openai"
        )
    
    model = OPENAI_MODEL
    
    print(f"[LLM PROVIDER] Backend: OpenAI")
    print(f"[LLM PROVIDER] Model: {model}")
    print(f"[LLM PROVIDER] API Key: {'*' * 20}...{OPENAI_API_KEY[-4:] if len(OPENAI_API_KEY) > 4 else '****'}")
    
    llm = ChatOpenAI(
        model=model,
        api_key=OPENAI_API_KEY,
        temperature=0.1,
        max_tokens=1000,
    )
    
    return llm


def _get_ollama_llm():
    """Get local Ollama LLM instance."""
    try:
        from langchain_community.chat_models import ChatOllama
    except ImportError:
        raise ImportError(
            "langchain-community required for Ollama. "
            "Install: pip install langchain-community"
        )
    
    model = OLLAMA_MODEL
    base_url = OLLAMA_URL
    
    print(f"[LLM PROVIDER] Backend: Ollama")
    print(f"[LLM PROVIDER] Model: {model}")
    print(f"[LLM PROVIDER] Base URL: {base_url}")
    
    llm = ChatOllama(
        model=model,
        base_url=base_url,
        temperature=0.1,
        num_predict=1000,
    )
    
    return llm


# Initialize LLM at module load
try:
    llm = get_llm()
    print("[LLM PROVIDER] Successfully initialized LLM")
except Exception as e:
    print(f"[LLM PROVIDER ERROR] Failed to initialize LLM: {e}")
    llm = None


def chat(messages, provider=None, model=None, temperature=None, max_tokens=None):
    """
    Wrapper function for compatibility with existing code.
    Uses the LangChain LLM instance to generate responses.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        provider: Ignored (uses LLM_BACKEND from env)
        model: Ignored (uses configured model from env)
        temperature: Optional temperature override
        max_tokens: Optional max tokens override
        
    Returns:
        String response from LLM
    """
    if llm is None:
        raise ValueError("LLM not initialized. Check LLM_BACKEND configuration.")
    
    # Convert messages to LangChain format
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    
    lc_messages = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        
        if role == "system":
            lc_messages.append(SystemMessage(content=content))
        elif role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))
    
    # Invoke LLM
    try:
        response = llm.invoke(lc_messages)
        return response.content
    except Exception as e:
        print(f"[LLM PROVIDER ERROR] Failed to invoke LLM: {e}")
        raise
