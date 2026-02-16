# Climate Data Chat Agent 🌍

A production-ready RAG-powered chat agent for querying climate observation data using **LangGraph** orchestration, SPARQL templates, and local/cloud LLM support.

## Architecture

**LangGraph-based Template KG-RAG with Router + Memory**

```
User Query → LangGraph Workflow:
  ├─ load_memory: Restore session state (property/time/feature)
  ├─ resolve: Extract property, time, feature from message
  ├─ plan: LLM planner outputs JSON with template + params
  ├─ route: Followup question? → followup_node → END
  │         OR → build_query_node
  ├─ build_query: Render SPARQL template with safety checks
  ├─ execute_sparql: Query Virtuoso with timeout/retry
  ├─ format_evidence: Create compact evidence text from results
  ├─ explain: LLM explainer generates grounded answer
  └─ save_memory: Persist session state → END
```

## Features

✅ **Multi-turn Conversations** - Session memory tracks selected property, time range, and feature  
✅ **Safe SPARQL** - Template-based queries only (blocks INSERT/DELETE/LOAD/etc)  
✅ **Grounded Answers** - LLM generates answers from structured evidence, not raw data  
✅ **Multi-LLM Support** - Ollama (local) + SAIA (cloud, OpenAI-compatible)  
✅ **Production Ready** - Timeouts, retries, rate limiting, Redis session store  
✅ **Debug Mode** - View SPARQL query, template used, latency, evidence  

## Quick Start

### 1. Prerequisites

- **Python 3.10+**
- **Ollama** (for local LLM): [ollama.com](https://ollama.com)
- **Redis** (optional, for session memory): [redis.io](https://redis.io)

### 2. Install Dependencies

```bash
cd climate-chat-agent
pip install -r requirements.txt
```

### 3. Pull Ollama Model

```bash
ollama pull llama3.2
```

### 4. Configure Environment

Create `.env` file:

```bash
# LLM Configuration
LLM_PROVIDER=ollama          # ollama | saia
OLLAMA_MODEL=llama3.2
OLLAMA_URL=http://localhost:11434/api/chat

# SAIA (Optional - OpenAI-compatible API)
SAIA_API_KEY=your_api_key_here
SAIA_MODEL=gpt-4
SAIA_URL=https://chat-ai.academiccloud.de/v1/chat/completions

# SPARQL Endpoint
SPARQL_ENDPOINT=https://hyobs.webapps.nfdi4earth.de/sparql/
GRAPH_IRI=http://hyobs.nfdi4earth.de/graph/climateobservations

# Redis (Optional - falls back to in-memory if not set)
REDIS_URL=redis://localhost:6379/0

# Server Configuration
CACHE_TTL_MINUTES=15
MAX_REQUESTS_PER_MINUTE=30
LLM_TIMEOUT=30
```

### 5. Run the Server

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Open the Chat UI

Navigate to: **http://localhost:8000/static/index.html**

## Usage Examples

**List available properties:**
```
What variables are available?
```

**Query temperature data:**
```
Show me temperature observations
```

**Filter by time:**
```
Show temperature data from 2020
```

**Get averages:**
```
What's the average temperature in January 2020?
```

**Follow-up questions:**
```
User: Show me temperature data
Agent: [shows data for 2023]
User: Now show 1951
Agent: [shows temperature data for 1951]
```

## Model Selection

Click the dropdown in the header to select:

- **Llama 3.2 (Local)** - Default, runs via Ollama
- **GPT-4 (SAIA)** - Cloud model (requires API key)
- **Custom models** - Any Ollama model you've pulled

Add more Ollama models:
```bash
ollama pull mistral
ollama pull llama3.1
ollama pull codellama
```

Refresh the page to see them in the dropdown.

## LangGraph Workflow Details

### State Schema

```python
class AgentState(TypedDict):
    # Input
    session_id: str
    user_message: str
    history: List[Dict]
    model: Optional[str]  # "provider:model_name"
    
    # Session memory
    selected_property_uri: Optional[str]
    selected_feature_uri: Optional[str]
    time_range: Optional[Dict]  # {"start": "...", "end": "..."}
    
    # Processing
    plan: Optional[Dict]  # {"template": "...", "params": {...}, "followup": ...}
    sparql_query: Optional[str]
    sparql_rows: Optional[List]
    evidence_text: Optional[str]
    final_answer: Optional[str]
    
    # Debug
    debug: Dict  # latency, row count, errors
```

### Available Templates

| Template | Description | Required Params |
|----------|-------------|----------------|
| `list_properties` | List all climate variables | None |
| `list_features` | List observation stations | None |
| `sample_observations` | Show sample data | `property_uri` |
| `average_for_property_date_range` | Calculate average | `property_uri`, `start`, `end` |
| `top_extremes_for_property` | Show highest/lowest | `property_uri`, `order`, `limit` |

### Safety Guarantees

1. **Template-only queries** - No arbitrary SPARQL
2. **SELECT-only** - Blocks INSERT/DELETE/LOAD/CLEAR/DROP/etc
3. **FROM graph enforcement** - Always queries correct graph
4. **LIMIT clamping** - Maximum 500 rows
5. **Timeout** - 30s for SPARQL, 30s for LLM
6. **Validation** - JSON schema validation on LLM outputs

## API Reference

### POST `/chat`

**Request:**
```json
{
  "message": "Show me temperature data",
  "session_id": "abc123",
  "model": "ollama:llama3.2",
  "history": []
}
```

**Response:**
```json
{
  "answer": "Here are temperature observations...",
  "context": "📊 Property: Air Temperature | 📅 Period: 2023-01-01 to 2023-12-31",
  "sparql": "SELECT ?time ?value ?unit WHERE { ... }",
  "rows": [...],  // First 10 rows
  "used_template": "sample_observations"
}
```

### GET `/models`

Returns available LLM models (dynamically fetched from Ollama + SAIA config).

### GET `/health`

Health check for LLM provider and SPARQL endpoint.

## Development

### Project Structure

```
climate-chat-agent/
├── graph_agent.py          # LangGraph workflow definition
├── llm_client.py           # Unified LLM interface (Ollama + SAIA)
├── main.py                 # FastAPI application
├── sparql_client.py        # SPARQL execution with security
├── query_templates.py      # Safe SPARQL templates
├── property_resolver.py    # Property URI resolution
├── time_parser.py          # Time range extraction
├── state.py                # Session state management
├── static/
│   └── index.html         # Chat UI
├── requirements.txt
├── .env.example
└── README.md
```

### Run Tests

```bash
pytest tests/
```

### Debug Mode

Toggle debug in the UI to see:
- SPARQL query
- Template used
- Evidence summary
- Latency per node
- Row count
- LLM provider/model

## Troubleshooting

**LLM not responding:**
- Check Ollama is running: `ollama list`
- Verify model pulled: `ollama pull llama3.2`
- Test SAIA API key if using cloud

**SPARQL errors:**
- Verify endpoint: `curl https://hyobs.webapps.nfdi4earth.de/sparql/`
- Check graph IRI in `.env`

**Redis connection failed:**
- Falls back to in-memory session store
- Install Redis: `brew install redis` or `apt install redis`

**Model not in dropdown:**
- Pull the model: `ollama pull <model-name>`
- Refresh the page

## Production Deployment

**Environment variables to set:**
```bash
LLM_PROVIDER=saia                    # Use cloud LLM
SAIA_API_KEY=your_production_key
REDIS_URL=redis://redis:6379/0       # Use Redis for sessions
MAX_REQUESTS_PER_MINUTE=100          # Increase rate limit
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LLM_PROVIDER=saia
      - SAIA_API_KEY=${SAIA_API_KEY}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

**Security checklist:**
- [ ] Set CORS origins to specific domains
- [ ] Enable HTTPS
- [ ] Rotate API keys regularly
- [ ] Monitor rate limits
- [ ] Set up logging/monitoring

## License

MIT

## Contributors

Built with ❤️ for climate data exploration.
