Show me detailed statistical analysis of air temperature for 1950 including mean, standard deviation, variance, and distribution metricsShow me detailed statistical analysis of air temperature for 1950 including mean, standard deviation, variance, and distribution metrics# Vague Query Handling Improvements

## Overview
Enhanced the climate chat agent to intelligently handle vague, ambiguous, and general climate queries that previously caused errors.

## Improvements Implemented

### 1. Default Variable Selection for Vague Queries
**Problem**: Queries like "climate in 1950" or "weather overview" without specific variables caused errors or incomplete responses.

**Solution**: 
- Added new `all_properties_summary` SPARQL template that retrieves statistics for ALL 4 standard climate properties
- Template includes: avg, min, max, count for each property (temperature, humidity, precipitation, wind)
- Agent automatically detects vague queries using phrase patterns

**Supported Vague Query Phrases**:
- "climate", "weather", "climate data", "weather data"
- "overview", "summary", "general", "all variables"
- "what happened", "conditions", "climate conditions"

**Example Queries**:
```
✅ "Show me climate data for 1950"
✅ "Weather overview for 1951"
✅ "What was the climate like in 1950?"
✅ "Explain 1950 climate simply"
✅ "General climate conditions"
```

### 2. Enhanced Year Detection
**Problem**: Year mentions in natural phrases like "climate data for 1949" were not detected, causing year validation to fail.

**Solution**: 
- Expanded `extract_year_update()` method in TimeParser with comprehensive regex patterns
- Now detects years in ANY context:
  - "for 1949", "in 1960", "during 1950"
  - "climate data for 1949"
  - "weather in 1960"
  - "show me 1951"
  - Standalone 4-digit years (1950, 1951, etc.)

**Pattern Coverage**:
```python
patterns = [
    r'(?:for|from|in|during|about|year|use|set|show|data for|climate for|weather in|now show|what about)\s+(\d{4})',
    r'(\d{4})\s+(?:data|climate|weather|observations)',
    r'year\s+(\d{4})',
    r'\b(1\d{3}|20\d{2})\b'  # Any year 1000-2099 standalone
]
```

**Example Queries**:
```
✅ "climate data for 1949" → Detects 1949, validates against 1950-1951 range
✅ "weather in 1960" → Detects 1960, shows helpful error with suggestion
✅ "show 1951" → Detects 1951, sets time range
✅ "data from 1950" → Detects 1950, proceeds with query
```

### 3. Fallback Summaries for Simple Queries
**Problem**: Simple overview queries like "Explain 1950 climate simply" didn't provide comprehensive summaries.

**Solution**:
- Enhanced `plan_node` with fast-path routing for overview queries
- Automatically uses `all_properties_summary` template for:
  - Queries with "explain", "overview", "summary", "simply"
  - Vague queries flagged by resolve_node
  - General climate questions without specific property keywords
- Defaults to full 1950-1951 range if no time specified

**Fast Path Detection**:
```python
if state.get("debug", {}).get("vague_query") or any(phrase in msg_lower for phrase in [
    "explain", "overview", "summary", "simply", "general climate", "all data",
    "what happened", "climate conditions", "weather conditions"
]):
    # Use all_properties_summary with time range
```

**Example Queries**:
```
✅ "Explain 1950 climate simply" → All properties summary with layman format
✅ "Climate overview for 1951" → All 4 variables with statistics
✅ "What happened in 1950?" → Comprehensive climate summary
✅ "General climate conditions" → Full 1950-1951 summary with all variables
```

### 4. Expanded Date Pattern Matching
**Problem**: Limited date pattern recognition missed many natural language variations.

**Solution**:
- Already handles: "in YYYY", "between YYYY and YYYY", "from YYYY to YYYY", "Month YYYY"
- Enhanced with aggressive year extraction for ANY 4-digit year mention
- Strict validation still applies (1950-1951 only) with helpful suggestions

**Validation Flow**:
1. Extract year from text using comprehensive patterns
2. If year outside 1950-1951, raise DateValidationError
3. Provide helpful error message with suggested alternatives
4. Suggest valid years (1950 or 1951) in error response

## Technical Implementation

### New Template: all_properties_summary
```sparql
SELECT ?property 
       (AVG(?value) AS ?avg_value) 
       (MIN(?value) AS ?min_value) 
       (MAX(?value) AS ?max_value) 
       (COUNT(?value) AS ?count)
       (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty ?property ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL { ?result qudt:unit ?unit }
  FILTER (?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
}
GROUP BY ?property
ORDER BY ?property
```

### Resolve Node Enhancement
```python
# Detect vague climate queries
vague_query_phrases = [
    "climate", "weather", "climate data", "weather data",
    "overview", "summary", "general", "all variables",
    "what happened", "conditions", "climate conditions"
]

is_vague_query = False
for phrase in vague_query_phrases:
    if phrase in msg_lower:
        # Check if it's NOT followed by specific property keywords
        specific_keywords = ["temperature", "humidity", "precipitation", "wind", "pressure"]
        has_specific = any(kw in msg_lower for kw in specific_keywords)
        if not has_specific:
            is_vague_query = True
            state["debug"]["vague_query"] = True
            break
```

### Evidence Formatting
```python
if template_name == "all_properties_summary":
    evidence_parts.append("Climate Overview (All Variables):")
    for row in rows:
        property_uri = row.get("property", {}).get("value", "Unknown")
        prop_name = property_resolver.get_property_display_name(property_uri)
        avg_val = row.get("avg_value", {}).get("value", "N/A")
        min_val = row.get("min_value", {}).get("value", "N/A")
        max_val = row.get("max_value", {}).get("value", "N/A")
        count = row.get("count", {}).get("value", "N/A")
        unit = row.get("unit", {}).get("value", "")
        
        evidence_parts.append(f"  {prop_name}: avg={avg_val}, range={min_val}-{max_val} {unit} (n={count})")
```

## Testing Examples

### Vague Queries (Now Work!)
```
User: "Show me climate data for 1950"
→ Returns all 4 properties with statistics

User: "Weather overview"
→ Returns full 1950-1951 summary for all variables

User: "Explain climate simply"
→ Uses layman format + all properties summary
```

### Year Detection (Now Robust!)
```
User: "climate data for 1949"
→ Detects 1949, shows error: "Data only available for 1950-1951. Try: Show climate data for 1950"

User: "weather in 1960"
→ Detects 1960, suggests valid alternatives

User: "show 1951"
→ Detects 1951, sets time range, proceeds
```

### Simple Overviews (Now Comprehensive!)
```
User: "Explain 1950 climate simply"
→ All properties summary in layman terms with emojis

User: "What happened in 1951?"
→ Overview of all climate variables for 1951
```

### Range Queries (Already Worked, Still Work!)
```
User: "Climate from 1950 to 1951"
→ All properties for full range

User: "January 1950 weather"
→ All properties for January 1950
```

## Error Handling

### Invalid Years (Clear Feedback)
```
User: "climate in 1949"
Response: "❌ Sorry, data is only available for years 1950 and 1951.
You asked about 1949, which is outside the available range.

**Suggestion:** Show climate data for 1950"
```

### Ambiguous Queries (Intelligent Defaults)
```
User: "climate"
→ Assumes all properties + full 1950-1951 range
→ Returns comprehensive overview
```

## Benefits

1. **No More Errors**: Vague queries no longer cause NoneType or subscript errors
2. **Better UX**: Users get helpful responses even with imprecise questions
3. **Comprehensive**: Overview queries show all available climate variables
4. **Robust Year Detection**: ANY year mention is detected and validated
5. **Smart Defaults**: System assumes sensible defaults for incomplete queries

## Files Modified

1. **src/query/query_templates.py**
   - Added `all_properties_summary` template

2. **src/parsers/time_parser.py**
   - Enhanced `extract_year_update()` with comprehensive patterns

3. **src/agent/graph_agent.py**
   - Enhanced `resolve_node` with vague query detection
   - Updated `plan_node` with fast-path for overview queries
   - Added evidence formatting for all_properties_summary
   - Updated LLM prompts to mention new template

## Performance

- Fast-path routing skips LLM for common patterns (instant response)
- All-properties query is efficient (single SPARQL with GROUP BY)
- No performance degradation for specific queries
- Improved response time for vague queries (direct template vs. LLM planning)

## Next Steps

Consider adding:
1. Multi-year comparative analysis (e.g., "compare 1950 vs 1951")
2. Seasonal summaries (e.g., "winter 1950 climate")
3. Anomaly detection (e.g., "unusual weather in 1950")
4. Location-aware summaries (e.g., "climate in region X")
