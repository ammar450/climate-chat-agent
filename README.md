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

### ✨ New in v2.2.0 (February 2026)
- 🔧 **Smart Typo Correction**: Automatically fixes common climate term typos (e.g., "temprature" → "temperature")
- 📅 **Advanced Date Validation**: 
  - Strict YYYY-MM-DD format validation (catches invalid dates like Feb 30)
  - Auto-finds nearest available date when requested date missing
  - Clear messages: "Data for 1950-05-15 not available. Showing 1950-05-16 instead."
  - Enforces 1950-01-01 to 2024-12-31 data range
- 🌍 **Location-Based Filtering**:
  - Support for 50+ European/Mediterranean country names (Germany, France, Italy, etc.)
  - Coordinate parsing (3 formats: "lat: 52.5, lon: 13.4", "52.5, 13.4", "52.5°N 13.4°E")
  - Clear error messages for unavailable countries (USA, China, etc.)
  - Session memory persists location context
- 👥 **Dual Response Formats**: 
  - Primary: Layman-friendly response (simple language, emojis, comparisons)
  - Secondary: Collapsible technical details (SPARQL query, debug info, timings)
  - Auto-detects user preference from keywords
- 💡 **Helpful Error Messages**: Polite rejections with contextual suggestions
- 🎯 **Query Suggestions**: Smart alternatives when queries fail
- 🔄 **Progressive Disclosure**: Main answer + expandable technical details

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
LLM Verbalizer (Ollama/SAIA)
    ├─ Input: question + context from KG
    └─ Output: grounded answer (no hallucinations)
        ↓
User Interface
```

**Key Principle:** The LLM NEVER invents numbers. All facts come from the knowledge graph (SPARQL results).

## � Dataset Information

### E-OBS Gridded Climate Data

This application queries the **E-OBS (European Observations)** gridded climate dataset, a comprehensive collection of daily climate observations across Europe and the Mediterranean region.

**Dataset Specifications:**
- **Temporal Coverage:** January 1, 1950 - December 31, 2024 (75 years)
- **Total Observations:** 328+ million SOSA observations
- **Knowledge Graph Size:** 3.38 billion RDF triples
- **Geographic Coverage:** European and Mediterranean gridded points
- **Temporal Resolution:** Daily observations
- **Format:** Semantic sensor data using SOSA/SSN ontology

**Available Climate Variables (5):**
1. **Air Temperature** (`air_temperature`)
   - ~167 million observations
   - Unit: degrees Celsius (°C)
   
2. **Precipitation Amount** (`precipitation_amount`)
   - ~67 million observations
   - Unit: millimeters (mm)
   
3. **Relative Humidity** (`relative_humidity`)
   - ~51 million observations
   - Unit: percentage (%)
   
4. **Wind Speed** (`wind_speed`)
   - ~24 million observations
   - Unit: meters per second (m/s)
   
5. **Solar Radiation** (`surface_downwelling_shortwave_flux_in_air`)
   - ~43 million observations
   - Unit: watts per square meter (W/m²)

**Data Quality:**
- Gridded interpolation from weather station networks
- Quality-controlled by E-OBS project
- Regular updates with latest observations
- Compliant with CF (Climate and Forecast) conventions

**Access:**
- SPARQL endpoint: `http://141.76.19.254:8890/sparql/`
- Named graph: `<http://eobs/gridded>`
- Query timeout: 400 seconds (Virtuoso limit)

## �🚀 Quick Start

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

### Basic Queries
- "What variables are available?"
- "Show me temperature data"
- "List all locations"

### Time-Based Queries
- "What was the average temperature in March 1950?"
- "Show temperature for 1950-03-15" (specific date)
- "Climate overview for 1950" (all variables)
- "Daily temperature in January 2024"

### Location-Based Queries (New!)
- "Show temperature for Germany in 1950"
- "Climate data for France"
- "Temperature at lat: 52.5, lon: 13.4"
- "Weather in Italy during 2023"

### Statistical Queries
- "Show me the highest humidity values"
- "Average precipitation in 1950"
- "Temperature statistics for 2024"

### Response Formats
- "Explain simply: what was the temperature in 1950?" (layman response)
- "Technical details for temperature in March 1950" (technical response)
- Default: Auto-detects based on your question

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
FROM <http://eobs/gridded>
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
SPARQL_ENDPOINT=http://141.76.19.254:8890/sparql/
GRAPH_IRI=http://eobs/gridded
```

**Dataset Details:**
- **Source:** E-OBS (European Observations) gridded climate dataset
- **Coverage:** 1950-01-01 to 2024-12-31 (75 years)
- **Format:** SOSA (Sensor Observation, Sample, and Actuator) ontology
- **Time Property:** `sosa:resultTime` (observation timestamp)
- **Result Structure:** `sosa:hasResult` → `qudt:numericValue`
- **Scale:** 3.38 billion triples, 328 million observations
- **Variables:** 5 climate properties (temperature, precipitation, humidity, wind, solar)
- **Geographic Coverage:** European and Mediterranean regions (gridded)

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


## \ud83d\udcda Quick Reference

### Data Constraints
- **Time Period**: 1950-01-01 to 2024-12-31 (75 years)
- **Geographic Coverage**: European and Mediterranean regions
- **Available Countries**: Germany, France, Italy, Spain, UK, Greece, Poland, and 40+ more
- **Date Formats**: YYYY-MM-DD, "March 1950", "in 1950"
- **Coordinate Formats**: lat:X lon:Y, decimal pairs, degrees N/S E/W

### Example Queries by Category

**Variables & Locations**
```
What variables are available?
List all locations
```

**Simple Queries**
```
Show temperature in 1950
Average humidity in March 1950
Climate overview for 2024
```

**Location-Based**
```
Temperature for Germany in 1950
Climate in France during 2023
Data at lat: 52.5, lon: 13.4
```

**Advanced**
```
Daily temperature statistics for January 1950
Monthly precipitation averages in 2024
Highest temperature values in 1950
Explain simply: what was the climate like in 1950?
```

### Response Format Keywords
- **Layman**: explain, simply, easy, basic
- **Technical**: detailed, technical, advanced, debug

### Troubleshooting
| Issue | Solution |
|-------|----------|
| Rate limit exceeded | Wait 1 minute or increase MAX_REQUESTS_PER_MINUTE |
| SPARQL timeout | Increase SPARQL_TIMEOUT or simplify query |
| Date out of range | Use dates between 1950-01-01 and 2024-12-31 |
| Country not found | Use European/Mediterranean countries or coordinates |
| API key error | Check OPENAI_API_KEY in .env (never commit!) |

---

**Version 2.3.0** - E-OBS Full Dataset Integration (1950-2024)  
**Last Updated**: April 26, 2026

### Changelog v2.3.0 (April 2026)
- ✅ **Updated SPARQL endpoint** to E-OBS gridded dataset (http://141.76.19.254:8890/sparql/)
- ✅ **Extended data coverage** from 2 years to 75 years (1950-2024)
- ✅ **Massive dataset** with 328M+ observations, 3.38B triples
- ✅ **Fixed time property** from `phenomenonTime` to `resultTime` for E-OBS compatibility
- ✅ **All climate variables** available: temperature, precipitation, humidity, wind speed, solar radiation
- ✅ **Gridded coverage** across European and Mediterranean regions
- ✅ **Improved query templates** optimized for large-scale dataset

### Previous Versions
- **v2.2.0** (Feb 2026) - Location filtering, date validation, dual responses, typo correction
- **v2.1.0** (Jan 2026) - Multi-session chat, caching, rate limiting
- **v2.0.0** (Dec 2025) - RAG implementation, LLM integration

## 🚀 Development

### Running in Development Mode

```bash
# With auto-reload
uvicorn main:app --reload --log-level debug

# Or using Python directly
python main.py
```

### Running with Docker

```bash
# Build and run
docker-compose up --build

# Or manually
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

## 🧪 Testing & Evaluation

### Evaluation Framework

The project includes a comprehensive evaluation framework with 30 test questions covering all 18 SPARQL query templates. This ensures the agent correctly handles various query types across the 1950-2024 E-OBS dataset.

**Quick Start:**
```bash
# Run all 30 evaluation tests
python evaluation/evaluate_agent.py --report

# Run specific test by ID (1-30)
python evaluation/evaluate_agent.py --question-id 5

# Run tests by category
python evaluation/evaluate_agent.py --category statistics

# Save detailed report
python evaluation/evaluate_agent.py --output evaluation_report.json

# Windows users - interactive menu
evaluation\run_evaluation.bat
```

**Test Coverage:**
- ✅ All 18 query templates validated
- ✅ 30 questions across 11 categories (discovery, statistics, aggregation, spatial, etc.)
- ✅ 3 difficulty levels (6 easy, 10 medium, 14 hard)
- ✅ Automated template matching validation
- ✅ Execution time and success rate metrics

**Evaluation Metrics:**
- Template Match Rate: % of correct template selections
- Success Rate: % of queries executing without errors
- Execution Time: Average query performance
- Category/Difficulty Breakdown: Performance by question type

For detailed documentation, see [evaluation/README.md](evaluation/README.md)

### Unit Tests

Individual component tests are available in the `tests/` directory:
```bash
# Run specific tests
python tests/test_typos.py
python tests/test_property_resolver.py
python tests/test_vague_queries.py
```

## 📜 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a Pull Request

**Areas for contribution:**
- Additional SPARQL query templates
- Support for more climate variables
- Enhanced natural language understanding
- Improved visualization options
- Documentation improvements

---

For more details, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) and documentation in the `docs/` folder.

## 🙏 Acknowledgments

  The work has been funded by the European Project EOSC Data Commons.
