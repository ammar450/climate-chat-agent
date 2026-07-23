# 🌍 Climate Chat Agent

**Version 2.3.0** - E-OBS Knowledge Graph Integration (1950-2024)

An intelligent question-answering system for European climate data using Retrieval-Augmented Generation (RAG). Combines Large Language Models with Knowledge Graphs to provide accurate, grounded answers about climate observations.

> **Key Idea:** The LLM does not invent numbers. All climate data comes directly from the E-OBS Knowledge Graph via validated SPARQL queries.

---

## 🚀 Quick Links

- 📦 **[Setup & Installation](SETUP.md)** - Get started in 5 minutes
- 🏗️ **[Architecture Details](docs/ARCHITECTURE.md)** - RAG flow and system design
- 🔌 **[API Reference](API.md)** - REST API documentation
- 👨‍💻 **[Development Guide](DEVELOPMENT.md)** - For contributors and developers
- 📊 **[Evaluation Results](evaluation/EVALUATION_COMPARISON_TABLE.md)** - Performance metrics

---

## ✨ Key Features

- 🤖 **Multi-LLM Support** - Works with Ollama (local) or OpenAI/SAIA (cloud)
- 🧠 **Knowledge-Graph RAG** - Grounded responses from SPARQL queries
- 💬 **Multi-Session Chat** - ChatGPT-like interface with session management
- 🔧 **Smart Typo Correction** - Auto-fixes climate term errors ("temprature" → "temperature")
- 📅 **Advanced Date Validation** - Strict format validation, nearest date fallback (1950-2024)
- 🌍 **Location Filtering** - 50+ European countries, coordinate parsing
- 🚀 **Fast Pattern Matching** - Instant responses for common queries
- 🔒 **Security First** - Query validation, rate limiting, read-only SPARQL
- 📦 **Smart Caching** - Common queries cached for sub-second responses
- 📊 **18 Query Templates** - Covering statistics, time-series, location-based queries

---

## 📊 Dataset

**E-OBS Knowledge Graph** - European Climate Observations

- **5 climate variables:** precipitation (Unit: millimeters (mm)), mean temperature (Unit: degrees Celsius (°C)), relative humidity (Unit: percentage (%)), radiation (Unit: watts per square meter (W/m²)) and wind speed (Unit: meters per second (m/s))
- **0.1° × 0.1° spatial resolution** (~11km grid)
- **Geographic Coverage:** European and Mediterranean gridded points
- **Temporal Coverage:** January 1, 1950 - December 31, 2024 (75 years)
- **Total Observations:** 328+ million SOSA observations
- **Knowledge Graph Size:** 3.38 billion RDF triples
- **Temporal Resolution:** Daily observations
- **Interoperability:** The data has been annotated using the SOSA/SSN ontology

**Data Quality:**
- Gridded interpolation from weather station networks
- Quality-controlled by E-OBS project
- Regular updates with latest observations
- Compliant with CF (Climate and Forecast) conventions

**Access:**
- SPARQL endpoint: `https://obs.knowledgehub.nfdi4earth.de/sparql`
- Named graph: `<climateobservations/eobs-v31>`
- Query timeout: 400 seconds (Virtuoso limit)
---


## 🏗️ Architecture

```
User Question
    ↓
LLM Planner (Ollama/OpenAI)
    ├─ Selects SPARQL query template
    └─ Extracts parameters (location, time, variable)
        ↓
SPARQL Query Execution
    ├─ Security validation (SELECT only)
    └─ Query E-OBS Knowledge Graph
        ↓
Knowledge Graph Results
    └─ Returns: observations, statistics, metadata
        ↓
LLM Answer Generator (Ollama/OpenAI/SAIA)
    ├─ Input: question + KG context
    └─ Output: grounded answer (no hallucinations)
        ↓
User Interface
```

**Key Principle:** The LLM never invents climate data. All numbers come from the knowledge graph.

[**→ Full architecture details**](docs/ARCHITECTURE.md)

---

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

⚠️ **Security**: Never commit `.env` file! It contains your API keys.

3. **For OpenAI (default):**
```bash
# Set in .env:
LLM_BACKEND=openai
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

4. **For Ollama (local):**
```bash
# Pull model
ollama pull llama3.2

# Start Ollama if not running
ollama serve

# Set in .env:
LLM_BACKEND=ollama
OLLAMA_MODEL=llama3.2
```

5. **Run the server**
```bash
uvicorn main:app --reload
```

6. **Open in browser**
```
http://127.0.0.1:8000
```
[**→ Complete setup guide**](SETUP.md)


## ⚙️ Configuration

### LLM Provider Selection

```bash
# Choose backend: openai | ollama | anthropic
LLM_BACKEND=openai

# OpenAI Configuration (Default - Recommended)
OPENAI_API_KEY=your-key-here  # ⚠️ NEVER commit this!
OPENAI_MODEL=gpt-4o-mini      # Fast and cost-effective

# Ollama (local LLM)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Legacy LLM Provider
LLM_PROVIDER=openai

# LLM parameters
LLM_TEMPERATURE=0.1      # Lower = more focused (0.0 for deterministic)
LLM_MAX_TOKENS=1000      # Maximum response length
LLM_TIMEOUT=30           # Request timeout in seconds
```

⚠️ **API Key Security**:
- Never commit `.env` to git (already in `.gitignore`)
- Use `.env.example` for templates
- Rotate keys immediately if exposed
- GitHub will block pushes with exposed keys

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
SPARQL_ENDPOINT=http://141.76.19.254:8890/sparql/
GRAPH_IRI=http://eobs/gridded
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

The following table summarizes the query categories currently supported by the application, and examples for each category.

| Category | Example Query |
|----------|---------------|
| **Overview** | What variables are available? |
| **Overview** | List all locations of observations available. |
| **Overview** | Give me an overview of climate observations for 2024. |
| **Aggregation (Multi-year)** | Show me wind speed trends for the last 5 years. |
| **Aggregation (Single-year)** | Calculate temperature statistics for 2024. |
| **Aggregation (Mean-year)** | What was the average temperature in 2020? |
| **Aggregation (Mean-month)** | Show monthly temperature averages for 2022. |
| **Aggregation (Mean-day)** | What are daily humidity averages for March 2000? |
| **Nested Aggregation** | What was the mean daily temperature in 2001? |
| **Extreme Values** | What were the highest temperature values in 2023? |
| **Subsampling** | Show me some sample observations. |
| **Filtering (Threshold)** | Find temperature readings above 30°C in Summer 2024. |
| **Filtering (Range)** | Find precipitation values between 10 mm and 12 mm in 2001. |
| **Location-based** | What are the grid points near latitude 67.8 and longitude 20.3? |
| **Location-based** | What was the weather like in France during 1985? |
| **Location-based** | Compare temperature across different grid points in 2019. |

### Query Categories

- **Overview** – Explore available variables, locations, and dataset summaries.
- **Aggregation** – Compute statistics over different temporal resolutions (daily, monthly, yearly, or across multiple years).
- **Nested Aggregation** – Perform multi-level aggregations, such as averaging daily values over a year.
- **Extreme Values** – Identify minimum or maximum observations.
- **Subsampling** – Retrieve representative samples from the dataset.
- **Filtering** – Filter observations using thresholds or value ranges.
- **Location-based** – Query observations by geographic location, country, or compare across spatial grid points.

 For more examples of questions, see the [test questions](evaluation/test_questions.json).

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
SELECT (AVG(?value) as ?avg) (SAMPLE(?unit) as ?unit)
FROM <climateobservations/eobs-v31>
WHERE {
  ?obs sosa:observedProperty <http://vocab.nerc.ac.uk/standard_name/air_temperature> ;
       sosa:resultTime ?time ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL { ?result qudt:unit ?unit }
  FILTER(?time >= "1950-03-01"^^xsd:dateTime && 
         ?time < "1950-04-01"^^xsd:dateTime)
}
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

## 🎯 Advanced Features (v2.2.0)

### 1. Date Validation & Fallback
```python
# User: "Show temperature for 2020"
# Response: "Sorry, I only have data from 1950-01-01 to 2024-12-31."

# User: "Show temperature for 1950-05-15"
# If 1950-05-15 doesn't exist:
# Response: "Data for 1950-05-15 not available. Showing 1950-05-16 instead."
```

### 2. Location-Based Filtering
```python
# Supported: 50+ European/Mediterranean countries
Available: Germany, France, Italy, Spain, UK, Greece, Poland...

# Three coordinate formats:
"lat: 52.5, lon: 13.4"      # Explicit labels
"52.5, 13.4"                # Decimal pairs
"52.5°N 13.4°E"             # Degrees with direction

# Unavailable countries get helpful message:
# "Sorry, 'USA' is not available. This dataset contains European
# and Mediterranean regions for 1950-2024.
# specific coordinates if you have data points in 'USA'."
```

### 3. Dual Response System
```python
# Primary Response (Layman):
"The average temperature in Germany in 1950 was 15.3°C 🌡️
That's about 59.5°F - a mild year overall!"

# Technical Details (Collapsible):
🔧 Show Technical Details
  ├─ Query Template: timeseries_statistics
  ├─ Property: Air Temperature
  ├─ Time Range: 1950-01-01 to 1951-01-01
  ├─ Location: Germany
  ├─ Rows Retrieved: 8760
  ├─ Execution Time: 0.234s
  └─ SPARQL Query: [Full query shown]
```

### 4. Typo Correction
```python
# Automatically fixes:
"temprature" → "temperature"
"humdity" → "humidity"
"percipitation" → "precipitation"

# Shows friendly message:
"I noticed you wrote 'temprature' and corrected it to 'temperature'."
```

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

> The backend NEVER exposes the SPARQL endpoint directly

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
├── main.py                          # FastAPI app with caching & rate limiting
├── .env                             # Environment configuration (DO NOT COMMIT!)
├── .env.example                     # Configuration template
├── requirements.txt                  # Python dependencies
├── docker-compose.yml               # Docker configuration
├── Dockerfile                       # Container definition
├── README.md                        # This file
├── PROJECT_STRUCTURE.md             # Detailed architecture documentation
│
├── src/                             # Source code
│   ├── agent/
│   │   ├── graph_agent.py          # LangGraph-based agent workflow
│   │   └── state.py                # Session state management
│   ├── formatting/
│   │   ├── answer_formatter.py     # Formats results for display
│   │   └── response_formatter.py   # Response formatting utilities
│   ├── llm/
│   │   ├── llm_client.py           # LLM interaction (legacy)
│   │   └── llm_provider.py         # Multi-provider LLM support
│   ├── parsers/
│   │   ├── property_resolver.py    # Maps natural language → property URIs
│   │   ├── time_parser.py          # Extracts dates from natural language (1950-2024 validation)
│   │   └── typo_corrector.py       # Auto-corrects common climate term typos
│   ├── query/
│   │   ├── query_templates.py      # Safe SPARQL templates (uses sosa:resultTime)
│   │   ├── sparql_client.py        # Secure SPARQL client (backend only)
│   │   └── wikidata_client.py      # Wikidata enrichment (labels, locations)
│   └── utils/
│       └── error_handler.py        # Helpful error messages & suggestions
│
├── static/                          # Frontend assets
│   ├── index.html                  # Multi-chat web UI
│   ├── style.css                   # Styling
│   └── script.js                   # Chat interface logic
│
├── tests/                           # Test suite
│   ├── test_graph.py               # Agent workflow tests
│   ├── test_typos.py               # Typo correction tests
│   ├── test_vague_queries.py       # Vague query handling
│   └── ...
│
└── docs/                            # Documentation
    ├── ARCHITECTURE.md             # System architecture
    ├── RAG_IMPLEMENTATION.md       # RAG design details
    ├── TEST_PROMPTS.md            # Example test queries
    └── ...
```

**Key Components:**

- **graph_agent.py**: LangGraph workflow for query planning, execution, and answer generation
- **query_templates.py**: 15+ predefined SPARQL templates (all use `sosa:resultTime` for E-OBS compatibility)
- **time_parser.py**: Validates dates within 1950-2024 range, handles date formats
- **property_resolver.py**: Resolves "temperature" → `http://vocab.nerc.ac.uk/standard_name/air_temperature`
- **sparql_client.py**: Security-first SPARQL execution (SELECT only, enforces LIMIT, timeout protection)

## 🔄 SPARQL Configuration

**Current Configuration:**
```bash
# E-OBS Gridded Climate Dataset (1950-2024)
SPARQL_ENDPOINT= https://obs.knowledgehub.nfdi4earth.de/sparql
GRAPH_IRI=climateobservations/eobs-v31
```

**Data Structure Example:**
```turtle
<observation/temp_48.62_43.62_20240101T000000>
  a sosa:Observation ;
  sosa:resultTime "2024-01-01T00:00:00"^^xsd:dateTime ;
  sosa:observedProperty <http://vocab.nerc.ac.uk/standard_name/air_temperature> ;
  sosa:hasFeatureOfInterest <http://www.w3.org/2003/01/geo/wgs84_pos#grid_48.62_43.62> ;
  sosa:hasResult [
    qudt:numericValue 15.3 ;
    qudt:unit <http://qudt.org/vocab/unit/DEG_C>
  ] .
```

**To use a different SPARQL endpoint:**

Update `.env`:
```bash
SPARQL_ENDPOINT=https://your-endpoint.com/sparql/
GRAPH_IRI=http://your-graph-iri.com/data
```

No code changes required! The backend will automatically use the new endpoint.

## 🐛 Debugging

### Enable Debug Logging

The agent prints debug information:
```
[LLM PROVIDER] Backend: OpenAI
[LLM PROVIDER] Model: gpt-4o-mini
[STARTUP] Initializing Climate Chat Agent...
[CONFIG] SPARQL Endpoint: http://141.76.19.254:8890/sparql/
[CONFIG] Graph IRI: http://eobs/gridded
[RESOLVE] Starting resolution for: what variables are available?
[PLAN] Fast path: list_properties
[SPARQL] Executing query against http://141.76.19.254:8890/sparql/
[CACHE HIT] template:list_properties
[SECURITY] Added default LIMIT 200
Cached 5 properties from endpoint
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

## 💻 Troubleshooting
| Issue | Solution |
|-------|----------|
| Rate limit exceeded | Wait 1 minute or increase MAX_REQUESTS_PER_MINUTE |
| SPARQL timeout | Increase SPARQL_TIMEOUT or simplify query |
| Date out of range | Use dates between 1950-01-01 and 2024-12-31 |
| Country not found | Use European/Mediterranean countries or coordinates |
| API key error | Check OPENAI_API_KEY in .env (never commit!) |

## 📊 Performance Tips

1. **Use caching**: Common queries (list properties/features) are cached
2. **Limit results**: Smaller LIMIT values = faster queries
3. **Specific queries**: More specific questions = better results
4. **Rate limiting**: Prevents overload, keeps system responsive

---


## 🧪 Testing & Evaluation

Currently, the project includes an evaluation framework with 48 [test questions](evaluation/test_questions.json):

```bash
# Run full evaluation
python evaluation/evaluate_agent.py --report

# Run specific test
python evaluation/evaluate_agent.py --question-id 5

# Windows users - interactive menu
evaluation\run_evaluation.bat
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests if applicable
5. Submit a Pull Request

**Planned improvements:**
- Enhanced understanding of the user's intent (e.g. LLM-based interpretation of user inputs)
- Additional SPARQL query templates
- Improved visualization of the results
- Integration of additional knowledge graphs beyond Wikidata for federated search

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed guidelines.

---

## 📜 License

MIT License - see LICENSE file for details.

---

## 📞 Support & Documentation

- **Setup Issues?** See [SETUP.md](SETUP.md)
- **Usage Questions?** Check the Usage Examples section above
- **API Integration?** See [API.md](API.md)
- **Want to Contribute?** See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Architecture Details?** See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🎯 Version History

### v2.3.0 (Current)
- E-OBS full dataset integration (1950-2024)
- 328 million observations
- 18 validated query templates

### v2.2.0
- Smart typo correction
- Advanced date validation
- Location-based filtering
- Dual response formats

### v2.1.0
- Multi-session chat interface
- Enhanced caching
- Rate limiting

### v2.0.0
- LangGraph agent integration
- RAG implementation
- SPARQL security hardening

**For detailed version history and changelog, see [docs/UPDATES.md](docs/UPDATES.md)**

---

## 🙏 Acknowledgments

The work has been funded by the European Project EOSC Data Commons. A dump of the knowledge graph is available at https://doi.org/10.34740/kaggle/dsv/16870986. 

If you reuse the EOBS knowledge graph, please cite:

```bash

@inproceedings{yousafEOBSKnowledgeGraph2026,
	address = {Ghent, Belgium},
	title = {The {EOBS} knowledge graph: {A} knowledge graph of {European} climate observations},
	booktitle = {Companion Proceedings of SEMANTiCS 2026},
	author = {Yousaf, Ammar and Degbelo, Auriol},
	year = {2026},
}

```

