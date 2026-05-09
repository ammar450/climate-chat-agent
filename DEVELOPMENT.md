# Development Guide

Guide for developers working on the Climate Chat Agent.

## Project Structure

```
climate-chat-agent/
├── main.py                          # FastAPI app with caching & rate limiting
├── .env                             # Environment configuration (DO NOT COMMIT!)
├── .env.example                     # Configuration template
├── requirements.txt                  # Python dependencies
├── docker-compose.yml               # Docker configuration
├── Dockerfile                       # Container definition
├── README.md                        # Main documentation
├── SETUP.md                         # Installation guide
├── DEVELOPMENT.md                   # This file
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
│   │   ├── time_parser.py          # Extracts dates (1950-2024 validation)
│   │   └── typo_corrector.py       # Auto-corrects climate term typos
│   ├── query/
│   │   ├── query_templates.py      # Safe SPARQL templates
│   │   ├── sparql_client.py        # Secure SPARQL client
│   │   └── wikidata_client.py      # Wikidata enrichment
│   └── utils/
│       └── error_handler.py        # Error messages & suggestions
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
├── evaluation/                      # Evaluation framework
│   ├── evaluate_agent.py           # Main evaluation script
│   ├── test_questions.json         # 30 test questions
│   └── README.md                   # Evaluation docs
│
└── docs/                            # Additional documentation
    ├── ARCHITECTURE.md             # System architecture
    ├── RAG_IMPLEMENTATION.md       # RAG design details
    ├── TEST_PROMPTS.md            # Example test queries
    └── ...
```

---

## Key Components

### Core Files

- **graph_agent.py**: LangGraph workflow for query planning, execution, and answer generation
- **query_templates.py**: 15+ predefined SPARQL templates for safe query execution
- **time_parser.py**: Validates dates within 1950-2024 range, handles multiple date formats
- **property_resolver.py**: Resolves "temperature" → `http://vocab.nerc.ac.uk/standard_name/air_temperature`
- **sparql_client.py**: Security-first SPARQL execution (SELECT only, enforces LIMIT, timeout protection)

### Frontend

- **index.html**: Multi-session chat interface (similar to ChatGPT)
- **script.js**: Handles chat interactions, session management, markdown rendering
- **style.css**: Modern, responsive styling

---

## Running in Development Mode

### Standard Development

```bash
# With auto-reload
uvicorn main:app --reload --log-level debug

# Or using Python directly
python main.py
```

### Docker Development

```bash
# Build and run
docker-compose up --build

# Rebuild after changes
docker-compose up --build --force-recreate
```

### Port Configuration

```bash
# Update .env
PORT=8001

# Or override in command
uvicorn main:app --port 8001
```

---

## Testing & Evaluation

### Evaluation Framework

The project includes a comprehensive evaluation framework with 30 test questions covering all query templates.

**Quick Start:**
```bash
# Run all 30 evaluation tests
python evaluation/evaluate_agent.py --report

# Run specific test by ID (1-30)
python evaluation/evaluate_agent.py --question-id 5

# Run tests by category
python evaluation/evaluate_agent.py --category statistics

# Save detailed report
python evaluation/evaluate_agent.py --output evaluation_report.json --llm-judge

# Windows users - interactive menu
evaluation\run_evaluation.bat
```

**Test Coverage:**
- ✅ All 18 query templates validated
- ✅ 30 questions across 11 categories
- ✅ 3 difficulty levels (6 easy, 10 medium, 14 hard)
- ✅ Automated template matching validation
- ✅ Execution time and success rate metrics
- ✅ Optional LLM-as-judge evaluation

**Evaluation Metrics:**
- Template Match Rate: % of correct template selections
- Execution Success Rate: % of queries executing without errors
- Average Execution Time: Query performance
- LLM Judge Scores: Semantic correctness evaluation

For detailed documentation, see [evaluation/README.md](evaluation/README.md)

### Unit Tests

Individual component tests:
```bash
# Test typo correction
python tests/test_typos.py

# Test property resolution
python tests/test_property_resolver.py

# Test vague query handling
python tests/test_vague_queries.py

# Test graph agent workflow
python tests/test_graph.py

# Test time parsing
python tests/test_daily_monthly.py
```

---

## Extending the System

### 1. Adding New Query Templates

Edit `src/query/query_templates.py`:

```python
TEMPLATES = {
    # ... existing templates ...
    
    "your_new_template": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
SELECT ?result
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasResult ?result .
}}
LIMIT {limit}"""
}
```

### 2. Adding New Intent Patterns

Edit `src/agent/graph_agent.py` in the `plan_node()` function:

```python
# Fast-path pattern matching
if "your keyword" in msg_lower:
    return {
        "template": "your_new_template",
        "params": {...}
    }
```

### 3. Adding New Formatters

Edit `src/formatting/answer_formatter.py`:

```python
def format_your_new_template(results, params):
    """Format results for your new template."""
    # Custom formatting logic
    return formatted_text
```

### 4. Updating the UI

Edit `static/index.html` or `static/script.js` for frontend changes.

---

## Debugging Tips

### Enable Debug Logging

```bash
uvicorn main:app --reload --log-level debug
```

The agent prints detailed information:
```
[LLM PROVIDER] Backend: OpenAI
[STARTUP] Initializing Climate Chat Agent...
[CONFIG] SPARQL Endpoint: https://obs.knowledgehub.nfdi4earth.de/sparql/
[RESOLVE] Starting resolution for: what variables are available?
[PLAN] Fast path: list_properties
[SPARQL] Executing query against endpoint
[CACHE HIT] template:list_properties
[FORMAT] Formatting 5 results
```

### Common Development Issues

**Template not working:**
- Check SPARQL syntax in `query_templates.py`
- Verify all placeholders (`{graph}`, `{property_uri}`, etc.) are defined
- Test query directly on SPARQL endpoint

**Agent not selecting right template:**
- Check pattern matching in `graph_agent.py`
- Add debug prints to see LLM planner output
- Verify template name matches exactly

**Cache not updating:**
- Restart the server to clear cache
- Adjust `CACHE_TTL_MINUTES` in `.env`
- Check cache key generation in `main.py`

---

## Code Style & Best Practices

### Python Code

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to all functions
- Keep functions focused (single responsibility)
- Use descriptive variable names

### Security

- **Never** expose SPARQL endpoint directly to frontend
- Always validate and sanitize user input
- Enforce query limits and timeouts
- Use environment variables for sensitive data
- Never commit `.env` file

### Performance

- Cache frequently used queries
- Limit SPARQL result sizes
- Use indexes where appropriate
- Monitor query execution times
- Implement rate limiting

---

## Architecture Diagrams

### RAG Flow

```
User Question
    ↓
LLM Planner (Ollama/OpenAI)
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
LLM Explainer (Ollama/OpenAI)
    ├─ Input: question + context from KG
    └─ Output: grounded answer (no hallucinations)
        ↓
User Interface
```

**Key Principle:** The LLM NEVER invents numbers. All facts come from the knowledge graph.

---

## Contributing

We welcome contributions! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow code style guidelines
   - Add tests if applicable
   - Update documentation
4. **Test your changes**
   ```bash
   python evaluation/evaluate_agent.py --report
   ```
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Submit a Pull Request**
   - Describe what changed and why
   - Reference any related issues
   - Include test results if applicable

### Areas for Contribution

- 🔧 Additional SPARQL query templates
- 🌍 Support for more climate variables
- 🧠 Enhanced natural language understanding
- 📊 Improved visualization options
- 📝 Documentation improvements
- 🧪 More comprehensive test coverage
- 🚀 Performance optimizations
- 🎨 UI/UX enhancements

### Code Review Process

All contributions will be reviewed for:
- Code quality and style
- Test coverage
- Documentation updates
- Security implications
- Performance impact

---

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality (backwards-compatible)
- PATCH version for backwards-compatible bug fixes

### Current Version

**v2.3.0** - E-OBS Full Dataset Integration (1950-2024)

### Changelog

See main [README.md](README.md) for detailed version history.

---

[← Back to Main README](README.md) | [Setup Guide →](SETUP.md) | [API Reference →](API.md)
