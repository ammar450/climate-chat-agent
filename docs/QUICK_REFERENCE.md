# 🚀 LangGraph Climate Agent - Quick Reference

## Installation
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Files Added/Modified

| File | Status | Description |
|------|--------|-------------|
| `graph_agent.py` | ✅ NEW | LangGraph workflow (570 lines) |
| `main.py` | ✅ MODIFIED | Simplified chat endpoint |
| `requirements.txt` | ✅ UPDATED | Added langgraph, langchain-core, redis |
| `test_graph.py` | ✅ NEW | Test suite |
| `README_LANGGRAPH.md` | ✅ NEW | Production guide |
| `MIGRATION.md` | ✅ NEW | Migration guide |
| `REFACTORING_COMPLETE.md` | ✅ NEW | Summary document |
| `WORKFLOW_VISUALIZATION.txt` | ✅ NEW | ASCII workflow diagram |

## Environment Variables

```bash
# Required
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
SPARQL_ENDPOINT=https://hyobs.webapps.nfdi4earth.de/sparql/
GRAPH_IRI=http://hyobs.nfdi4earth.de/graph/climateobservations

# Optional
REDIS_URL=redis://localhost:6379/0
SAIA_API_KEY=your_key
SAIA_MODEL=gpt-4
```

## LangGraph Nodes

1. **load_memory** → Restore session state
2. **resolve** → Extract property/time/feature
3. **planner** → LLM outputs JSON plan
4. **route** → Conditional: followup OR build_query
5. **followup** → Ask clarification
6. **build_query** → Render SPARQL template
7. **execute_sparql** → Query Virtuoso
8. **format_evidence** → Create context text
9. **explainer** → LLM generates answer
10. **save_memory** → Persist session state

## API Usage

```python
from graph_agent import run_agent

result = run_agent(
    session_id="user123",
    user_message="Show me temperature data",
    history=[],
    model="ollama:llama3.2"
)

# Returns:
{
    "answer": "Here are the temperature observations...",
    "used_template": "sample_observations",
    "sparql": "SELECT ?time ?value WHERE { ... }",
    "rows": [...],
    "evidence": "Query type: sample_observations...",
    "debug": {
        "resolve_time": 0.003,
        "plan_time": 1.245,
        "execute_time": 0.456,
        "explain_time": 1.123,
        "row_count": 150
    }
}
```

## Testing

```bash
# Run all tests
python test_graph.py

# Test individual queries
python -c "from graph_agent import run_agent; print(run_agent('test', 'What variables?', []))"
```

## Common Commands

```bash
# Start server
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Test health
curl http://localhost:8000/health

# List models
curl http://localhost:8000/models

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Show temperature data","session_id":"test"}'
```

## Debugging

```python
# Enable logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Visualize graph
from graph_agent import compiled_graph
print(compiled_graph.get_graph())

# Check node execution
result = run_agent(...)
print(result["debug"])  # Shows latency per node
```

## Safety Features

✅ **Template-only SPARQL** - No arbitrary queries  
✅ **SELECT enforcement** - Blocks INSERT/DELETE/LOAD/etc  
✅ **FROM graph injection** - Always queries correct graph  
✅ **LIMIT clamping** - Max 500 rows  
✅ **Timeout protection** - 30s for SPARQL and LLM  
✅ **Error isolation** - Per-node error handling  

## Session Memory

Tracks across turns:
- `selected_property_uri` (e.g., temperature)
- `time_range` (e.g., {"start": "2020-01-01", "end": "2020-02-01"})
- `selected_feature_uri` (e.g., station ID)

Stored in Redis (or in-memory if Redis unavailable).

## Performance Tips

1. **Use Redis** for production (faster session retrieval)
2. **Enable caching** for common queries (list_properties, list_features)
3. **Monitor debug times** to identify bottlenecks
4. **Use local LLM (Ollama)** for faster responses
5. **Limit SPARQL rows** to reduce processing time

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `langgraph not found` | `pip install langgraph==0.0.26` |
| `Redis connection failed` | Falls back to in-memory (or install Redis) |
| `LLM timeout` | Increase `LLM_TIMEOUT` in .env |
| `SPARQL 403` | Check SPARQL_ENDPOINT and GRAPH_IRI |
| `Model not found` | Run `ollama pull <model-name>` |

## Production Checklist

- [ ] Set `REDIS_URL` for persistent sessions
- [ ] Configure `SAIA_API_KEY` for cloud LLM
- [ ] Increase `MAX_REQUESTS_PER_MINUTE` as needed
- [ ] Enable HTTPS
- [ ] Set CORS origins to specific domains
- [ ] Monitor `debug` field for performance
- [ ] Set up logging/monitoring
- [ ] Deploy with Docker Compose

## Next Steps

1. Test the workflow: `python test_graph.py`
2. Start the server: `uvicorn main:app --reload`
3. Open UI: http://localhost:8000/static/index.html
4. Monitor performance via `debug` field
5. Customize nodes in `graph_agent.py` as needed

---

**Documentation:**
- [README_LANGGRAPH.md](README_LANGGRAPH.md) - Full guide
- [MIGRATION.md](MIGRATION.md) - Migration from old code
- [WORKFLOW_VISUALIZATION.txt](WORKFLOW_VISUALIZATION.txt) - ASCII diagram
- [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md) - Summary
