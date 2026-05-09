# API Reference

Complete API documentation for the Climate Chat Agent.

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### 1. Chat Endpoint (Primary Interface)

**POST** `/chat`

Send a natural language query and get a grounded answer.

**Request Body:**
```json
{
  "message": "What was the average temperature in Berlin in January 2020?"
}
```

**Response:**
```json
{
  "response": "Based on E-OBS data, the average temperature in Berlin (52.5°N, 13.4°E) during January 2020 was 3.2°C. This is above the long-term January average for this location.",
  "execution_time_ms": 1234,
  "metadata": {
    "template_used": "avg_property_time_location",
    "parameters": {
      "property": "air_temperature",
      "start_date": "2020-01-01",
      "end_date": "2020-01-31",
      "latitude": 52.5,
      "longitude": 13.4
    },
    "results_found": 31
  }
}
```

**Performance:**
- ⚡ **Cached queries:** < 100ms
- 🚀 **New queries:** 1-3 seconds (depends on LLM backend)
- 🌐 **SPARQL execution:** 200-800ms

**Error Responses:**

```json
{
  "error": "No data found for your query",
  "suggestion": "Try a different location or time period. E-OBS covers 1950-2024.",
  "execution_time_ms": 456
}
```

---

### 2. Web Interface (UI)

**GET** `/`

Returns the interactive chat web interface.

**Features:**
- Multi-session chat (like ChatGPT)
- Markdown rendering with syntax highlighting
- Chat history management
- Dark/light mode support
- Responsive design

**Access:**
```
http://localhost:8000
```

---

### 3. Health Check

**GET** `/health`

Check if the service is running and healthy.

**Response:**
```json
{
  "status": "ok",
  "llm_backend": "OpenAI",
  "sparql_endpoint": "https://obs.knowledgehub.nfdi4earth.de/sparql/",
  "cache_enabled": true
}
```

---

### 4. Metrics & Statistics

**GET** `/metrics`

Get system performance metrics.

**Response:**
```json
{
  "total_requests": 1234,
  "cache_hit_rate": 0.67,
  "average_response_time_ms": 1200,
  "uptime_seconds": 86400
}
```

---

## Rate Limiting

**Default Limits:**
- 100 requests per minute per IP
- 1000 requests per hour per IP

**Rate Limit Response:**
```json
{
  "error": "Rate limit exceeded",
  "retry_after_seconds": 60
}
```

**Configuration:**

Edit `.env`:
```bash
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000
```

---

## Caching

**Cache Configuration:**

```bash
# .env
CACHE_ENABLED=true
CACHE_TTL_MINUTES=60
```

**Cache Key Format:**
```
template:{template_name}:params:{param_hash}
```

**Cache Behavior:**
- ✅ Identical queries return cached results
- ✅ Cache expires after TTL
- ✅ Server restart clears cache
- ✅ Parameter changes invalidate cache

**When queries are cached:**
1. Same template (e.g., `avg_property_time`)
2. Same parameters (location, time, variable)
3. Within cache TTL window

---

## Query Examples by API

### Basic Property Queries

**List all available climate variables:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What variables are available?"}'
```

**Response:**
```json
{
  "response": "The E-OBS dataset includes 5 climate variables:\n1. Air temperature (TG)\n2. Maximum temperature (TX)\n3. Minimum temperature (TN)\n4. Precipitation (RR)\n5. Sea level pressure (PP)",
  "metadata": {
    "template_used": "list_properties",
    "results_found": 5
  }
}
```

---

### Time-Based Queries

**Get data for specific date:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Temperature on 2020-06-15"}'
```

**Get monthly average:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Average temperature in July 2019"}'
```

**Get yearly data:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Precipitation in 2018"}'
```

---

### Location-Based Queries

**Specific coordinates:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Temperature at 52.5°N 13.4°E on 2020-01-15"}'
```

**City name (enriched via Wikidata):**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Temperature in Paris yesterday"}'
```

**Bounding box (area query):**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Average temperature in Europe (40-60°N, 0-20°E) in January 2020"}'
```

---

### Statistical Queries

**Maximum value:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Highest temperature in 2020"}'
```

**Minimum value:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Lowest precipitation in Berlin last year"}'
```

**Count observations:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How many temperature observations are there?"}'
```

**Standard deviation:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Temperature variability in 2019"}'
```

---

### Advanced Queries

**Comparison queries:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Compare temperature in January 2020 vs January 2010"}'
```

**Vague queries (handled intelligently):**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about climate data"}'
```

**Response includes clarification:**
```json
{
  "response": "The E-OBS dataset contains 328 million climate observations from 1950-2024 covering Europe. I can help you find:\n- Temperature (daily, min, max)\n- Precipitation\n- Sea level pressure\n\nPlease ask about a specific variable, location, or time period.",
  "metadata": {
    "template_used": "vague_query_handler"
  }
}
```

---

## Error Handling

### Error Types

**1. No Data Found**
```json
{
  "error": "No data found for your query",
  "suggestion": "Try a different location or time period. E-OBS covers Europe from 1950-2024.",
  "execution_time_ms": 234
}
```

**2. Invalid Date Range**
```json
{
  "error": "Date out of range",
  "suggestion": "E-OBS dataset covers 1950-01-01 to 2024-12-31. Please specify dates within this range.",
  "execution_time_ms": 150
}
```

**3. Invalid Location**
```json
{
  "error": "Location not found",
  "suggestion": "E-OBS covers Europe (approximately 25°N-75°N, 25°W-45°E). Please check your coordinates.",
  "execution_time_ms": 180
}
```

**4. Query Timeout**
```json
{
  "error": "Query timeout",
  "suggestion": "Your query is too broad. Try narrowing down the time period or geographic area.",
  "execution_time_ms": 30000
}
```

**5. SPARQL Endpoint Unavailable**
```json
{
  "error": "SPARQL endpoint unavailable",
  "suggestion": "The knowledge graph service is temporarily unavailable. Please try again later.",
  "execution_time_ms": 5000
}
```

---

## Security Features

### Query Validation

**Allowed:**
- ✅ SELECT queries only
- ✅ Maximum LIMIT of 500
- ✅ Enforced FROM clause with specific graph
- ✅ Read-only operations

**Blocked:**
- ❌ INSERT, DELETE, UPDATE, DROP operations
- ❌ CLEAR, LOAD, or COPY operations
- ❌ Unbounded queries (must have LIMIT)
- ❌ Multi-graph queries

### Input Sanitization

All user inputs are:
1. Validated for type and format
2. Sanitized to prevent injection attacks
3. Processed through safe templates
4. Limited in scope and size

### SPARQL Protection

```python
# Example of security check
def validate_query(query_text):
    unsafe_keywords = ["INSERT", "DELETE", "DROP", "CLEAR", "LOAD"]
    for keyword in unsafe_keywords:
        if keyword in query_text.upper():
            raise SecurityError(f"Unsafe operation: {keyword}")
    
    if "LIMIT" not in query_text.upper():
        raise ValidationError("Query must include LIMIT clause")
    
    return True
```

---

## Response Format

### Standard Response

```json
{
  "response": "Human-readable answer",
  "execution_time_ms": 1234,
  "metadata": {
    "template_used": "template_name",
    "parameters": {
      "property": "air_temperature",
      "start_date": "2020-01-01",
      "end_date": "2020-01-31"
    },
    "results_found": 42,
    "cache_hit": true
  }
}
```

### Field Descriptions

- **response** (string): Natural language answer grounded in knowledge graph data
- **execution_time_ms** (integer): Total query execution time in milliseconds
- **metadata** (object): Query execution details
  - **template_used** (string): SPARQL template selected by the planner
  - **parameters** (object): Extracted query parameters
  - **results_found** (integer): Number of results from knowledge graph
  - **cache_hit** (boolean): Whether result came from cache

---

## Integration Examples

### Python Client

```python
import requests

def query_climate_data(question):
    response = requests.post(
        "http://localhost:8000/chat",
        json={"message": question},
        timeout=30
    )
    return response.json()

# Example usage
result = query_climate_data("What was the temperature in Berlin on 2020-06-15?")
print(result["response"])
print(f"Execution time: {result['execution_time_ms']}ms")
```

### JavaScript Client

```javascript
async function queryclimateData(question) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: question }),
  });
  return await response.json();
}

// Example usage
const result = await queryClimateData('Average precipitation in 2019');
console.log(result.response);
```

### cURL Examples

```bash
# Basic query
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Temperature in Paris yesterday"}'

# With verbose output
curl -v -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Precipitation last week"}'

# Save response to file
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Average temperature in 2020"}' \
  -o response.json
```

---

## Performance Optimization

### Query Optimization Tips

1. **Use specific dates instead of relative dates**
   - ✅ "Temperature on 2020-06-15"
   - ❌ "Temperature yesterday" (requires additional processing)

2. **Limit geographic scope**
   - ✅ "Temperature in Berlin"
   - ❌ "Temperature in all of Europe" (very broad)

3. **Specify exact variables**
   - ✅ "Air temperature in July 2020"
   - ❌ "Climate data for 2020" (vague)

4. **Use monthly/yearly aggregates for long periods**
   - ✅ "Average temperature in 2020"
   - ❌ "Show me daily temperature for all of 2020" (too many results)

### Cache Strategy

```bash
# High-traffic applications
CACHE_TTL_MINUTES=120

# Real-time applications
CACHE_TTL_MINUTES=5

# Static datasets
CACHE_TTL_MINUTES=1440  # 24 hours
```

---

## Support & Documentation

- **Main Documentation:** [README.md](README.md)
- **Setup Guide:** [SETUP.md](SETUP.md)
- **Development Guide:** [DEVELOPMENT.md](DEVELOPMENT.md)
- **Architecture Details:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Evaluation Framework:** [evaluation/README.md](evaluation/README.md)

---

[← Back to Main README](README.md) | [Development Guide →](DEVELOPMENT.md) | [Setup Guide →](SETUP.md)
