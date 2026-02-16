# RAG Implementation Summary

## What Was Added

### 1. Multi-LLM Support (`llm_client.py`)

**NEW FILE** - Unified interface for multiple LLM providers:

- **Ollama** (local): `http://localhost:11434/api/chat`
- **SAIA** (cloud): `https://chat-ai.academiccloud.de/v1/chat/completions` (OpenAI-compatible)

**Key Function:**
```python
def chat(messages: List[Dict], provider: str = None, model: str = None) -> str
```

**Configuration:**
```bash
LLM_PROVIDER=ollama|saia
OLLAMA_MODEL=llama3.2
SAIA_API_KEY=sk-proj-...
SAIA_MODEL=gpt-4
```

### 2. RAG Implementation (`agent.py`)

**UPDATED** - Added knowledge-graph RAG flow:

#### A. LLM Planner
```python
def plan_query_with_llm(user_message, session) -> Dict
```
- Sends question + session context to LLM
- LLM outputs strict JSON: `{"template": "...", "params": {...}}`
- Selects appropriate SPARQL template
- Falls back to fast mode if LLM fails

#### B. Context Builder
```python
def build_context_from_results(results, template_name, session) -> str
```
- Takes SPARQL query results
- Extracts key facts: values, stats, time ranges
- Creates compact context text (top 10 rows + summary)
- Template-specific formatting

#### C. LLM Explainer
```python
def explain_results(user_message, results, template_name, session) -> Tuple[str, str]
```
- Builds context from SPARQL results
- Sends to LLM with instruction: "Use ONLY facts from context"
- Returns grounded answer (no hallucinations)

### 3. Configuration Updates

**`.env.example`** - Added:
```bash
# LLM Provider
LLM_PROVIDER=ollama|saia
OLLAMA_URL=...
OLLAMA_MODEL=...
SAIA_URL=...
SAIA_API_KEY=...
SAIA_MODEL=...

# LLM Parameters
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1000
LLM_TIMEOUT=30

# RAG Mode
USE_RAG=true
ENABLE_FAST_MODE=false
```

**`main.py`** - Updated health check to test LLM provider

**`README.md`** - Added comprehensive RAG documentation

## RAG Flow Example

### User Question
"What was the average temperature in March 1950?"

### Step 1: LLM Planner
**Input:**
```
System: You are a SPARQL query planner...
User: What was the average temperature in March 1950?
```

**Output (JSON):**
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

### Step 2: SPARQL Query Execution
```sparql
SELECT (AVG(?value) as ?avg) ?unit
FROM <http://hyobs.nfdi4earth.de/graph/climateobservations>
WHERE {
  ?obs sosa:observedProperty <http://vocab.nerc.ac.uk/standard_name/air_temperature> ;
       sosa:resultTime ?time ;
       sosa:hasSimpleResult ?value .
  OPTIONAL { ?obs sosa:hasResult/qudt:unit ?unit }
  FILTER(?time >= "1950-03-01T00:00:00"^^xsd:dateTime && 
         ?time < "1950-04-01T00:00:00"^^xsd:dateTime)
}
LIMIT 200
```

**Results:**
```json
[
  {"avg": {"value": "15.3"}, "unit": {"value": "degC"}}
]
```

### Step 3: Context Building
```
Query type: average_for_property_date_range
Result count: 1
Property: Air Temperature
Time range: 1950-03-01T00:00:00 to 1950-04-01T00:00:00
Average value: 15.3 degC
```

### Step 4: LLM Explainer
**Input:**
```
System: Answer based ONLY on the provided context. Do NOT invent values.
User: What was the average temperature in March 1950?

CONTEXT:
Query type: average_for_property_date_range
Result count: 1
Property: Air Temperature
Time range: 1950-03-01T00:00:00 to 1950-04-01T00:00:00
Average value: 15.3 degC
```

**Output:**
"Based on the climate observations in the knowledge graph, the average air temperature in March 1950 was 15.3°C."

✅ **Grounded** - uses actual value from database  
❌ **No hallucination** - doesn't invent numbers

## Security Maintained

All existing security controls preserved:

- ✅ Only SELECT queries
- ✅ FROM <graph> enforced
- ✅ LIMIT ≤ 500, default 200
- ✅ No INSERT/DELETE/UPDATE/DROP
- ✅ Rate limiting (30/min)
- ✅ Caching (15 min TTL)
- ✅ Timeout protection (30s)

## Operating Modes

### Mode 1: Full RAG (Recommended)
```bash
USE_RAG=true
ENABLE_FAST_MODE=false
LLM_PROVIDER=ollama  # or saia
```
- LLM planner selects template
- SPARQL retrieves data
- LLM explainer generates grounded answer
- **Best for:** Natural conversation, complex questions

### Mode 2: Fast Mode (No LLM)
```bash
ENABLE_FAST_MODE=true
```
- Pattern matching selects template
- SPARQL retrieves data
- Returns formatted context
- **Best for:** Speed, simple queries

### Mode 3: Hybrid
```bash
USE_RAG=true
ENABLE_FAST_MODE=true  # Uses fast planner, LLM explainer
```
- Pattern matching selects template (fast)
- SPARQL retrieves data
- LLM explainer generates answer
- **Best for:** Balance of speed and natural language

## Testing

### 1. Test Ollama
```bash
# Start Ollama
ollama serve

# Pull model
ollama pull llama3.2

# Set in .env
LLM_PROVIDER=ollama

# Test
curl http://localhost:8000/health
```

### 2. Test SAIA
```bash
# Set in .env
LLM_PROVIDER=saia
SAIA_API_KEY=sk-proj-...

# Test
curl http://localhost:8000/health
```

### 3. Test RAG Flow
```bash
# Enable RAG
USE_RAG=true
ENABLE_FAST_MODE=false

# Ask question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What was the average temperature in 1950?", "session_id": "test123"}'
```

## Files Modified/Created

✅ **Created:**
- `llm_client.py` - Multi-LLM interface

✅ **Updated:**
- `agent.py` - Added RAG methods (planner, context builder, explainer)
- `main.py` - Updated health check for LLM
- `.env.example` - Added LLM configuration
- `README.md` - Added RAG documentation
- `ARCHITECTURE.md` - (existing, no changes needed)

## Migration Guide

### From Old System
1. Install new dependencies (already in requirements.txt)
2. Copy `.env.example` to `.env`
3. Set `LLM_PROVIDER=ollama` or `saia`
4. Set `USE_RAG=true` to enable RAG
5. Restart server

### Backwards Compatibility
- Fast mode still works (`ENABLE_FAST_MODE=true`)
- All existing templates work
- All existing security features active
- No breaking changes to API

---

**Version:** 3.0.0 - RAG Implementation  
**Date:** January 2026
