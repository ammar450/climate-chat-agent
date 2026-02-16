# Climate Chat Agent - Project Structure

## 📁 Directory Organization

```
climate-chat-agent/
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration (git-ignored)
├── .env.example               # Example environment configuration
├── README.md                  # Main project documentation
│
├── src/                       # Source code (organized by domain)
│   ├── __init__.py
│   │
│   ├── agent/                 # LangGraph agent logic
│   │   ├── __init__.py
│   │   ├── graph_agent.py     # Main LangGraph workflow (10 nodes)
│   │   └── state.py           # Legacy state management
│   │
│   ├── llm/                   # LLM providers and clients
│   │   ├── __init__.py
│   │   ├── llm_provider.py    # Dual backend (Ollama + SAIA)
│   │   └── llm_client.py      # LLM connection utilities
│   │
│   ├── parsers/               # Natural language parsing
│   │   ├── __init__.py
│   │   ├── property_resolver.py  # Property name → URI mapping (90+ synonyms)
│   │   └── time_parser.py        # Time range extraction
│   │
│   ├── query/                 # SPARQL query management
│   │   ├── __init__.py
│   │   ├── query_templates.py    # 13 safe SPARQL templates
│   │   └── sparql_client.py      # SPARQL endpoint client
│   │
│   └── formatting/            # Output formatting
│       ├── __init__.py
│       └── answer_formatter.py   # Result presentation
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
- **graph_agent.py** (736 lines): Complete LangGraph workflow
  - 10 nodes: load_memory, resolve, planner, route, followup, build_query, execute_sparql, format_evidence, explainer, save_memory
  - AgentState with 13 fields
  - Redis/in-memory session storage
  - Fast paths for common queries
  - Conditional routing logic

### `src/llm/` - LLM Backend
- **llm_provider.py** (157 lines): Dual LLM backend abstraction
  - Supports: Ollama (local) + SAIA (cloud)
  - Environment-based configuration
  - Lazy initialization
  - Compatible message format wrapper

### `src/parsers/` - Natural Language Understanding
- **property_resolver.py** (277 lines): Property name resolution
  - 90+ synonym mappings (temperature, temp, temprature, etc.)
  - Levenshtein distance fuzzy matching (1-2 char tolerance)
  - Lazy prefetching from SPARQL endpoint
  - Handles typos automatically

- **time_parser.py** (203 lines): Time range extraction
  - Parses: "January 1950", "in 1950", "between 1950 and 1951"
  - Exclusive end bounds (YYYY-MM-01T00:00:00 → next month at 00:00:00)
  - Data period validation (1950-1951)
  - Auto-clipping to available data

### `src/query/` - SPARQL Interface
- **query_templates.py** (304 lines): Safe SPARQL templates
  - 13 templates: list_properties, list_features, average, extremes, statistics, daily/monthly aggregates, etc.
  - Template-only execution (prevents injection)
  - FROM graph enforcement
  - LIMIT clamping (≤500)

- **sparql_client.py**: SPARQL endpoint client
  - Timeout: 30s
  - Error handling
  - Security validation

### `src/formatting/` - Output Presentation
- **answer_formatter.py** (293 lines): Result formatting
  - format_daily_aggregates(): Daily mean presentation with scope
  - format_monthly_aggregates(): Monthly mean presentation
  - format_timeseries_summary(): Time series statistics
  - Includes scope labels ("aggregated across all grid cells")

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
```bash
# LLM Backend
LLM_BACKEND=ollama              # ollama | saia
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
SAIA_BASE_URL=https://chat-ai.academiccloud.de/v1
SAIA_API_KEY=your-key-here
SAIA_MODEL=codestral-22b

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 📊 Key Features

1. **Organized Structure**: Clear separation of concerns
2. **Modular Design**: Easy to maintain and extend
3. **Clean Imports**: Explicit module paths
4. **Comprehensive Tests**: Isolated in `tests/` directory
5. **Well-Documented**: All docs in `docs/` directory
6. **Production-Ready**: Follows Python best practices

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
**Last Updated**: January 26, 2026
**Structure Version**: 2.0
