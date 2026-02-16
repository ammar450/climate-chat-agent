# Climate Chat Agent - Security Architecture

## Overview

This document describes the secure architecture where the **frontend NEVER calls the SPARQL endpoint directly**. All SPARQL queries go through the FastAPI backend with comprehensive security controls.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│                    (static/index.html)                       │
│                                                              │
│  - Multi-chat interface                                      │
│  - Local storage for chat history                           │
│  - NO direct SPARQL access                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ POST /chat
                   │ POST /reset
                   │ GET /health
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│                      (main.py)                               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Rate Limiter                                        │   │
│  │  - 30 requests/min per session                       │   │
│  │  - In-memory tracking                                │   │
│  │  - Returns 429 if exceeded                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Cache Layer                                         │   │
│  │  - 15 min TTL                                        │   │
│  │  - Pre-cached: list_properties, list_features       │   │
│  │  - Instant responses for common queries             │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Agent (agent.py)                                    │   │
│  │  - Pattern-based intent detection                    │   │
│  │  - Session state management                          │   │
│  │  - Template selection                                │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SPARQL Client (sparql_client.py)                    │   │
│  │  ONLY component that calls SPARQL endpoint           │   │
│  │                                                       │   │
│  │  Security Controls:                                  │   │
│  │  ✓ SELECT queries only                               │   │
│  │  ✓ Block INSERT/DELETE/UPDATE/DROP                   │   │
│  │  ✓ Enforce FROM <graph> clause                       │   │
│  │  ✓ Enforce LIMIT ≤ 500, default 200                  │   │
│  │  ✓ 30 second timeout                                 │   │
│  │  ✓ Error handling & logging                          │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ SPARQL SELECT queries
                   │ (validated & secured)
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Virtuoso SPARQL Endpoint                        │
│   https://hyobs.webapps.nfdi4earth.de/sparql/              │
│                                                              │
│   Graph: http://hyobs.nfdi4earth.de/graph/climate...        │
└─────────────────────────────────────────────────────────────┘
```

## Security Layers

### Layer 1: Frontend Restrictions
- **No SPARQL endpoint URL exposed to frontend**
- Frontend only knows about `/chat`, `/reset`, `/health`
- All data flows through backend API
- Session ID generated client-side, validated server-side

### Layer 2: Rate Limiting
- Max 30 requests per minute per session ID
- In-memory tracking (resets on server restart)
- Returns HTTP 429 (Too Many Requests) when exceeded
- Configurable via `MAX_REQUESTS_PER_MINUTE` env var

### Layer 3: Query Validation (sparql_client.py)

#### Must Start with SELECT
```python
if not query_upper.startswith("SELECT"):
    raise SPARQLSecurityError("Only SELECT queries are allowed")
```

#### Block Dangerous Keywords
```python
DANGEROUS_KEYWORDS = [
    "INSERT", "DELETE", "LOAD", "CLEAR", "CREATE", 
    "DROP", "MOVE", "COPY", "ADD", "UPDATE"
]
```

#### Enforce Graph Scope
```python
# Ensures query includes FROM <graph_uri>
query = ensure_from_clause(query, GRAPH)
```

#### Enforce LIMIT
```python
# If LIMIT > 500: reduce to 500
# If no LIMIT: add LIMIT 200
query = enforce_limit(query)
```

#### Timeout Protection
```python
sparql.setTimeout(QUERY_TIMEOUT)  # Default: 30 seconds
```

### Layer 4: Template System
- All queries generated from safe templates
- No raw SPARQL from user input
- Parameters validated and escaped
- Templates defined in `query_templates.py`

### Layer 5: Caching
- Common queries cached for 15 minutes
- Reduces load on SPARQL endpoint
- Pre-cached at startup:
  - `list_properties`
  - `list_features`
- Cache key includes template name + params
- Thread-safe implementation

## Configuration

All security settings configurable via environment variables:

```bash
# Endpoint Configuration
SPARQL_ENDPOINT=https://hyobs.webapps.nfdi4earth.de/sparql/
GRAPH_IRI=http://hyobs.nfdi4earth.de/graph/climateobservations

# Query Limits
MAX_LIMIT=500              # Maximum rows per query
DEFAULT_LIMIT=200          # Default if no LIMIT specified
SPARQL_TIMEOUT=30          # Query timeout in seconds

# Performance
CACHE_TTL_MINUTES=15       # Cache time-to-live
MAX_REQUESTS_PER_MINUTE=30 # Rate limit per session
```

## Request Flow Example

### User asks: "What variables are available?"

1. **Frontend** (index.html)
   ```javascript
   fetch('/chat', {
     method: 'POST',
     body: JSON.stringify({
       message: "What variables are available?",
       session_id: "abc-123"
     })
   })
   ```

2. **Rate Limiter** (main.py)
   - Check: `_rate_limit_data["abc-123"]` 
   - Count requests in last minute
   - If < 30: proceed
   - If ≥ 30: return HTTP 429

3. **Cache Check** (main.py)
   ```python
   cache_key = "template:list_properties"
   cached = get_cached_query(cache_key)
   if cached:
       return cached  # Instant response!
   ```

4. **Agent Planning** (agent.py)
   - Detect intent: "list_properties"
   - Select template: "list_properties"
   - No parameters needed

5. **Template Rendering** (query_templates.py)
   ```python
   query = render_template("list_properties", {})
   ```

6. **Security Validation** (sparql_client.py)
   - ✓ Starts with SELECT
   - ✓ No dangerous keywords
   - ✓ Add FROM clause
   - ✓ Add LIMIT 200

7. **SPARQL Execution**
   ```sparql
   SELECT DISTINCT ?property ?label
   FROM <http://hyobs.nfdi4earth.de/graph/climateobservations>
   WHERE {
     ?obs sosa:observedProperty ?property .
     OPTIONAL { ?property rdfs:label ?label }
   }
   LIMIT 200
   ```

8. **Cache Result**
   ```python
   cache_query(cache_key, result)  # Cache for 15 min
   ```

9. **Format & Return**
   - Format results for display
   - Return to frontend
   - Frontend displays in chat

## Swapping Endpoints

To use a different SPARQL endpoint:

1. Update `.env`:
   ```bash
   SPARQL_ENDPOINT=https://your-endpoint.com/sparql/
   GRAPH_IRI=http://your-graph.com/data
   ```

2. Restart server:
   ```bash
   uvicorn main:app --reload
   ```

**That's it!** No code changes required.

## Monitoring & Debugging

### Health Check
```bash
curl http://localhost:8000/health
```

Returns:
```json
{
  "status": "healthy",
  "sparql": "ok"
}
```

### Debug Logs

Backend prints:
```
[STARTUP] Initializing Climate Chat Agent...
[CONFIG] SPARQL Endpoint: https://...
[CONFIG] Cache TTL: 15 minutes
[CONFIG] Rate Limit: 30 requests/minute
[CACHE HIT] template:list_properties
[SECURITY] Added default LIMIT 200
[SPARQL] Executing query against https://...
```

### Common Errors

**HTTP 429 - Rate Limit Exceeded**
```json
{
  "detail": "Rate limit exceeded. Maximum 30 requests per minute."
}
```
*Solution:* Wait 1 minute or increase `MAX_REQUESTS_PER_MINUTE`

**HTTP 403 - Security Violation**
```json
{
  "detail": "Security violation: Query contains forbidden keyword: DELETE"
}
```
*Solution:* Query attempted dangerous operation

**HTTP 500 - SPARQL Timeout**
```json
{
  "detail": "SPARQL query failed: timeout"
}
```
*Solution:* Increase `SPARQL_TIMEOUT` or simplify query

## Production Deployment Checklist

- [ ] Set `SPARQL_ENDPOINT` and `GRAPH_IRI` in environment
- [ ] Configure appropriate `MAX_REQUESTS_PER_MINUTE`
- [ ] Set `SPARQL_TIMEOUT` based on endpoint performance
- [ ] Adjust `CACHE_TTL_MINUTES` based on data update frequency
- [ ] Review `MAX_LIMIT` and `DEFAULT_LIMIT` for your use case
- [ ] Configure CORS in `main.py` to allow only your domain
- [ ] Add HTTPS/TLS in production
- [ ] Consider external cache (Redis) for multi-instance deployments
- [ ] Monitor rate limit violations
- [ ] Set up logging to file/service
- [ ] Add metrics/monitoring (Prometheus, etc.)

## Security Best Practices

1. ✅ **Never expose SPARQL endpoint URL to frontend**
2. ✅ **Always validate queries on backend**
3. ✅ **Use template system, not raw query construction**
4. ✅ **Enforce LIMIT on all non-aggregate queries**
5. ✅ **Set reasonable timeout values**
6. ✅ **Rate limit per session/user**
7. ✅ **Cache common queries**
8. ✅ **Log security violations**
9. ✅ **Use environment variables for configuration**
10. ✅ **Implement health checks**

---

**Version:** 2.0.0  
**Last Updated:** January 2026
