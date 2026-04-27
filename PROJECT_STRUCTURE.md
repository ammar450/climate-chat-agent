# Climate Chat Agent - Project Structure

## 📁 Directory Organization

```
climate-chat-agent/
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration (git-ignored, DO NOT COMMIT)
├── .env.example               # Example environment configuration (safe to commit)
├── .gitignore                 # Git ignore rules (includes .env)
├── README.md                  # Main project documentation
│
├── src/                       # Source code (organized by domain)
│   ├── __init__.py
│   │
│   ├── agent/                 # LangGraph agent logic
│   │   ├── __init__.py
│   │   ├── graph_agent.py     # Main LangGraph workflow (11 nodes)
│   │   └── state.py           # TypedDict state definition
│   │
│   ├── llm/                   # LLM providers and clients
│   │   ├── __init__.py
│   │   ├── llm_provider.py    # Multi-backend (OpenAI/Ollama/Anthropic)
│   │   └── llm_client.py      # LLM connection utilities
│   │
│   ├── parsers/               # Natural language parsing
│   │   ├── __init__.py
│   │   ├── property_resolver.py  # Property name → URI mapping (90+ synonyms)
│   │   ├── time_parser.py        # Time range extraction with date validation
│   │   └── typo_corrector.py     # Automatic typo correction
│   │
│   ├── query/                 # SPARQL query management
│   │   ├── __init__.py
│   │   ├── query_templates.py    # 15 safe SPARQL templates
│   │   └── sparql_client.py      # SPARQL endpoint client
│   │
│   ├── formatting/            # Output formatting
│   │   ├── __init__.py
│   │   ├── answer_formatter.py   # Result presentation
│   │   └── response_formatter.py # Dual response format (layman/technical)
│   │
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── error_handler.py      # Query suggestion engine
│
├── static/                    # Frontend assets
│   └── index.html            # Chat UI
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_graph.py         # LangGraph workflow tests
│   ├── test_property_resolver.py  # Property resolution tests
│   ├── test_typos.py         # Typo handling tests
│   ├── test_stats.py         # Statistical queries tests
│   ├── test_daily_monthly.py # Aggregation tests
│   ├── test_1950_data.py     # Data period tests
│   ├── test_quick.py         # Quick smoke tests
│   ├── test_endpoint.py      # SPARQL endpoint tests
│   ├── test_temp_query.py    # Temperature query tests
│   └── test_saia.py          # SAIA integration tests
│
├── evaluation/                # Evaluation framework
│   ├── __init__.py
│   ├── test_questions.json   # 30 test questions covering all 18 templates
│   ├── evaluate_agent.py     # Evaluation script with reporting
│   ├── examples.py           # Example usage and custom analysis
│   ├── run_evaluation.bat    # Windows batch script (interactive menu)
│   └── README.md             # Evaluation documentation
│
└── docs/                      # Documentation
    ├── AGGREGATION_FIXES.md  # Daily/monthly aggregation fixes
    ├── ARCHITECTURE.md       # System architecture
    ├── MIGRATION.md          # Migration guide
    ├── MODEL_SELECTION.md    # LLM model selection guide
    ├── QUICK_REFERENCE.md    # Quick reference
    ├── RAG_IMPLEMENTATION.md # RAG workflow details
    ├── README_LANGGRAPH.md   # LangGraph setup guide
    ├── REFACTORING_COMPLETE.md  # Refactoring summary
    ├── SAIA_SETUP.md         # SAIA configuration
    ├── TEST_PROMPTS.md       # Test queries
    ├── UPDATES.md            # Change log
    └── WORKFLOW_VISUALIZATION.txt  # ASCII workflow diagram
```

## 📦 Module Descriptions

### `src/agent/` - Agent Orchestration
- **graph_agent.py** (1368 lines): Complete LangGraph workflow
  - 11 nodes: load_memory, validation, resolve, planner, route, followup, date_error, build_query, execute_sparql, format_evidence, explainer, save_memory
  - AgentState with 16 fields (includes location, coordinates, date validation)
  - Redis/in-memory session storage with location persistence
  - Fast paths for common queries (list_properties, list_features, vague queries)
  - Conditional routing logic with date error handling
  - Country availability validation (50+ European/Mediterranean countries)
  - Coordinate parsing (3 formats: lat:X lon:Y, decimal pairs, degrees N/S E/W)

### `src/llm/` - LLM Backend
- **llm_provider.py**: Multi-LLM backend abstraction
  - Supports: OpenAI (gpt-4o-mini), Ollama (local), Anthropic (Claude)
  - Environment-based configuration
  - Lazy initialization
  - Compatible message format wrapper

### `src/parsers/` - Natural Language Understanding
- **property_resolver.py** (277 lines): Property name resolution
  - 90+ synonym mappings (temperature, temp, temprature, etc.)
  - Levenshtein distance fuzzy matching (1-2 char tolerance)
  - Lazy prefetching from SPARQL endpoint
  - Handles typos automatically

- **time_parser.py**: Time range extraction with strict validation
  - Parses: "January 1950", "in 1950", "1950-03-15" (YYYY-MM-DD)
  - Exclusive end bounds (YYYY-MM-01T00:00:00 → next month at 00:00:00)
  - Data period validation (1950-01-01 to 2024-12-31)
  - Auto-clipping to available data with user notification
  - Invalid date detection (month 13, day 32, Feb 30)
  - Nearest available date fallback with clear messaging
  - DateValidationError for out-of-range dates

- **typo_corrector.py**: Automatic typo correction
  - 50+ common climate term typos
  - Friendly correction messages ("I noticed you wrote...")
  - Fast dictionary lookup (no fuzzy matching overhead)

### `src/query/` - SPARQL Interface
- **query_templates.py**: Safe SPARQL templates
  - 15 templates: list_properties, list_features, all_properties_summary, location_based_summary, features_near_coordinates, sample_observations, average, extremes, statistics, daily/monthly aggregates, etc.
  - Template-only execution (prevents injection)
  - FROM graph enforcement
  - LIMIT clamping (≤500)

- **sparql_client.py**: SPARQL endpoint client
  - Timeout: 30s
  - Error handling
  - Security validation
  - SPARQLSecurityError for forbidden operations

### `src/formatting/` - Output Presentation
- **answer_formatter.py**: Result formatting
  - format_daily_aggregates(): Daily mean presentation with scope
  - format_monthly_aggregates(): Monthly mean presentation
  - format_timeseries_summary(): Time series statistics
  - Includes scope labels ("aggregated across all grid cells")

- **response_formatter.py**: Dual response format system
  - ResponseFormatDetector: Auto-detects user preference (layman/technical)
  - DualFormatResponder: Generates both response types
  - ResponseFormat enum: LAYMAN, TECHNICAL, AUTO
  - Keyword detection: "explain", "simply", "technical", "detailed"

### `src/utils/` - Utilities
- **error_handler.py**: Query suggestion engine
  - QuerySuggestionEngine: Generates helpful alternatives
  - Contextual help based on error type
  - Friendly error messages with suggestions

## 🚀 Running the Application

### Start the Server
```bash
uvicorn main:app --reload
```

### Run Tests
```bash
# All tests
python -m pytest tests/

# Specific test
python tests/test_daily_monthly.py
```

### Quick Test
```bash
python tests/test_quick.py
```

## 📝 Import Paths

All imports now use the `src.` prefix:

```python
# OLD (removed)
from graph_agent import run_agent
from property_resolver import property_resolver

# NEW (current)
from src.agent.graph_agent import run_agent
from src.parsers.property_resolver import property_resolver
```

## 🗑️ Removed Files

The following obsolete files were removed:
- ✅ `agent.py` - Replaced by `src/agent/graph_agent.py`
- ✅ `switch_backend.py` - One-time utility script (no longer needed)

## 🔧 Configuration

### Environment Variables (.env)
⚠️ **NEVER commit .env to git!** Use .env.example as template.

```bash
# LLM Backend Configuration
LLM_BACKEND=openai              # openai | ollama | anthropic

# OpenAI Configuration (Default)
OPENAI_API_KEY=your-openai-api-key-here  # ⚠️ KEEP SECRET!
OPENAI_MODEL=gpt-4o-mini

# Ollama Configuration (local LLM)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Legacy Provider Config
LLM_PROVIDER=openai
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1000
LLM_TIMEOUT=30

# SPARQL Endpoint
SPARQL_ENDPOINT=https://hyobs.bgc-jena.mpg.de/sparql
GRAPH_IRI=http://hyobs.nfdi4earth.de/graph/climateobservations

# Optional: Redis for session management
# REDIS_URL=redis://localhost:6379/0
```

### Security Best Practices
1. ✅ Always use `.env.example` for templates (safe to commit)
2. ✅ Add `.env` to `.gitignore` (already configured)
3. ⚠️ Rotate API keys if accidentally exposed
4. ✅ Use environment variables for all secrets
5. ✅ Never hardcode API keys in source code

## 📊 Key Features

### Architecture
1. **Organized Structure**: Clear separation of concerns
2. **Modular Design**: Easy to maintain and extend
3. **Clean Imports**: Explicit module paths
4. **Comprehensive Tests**: Isolated in `tests/` directory
5. **Well-Documented**: All docs in `docs/` directory
6. **Production-Ready**: Follows Python best practices

### Intelligence (v2.2.0)
7. **Smart Typo Correction**: Automatically fixes common climate term typos
8. **Strict Date Validation**: Enforces 1950-2024 data range with helpful messages
9. **Dual Response Formats**: Auto-detects and provides layman or technical responses
10. **Location-Based Filtering**: Supports country names and lat/lon coordinates
11. **Country Availability Validation**: Clear messages for unavailable regions
12. **Nearest Date Fallback**: Finds closest available date when requested date missing
13. **Progressive Disclosure**: Main answer + collapsible technical details
14. **Session Memory**: Persists property, time range, and location context

## 🎯 Benefits of New Structure

### Before
```
❌ Mixed files in root (30+ files)
❌ No clear module organization
❌ Difficult to navigate
❌ Imports scattered everywhere
```

### After
```
✅ Clean root (5 files only)
✅ Domain-driven organization
✅ Easy to find files
✅ Explicit import paths
✅ Scalable structure
```

## 📚 Related Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [LangGraph Setup](docs/README_LANGGRAPH.md)
- [Aggregation Fixes](docs/AGGREGATION_FIXES.md)
- [Test Prompts](docs/TEST_PROMPTS.md)
- [Quick Reference](docs/QUICK_REFERENCE.md)

## 🔄 Migration Notes

If you have existing code importing from the old paths:
1. Replace `from X import Y` with `from src.module.X import Y`
2. Update test imports to use `src.` prefix
3. Run tests to verify: `python -m pytest tests/`

All imports in `main.py` and source files have been updated automatically.

## ✅ Verification

Test that everything works:
```bash
# Import test
python -c "from src.agent.graph_agent import run_agent; print('✅ Success')"

# Server test
uvicorn main:app --reload
# Visit http://localhost:8000
```

---
**Last Updated**: February 16, 2026
**Structure Version**: 2.2.0
**Major Features**: Date validation, location filtering, dual responses, typo correction
