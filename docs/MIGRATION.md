# LangGraph Migration Guide

## What Changed

### Before (Old Architecture)
- Simple agent with `plan_query()` and `explain_results()` methods
- Direct function calls in `/chat` endpoint
- Manual session state management
- Linear execution flow

### After (LangGraph Architecture)
- **Stateful workflow** with typed state (`AgentState`)
- **Multiple nodes** for each processing stage
- **Conditional routing** (followup vs. main execution path)
- **Session memory** (Redis or in-memory fallback)
- **Built-in debugging** (latency tracking per node)

## Installation

```bash
# Install new dependencies
pip install -r requirements.txt

# Optional: Start Redis (for persistent session memory)
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:7-alpine
```

## Configuration

Add to `.env`:

```bash
# Optional: Redis URL (falls back to in-memory if not set)
REDIS_URL=redis://localhost:6379/0
```

## Code Changes

### main.py
The `/chat` endpoint now calls `run_agent()` instead of the old agent methods:

```python
# OLD
plan = agent.plan_query(request.message, session, model=request.model)
# ... manual SPARQL execution ...
answer, context = agent.explain_results(...)

# NEW
result = run_agent(
    session_id=request.session_id,
    user_message=request.message,
    history=request.history or [],
    model=request.model
)
```

### graph_agent.py (New File)
Contains the entire LangGraph workflow:

**Nodes:**
1. `load_memory_node` - Restore session state
2. `resolve_node` - Extract property/time/feature
3. `plan_node` - LLM planner (JSON output)
4. `route_node` - Conditional routing
5. `followup_node` - Handle follow-up questions
6. `build_query_node` - Render SPARQL template
7. `execute_sparql_node` - Execute query
8. `format_evidence_node` - Create evidence text
9. `explain_node` - LLM explainer
10. `save_memory_node` - Persist session state

**Edges:**
```
load_memory → resolve → plan → route
                                 ├─→ followup → save_memory → END
                                 └─→ build_query → execute → format → explain → save_memory → END
```

## Benefits

### 1. Observable Execution
Every node tracks latency:
```json
{
  "debug": {
    "memory_loaded": true,
    "resolve_time": 0.003,
    "plan_time": 1.245,
    "build_query_time": 0.012,
    "execute_time": 0.456,
    "format_time": 0.008,
    "explain_time": 1.123,
    "memory_saved": true,
    "row_count": 150
  }
}
```

### 2. Conditional Routing
Automatically handles follow-up questions:
```
User: "Show temperature data"
Agent: "Which location would you like?"  ← Followup path
```

### 3. Session Memory
Tracks context across turns:
- `selected_property_uri`
- `selected_feature_uri`
- `time_range`

### 4. Production-Ready
- **Redis support** for distributed sessions
- **Fallback to in-memory** if Redis unavailable
- **Error isolation** per node
- **Graceful degradation** (LLM fails → return evidence)

## Testing

### Test the new workflow:

```bash
# Start server
uvicorn main:app --reload

# Test in Python
import requests

response = requests.post("http://localhost:8000/chat", json={
    "message": "What variables are available?",
    "session_id": "test123",
    "model": "ollama:llama3.2"
})

print(response.json())
```

### Expected response:
```json
{
  "answer": "Here are the available climate variables...",
  "context": "Query type: list_properties\nResult count: 4\n...",
  "sparql": "SELECT ?property ?label WHERE { ... }",
  "rows": [...],
  "used_template": "list_properties"
}
```

## Troubleshooting

### Import Error: `langgraph not found`
```bash
pip install langgraph langchain-core
```

### Redis Connection Failed
The system automatically falls back to in-memory storage. To use Redis:
```bash
# Install Redis
pip install redis

# Start Redis server
redis-server

# Or Docker
docker run -d -p 6379:6379 redis
```

### LLM Timeout
Increase timeout in `.env`:
```bash
LLM_TIMEOUT=60  # seconds
```

## Debugging

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

View LangGraph execution:
```python
from graph_agent import compiled_graph

# Visualize graph
compiled_graph.get_graph().print_ascii()
```

## Rollback (If Needed)

If you need to rollback to the old architecture:

1. Restore old `main.py`:
```bash
git checkout HEAD~1 main.py
```

2. Uninstall LangGraph:
```bash
pip uninstall langgraph langchain-core
```

3. Use old agent methods:
```python
from agent import agent
plan = agent.plan_query(...)
answer, context = agent.explain_results(...)
```

## Next Steps

1. **Monitor performance**: Check `debug` field for bottlenecks
2. **Tune LLM prompts**: Edit prompts in `graph_agent.py` nodes
3. **Add new templates**: Extend `query_templates.py`
4. **Custom nodes**: Add domain-specific processing nodes
5. **Deploy to production**: Use Redis + cloud LLM (SAIA)

## Questions?

See [README_LANGGRAPH.md](README_LANGGRAPH.md) for full documentation.
