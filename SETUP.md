# Setup Guide

Complete installation and configuration guide for the Climate Chat Agent.

## Prerequisites

- Python 3.8+
- **Either:**
  - [Ollama](https://ollama.com/download) installed locally, OR
  - OpenAI API key

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env to set LLM provider and credentials
```

⚠️ **Security**: Never commit `.env` file! It contains your API keys.

### 3. Choose Your LLM Provider

#### Option A: OpenAI (Recommended - Default)

```bash
# Set in .env:
LLM_BACKEND=openai
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

⚠️ **API Key Security**:
- Never commit `.env` to git (already in `.gitignore`)
- Use `.env.example` for templates
- Rotate keys immediately if exposed
- GitHub will block pushes with exposed keys

#### Option B: Ollama (Local LLM)

```bash
# Pull model
ollama pull llama3.2

# Start Ollama if not running
ollama serve

# Set in .env:
LLM_BACKEND=ollama
OLLAMA_MODEL=llama3.2
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

### 5. Open in Browser

```
http://127.0.0.1:8000
```

---

## Configuration Reference

### LLM Settings

```bash
# Choose backend: openai | ollama
LLM_BACKEND=openai

# OpenAI Configuration
OPENAI_API_KEY=your-key-here  # ⚠️ NEVER commit this!
OPENAI_MODEL=gpt-4o-mini      # Fast and cost-effective

# Ollama (local LLM)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# LLM parameters
LLM_TEMPERATURE=0.1      # Lower = more focused (0.0 for deterministic)
LLM_MAX_TOKENS=1000      # Maximum response length
LLM_TIMEOUT=30           # Request timeout in seconds
```

### RAG Mode

```bash
# Enable RAG (retrieval-augmented generation)
USE_RAG=true             # true = LLM with SPARQL context
                         # false = return raw context

# Fast mode (skip LLM, use pattern matching)
ENABLE_FAST_MODE=false   # true = no LLM calls (instant)
                         # false = use LLM planner/explainer
```

### SPARQL Endpoint

```bash
# Current E-OBS gridded dataset endpoint
SPARQL_ENDPOINT=https://obs.knowledgehub.nfdi4earth.de/sparql/
GRAPH_IRI=http://eobs/gridded
```

**To use a different SPARQL endpoint:**

Update `.env`:
```bash
SPARQL_ENDPOINT=https://your-endpoint.com/sparql/
GRAPH_IRI=your-graph-name
```

No code changes required! The backend will automatically use the new endpoint.

### Security & Performance

```bash
MAX_LIMIT=500                   # Maximum rows returned
DEFAULT_LIMIT=200               # Default if no LIMIT specified
SPARQL_TIMEOUT=30               # Query timeout in seconds
CACHE_TTL_MINUTES=15            # Cache duration
MAX_REQUESTS_PER_MINUTE=30      # Rate limit per session
```

---

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

### Manual Docker Build

```bash
docker build -t climate-chat-agent .
docker run -p 8000:8000 climate-chat-agent
```

### Port Configuration

If port 8000 is already in use:
```bash
# Update .env
PORT=8001

# Or override in command
uvicorn main:app --port 8001
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Rate limit exceeded | Wait 1 minute or increase `MAX_REQUESTS_PER_MINUTE` in `.env` |
| SPARQL timeout | Increase `SPARQL_TIMEOUT` or simplify query |
| Date out of range | Use dates between 1950-01-01 and 2024-12-31 |
| Country not found | Use European/Mediterranean countries or coordinates |
| API key error | Check `OPENAI_API_KEY` in `.env` (never commit!) |
| Ollama not found | Run `ollama serve` and verify model is pulled |

### Health Check

Visit http://127.0.0.1:8000/health to check:
- Backend status
- LLM provider connectivity
- SPARQL endpoint connectivity

### Debug Logging

The agent prints debug information to console:
```
[LLM PROVIDER] Backend: OpenAI
[LLM PROVIDER] Model: gpt-4o-mini
[STARTUP] Initializing Climate Chat Agent...
[CONFIG] SPARQL Endpoint: https://obs.knowledgehub.nfdi4earth.de/sparql/
[CONFIG] Graph IRI: http://eobs/gridded
```

Enable more verbose logging:
```bash
uvicorn main:app --reload --log-level debug
```

---

## Performance Tips

1. **Use caching**: Common queries (list properties/features) are cached automatically
2. **Limit results**: Smaller LIMIT values = faster queries
3. **Specific queries**: More specific questions = better results
4. **Rate limiting**: Prevents overload, keeps system responsive
5. **Fast mode**: For simple queries, enable `ENABLE_FAST_MODE=true` for instant responses

---

[← Back to Main README](README.md) | [Development Guide →](DEVELOPMENT.md)
