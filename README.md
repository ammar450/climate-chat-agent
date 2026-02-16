# Climate Chat Agent

A secure, RAG-enhanced chat application for querying climate observation data using natural language. Features LLM-powered query planning, knowledge-graph retrieval (SPARQL), and grounded answer generation.

## 🎯 Features

### Core Features
- 🤖 **Multi-LLM Support**: Works with Ollama (local) or SAIA (cloud, OpenAI-compatible)
- 🧠 **Knowledge-Graph RAG**: Retrieves facts from SPARQL before answering (grounded responses)
- 💬 **Multiple Chat Sessions**: Manage multiple conversations with sidebar (like ChatGPT)  
- 🚀 **Fast Pattern Matching**: Optional instant responses without LLM overhead
- 🔒 **Security First**: Backend-only SPARQL access with query validation
- 📦 **Smart Caching**: Common queries cached for instant responses
- 🛡️ **Rate Limiting**: 30 requests per minute per session
- 🎨 **Modern UI**: Clean, ChatGPT-inspired interface
- 📊 **SPARQL Transparency**: See the actual queries being executed

### ✨ New in v2.1.0 (January 2026)
- 🔧 **Smart Typo Correction**: Automatically fixes common climate term typos (e.g., "temprature" → "temperature")
- 📅 **Strict Date Validation**: Enforces 1950-1951 data range with helpful error messages
- 👥 **Dual Response Formats**: Auto-detects and provides layman or technical responses
- 💡 **Helpful Error Messages**: Polite rejections with contextual suggestions
- 🎯 **Query Suggestions**: Smart alternatives when queries fail
- 🔄 **Progressive Disclosure**: Layered responses (summary → details → technical)

## 🏗️ Architecture (RAG Flow)

```
User Question
    ↓
LLM Planner (Ollama/SAIA)
    ├─ Outputs: {"template": "...", "params": {...}}
    └─ Selects appropriate query template
        ↓
SPARQL Query Execution
    ├─ Security validation (SELECT only)
    ├─ Enforce FROM <graph>
    └─ Enforce LIMIT ≤ 500
        ↓
Knowledge Graph (Virtuoso)
    └─ Returns: observations, properties, metadata
        ↓
Context Builder
    ├─ Extracts: values, stats, time ranges
    └─ Creates: compact context text
        ↓
LLM Explainer (Ollama/SAIA)
    ├─ Input: question + context from KG
    └─ Output: grounded answer (no hallucinations)
        ↓
User Interface
```

**Key Principle:** The LLM NEVER invents numbers. All facts come from the knowledge graph (SPARQL results).

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- **Either:**
  - [Ollama](https://ollama.com/download) installed locally, OR
  - SAIA API key (OpenAI-compatible)

### Installation

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env to set LLM provider and credentials
```

3. **For Ollama (local):**
```bash
# Pull model
ollama pull llama3.2

# Start Ollama if not running
ollama serve

# Set in .env:
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

4. **For SAIA (cloud):**
```bash
# Set in .env:
LLM_PROVIDER=saia
SAIA_API_KEY=your-api-key-here
SAIA_MODEL=gpt-4
```

5. **Run the server**
```bash
uvicorn main:app --reload
```

6. **Open in browser**
```
http://127.0.0.1:8000
```

## ⚙️ Configuration

### LLM Provider Selection

```bash
# Choose provider: ollama | saia
LLM_PROVIDER=ollama

# Ollama (local LLM)
OLLAMA_URL=http://localhost:11434/api/chat
OLLAMA_MODEL=llama3.2

# SAIA (OpenAI-compatible cloud API)
SAIA_URL=https://chat-ai.academiccloud.de/v1/chat/completions
SAIA_API_KEY=sk-proj-YOUR-KEY-HERE
SAIA_MODEL=gpt-4

# LLM parameters
LLM_TEMPERATURE=0.1      # Lower = more focused
LLM_MAX_TOKENS=1000      # Maximum response length
LLM_TIMEOUT=30           # Request timeout
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
SPARQL_ENDPOINT=https://hyobs.webapps.nfdi4earth.de/sparql/
GRAPH_IRI=http://hyobs.nfdi4earth.de/graph/climateobservations
```

### Security & Performance
```bash
MAX_LIMIT=500                   # Maximum rows returned
DEFAULT_LIMIT=200               # Default if no LIMIT specified
SPARQL_TIMEOUT=30               # Query timeout in seconds
CACHE_TTL_MINUTES=15            # Cache duration
MAX_REQUESTS_PER_MINUTE=30      # Rate limit per session
```

## 💬 Usage Examples

Try asking:

- "What variables are available?"
- "Show me temperature data"
- "What was the average temperature in March 1950?"
- "Show me the highest humidity values"
- "List all locations"

### RAG vs Fast Mode

**RAG Mode (USE_RAG=true, ENABLE_FAST_MODE=false):**
- LLM plans query → SPARQL retrieves data → LLM generates grounded answer
- Best for: Natural conversation, complex questions, explanations
- Pros: Natural language, context-aware, no hallucinations
- Cons: Slower (LLM calls), requires API/local LLM

**Fast Mode (ENABLE_FAST_MODE=true):**
- Pattern matching selects template → SPARQL retrieves data → formatted output
- Best for: Speed, simple queries, low latency
- Pros: Instant responses, no LLM needed
- Cons: Less flexible, template-based only

## 🧠 How RAG Works

### 1. Query Planning (LLM)
User asks: *"What was the average temperature in March 1950?"*

LLM outputs:
```json
{
  "template": "average_for_property_date_range",
  "params": {
    "property_uri": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
    "start": "1950-03-01T00:00:00",
    "end": "1950-04-01T00:00:00"
  }
}
```

### 2. SPARQL Retrieval
```sparql
SELECT (AVG(?value) as ?avg) ?unit
FROM <http://hyobs.nfdi4earth.de/graph/climateobservations>
WHERE {
  ?obs sosa:observedProperty <http://...air_temperature> ;
       sosa:resultTime ?time ;
       sosa:hasSimpleResult ?value .
  FILTER(?time >= "1950-03-01"^^xsd:dateTime && 
         ?time < "1950-04-01"^^xsd:dateTime)
}
```

Returns: `avg=15.3, unit=degC`

### 3. Context Building
```
Query type: average_for_property_date_range
Result count: 1
Property: Air Temperature
Time range: 1950-03-01 to 1950-04-01
Average value: 15.3 degC
```

### 4. Answer Generation (LLM)
System prompt:
> "Answer based ONLY on the provided context. Do NOT invent values."

Context + Question → LLM

Response:
> "Based on the climate observations, the average air temperature in March 1950 was 15.3°C."

✅ **Grounded** - uses actual value from knowledge graph  
❌ **No hallucination** - doesn't invent numbers

## 🔐 Security Features

### 1. Query Validation
- ✅ Only `SELECT` queries allowed
- ❌ Blocks `INSERT`, `DELETE`, `UPDATE`, `DROP`, etc.
- ✅ Enforces `FROM <graph>` clause
- ✅ Enforces `LIMIT ≤ MAX_LIMIT`
- ✅ Auto-adds `LIMIT DEFAULT_LIMIT` if missing

### 2. Rate Limiting
- 30 requests per minute per session (configurable)
- Returns HTTP 429 when exceeded
- In-memory tracking (resets on server restart)

### 3. Caching
- Common queries cached for 15 minutes (configurable)
- `list_properties` and `list_features` pre-cached at startup
- Reduces load on SPARQL endpoint

### 4. Timeout Protection
- 30-second timeout on SPARQL queries (configurable)
- 30-second timeout on LLM requests
- Prevents hanging requests

### 5. Error Handling
- Graceful error messages
- Detailed logging for debugging
- Health check endpoint

## 📚 API Endpoints

### Frontend Endpoints

**POST /chat**
```json
{
  "message": "What variables are available?",
  "session_id": "uuid-here"
}
```

**POST /reset**
```json
{
  "session_id": "uuid-here"
}
```

**GET /health**
```json
{
  "status": "healthy",
  "llm_provider": "ollama",
  "llm": "ok",
  "sparql": "ok"
}
```

**GET /**
Returns the web UI

### Backend NEVER exposes SPARQL endpoint directly

## 📝 Query Templates

The system uses predefined SPARQL templates for safety:

1. **list_properties**: Lists all available climate variables
2. **list_features**: Lists all observation locations
3. **sample_observations**: Shows example observations
4. **timeseries_for_feature_property**: Time series for specific location and property
5. **average_for_property_date_range**: Average values over time period
6. **top_extremes_for_property**: Highest/lowest values for a property

## 🏗️ Project Structure

```
climate-chat-agent/
├── main.py                 # FastAPI app with caching & rate limiting
├── agent.py                # Pattern-based query planning
├── sparql_client.py        # Secure SPARQL client (ONLY component that calls endpoint)
├── query_templates.py      # Safe SPARQL templates
├── property_resolver.py    # Maps natural language → property URIs
├── time_parser.py          # Extracts dates from natural language
├── answer_formatter.py     # Formats results for display
├── state.py                # Session state management
├── requirements.txt        # Python dependencies
├── .env.example            # Configuration template
└── static/
    └── index.html          # Frontend UI (multi-chat interface)
```

## 🔄 Swapping SPARQL Endpoints

To use a different SPARQL endpoint, update `.env`:

```bash
SPARQL_ENDPOINT=https://your-endpoint.com/sparql/
GRAPH_IRI=http://your-graph-iri.com/data
```

No code changes required! The backend will automatically use the new endpoint.

## 🐛 Debugging

### Enable Debug Logging

The agent prints debug information:
```
[DEBUG] Planning query for: 'what variables are present'
[DEBUG] Found keyword: variable
[DEBUG] Resolver returned: uri=..., confidence=...
[SECURITY] Added default LIMIT 200
[SPARQL] Executing query against https://...
[CACHE HIT] template:list_properties
```

### Health Check

Visit http://127.0.0.1:8000/health to check:
- Backend status
- SPARQL endpoint connectivity

### Common Issues

**Rate limit exceeded:**
- Wait 1 minute or increase `MAX_REQUESTS_PER_MINUTE` in `.env`

**SPARQL timeout:**
- Increase `SPARQL_TIMEOUT` in `.env`
- Simplify your query

**Security error:**
- Query contains forbidden keywords
- Check that you're using SELECT only

## 📊 Performance Tips

1. **Use caching**: Common queries (list properties/features) are cached
2. **Limit results**: Smaller LIMIT values = faster queries
3. **Specific queries**: More specific questions = better results
4. **Rate limiting**: Prevents overload, keeps system responsive

## 🤝 Contributing

To extend the system:

1. **Add new templates** in `query_templates.py`
2. **Add new intents** in `agent.py` pattern matching
3. **Add new formatters** in `answer_formatter.py`
4. **Update UI** in `static/index.html`

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- NFDI4Earth for the climate observation dataset
- Virtuoso for the SPARQL endpoint
- FastAPI for the web framework

---

**Version 2.0.0** - Secure, cached, rate-limited architecture with multi-chat support

**Response:**
```json
{
  "answer": "The dataset contains the following variables...",
  "sparql": "PREFIX sosa: ...",
  "rows": [...],
  "used_template": "list_properties"
}
```

## Project Structure

```
climate-chat-agent/
├── main.py                 # FastAPI application
├── agent.py               # LLM planning and explanation
├── sparql_client.py       # SPARQL execution and safety
├── query_templates.py     # Template definitions
├── static/
│   └── index.html        # Chat UI
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Configuration

Environment variables (in `.env`):

- `OLLAMA_MODEL`: Ollama model to use (default: `llama3.2`)
- `PORT`: Server port (default: `8000`)

## Troubleshooting

### Ollama not reachable

Make sure Ollama is running:
```bash
ollama serve
```

Check if model is downloaded:
```bash
ollama list
```

### SPARQL endpoint unreachable

Check `/health` endpoint to verify connectivity to the Virtuoso endpoint.

### Port already in use

Change the port:
```bash
uvicorn main:app --port 8001
```

## Development

To run in development mode with auto-reload:

```bash
uvicorn main:app --reload --log-level debug
```

## License

MIT License

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
