# Quick Test Guide for New Features

## Feature A: Date Filtering by Date

### Test Cases

#### 1. Exact Date Within Range (1950-1951)
**Input:** "Show temperature data for 1950-06-15"
**Expected:**
- ✅ Returns data for exactly 1950-06-15
- ✅ No date availability message

#### 2. Date Before Range
**Input:** "What was the temperature on 1940-01-01?"
**Expected:**
- ✅ Message: "Data for 1940-01-01 is not available. Showing data for 1950-01-01 instead (earliest available date)."
- ✅ Returns data for 1950-01-01

#### 3. Date After Range
**Input:** "Show me data for 2023-05-20"
**Expected:**
- ✅ Message: "Data for 2023-05-20 is not available. Showing data for 1951-12-31 instead (latest available date)."
- ✅ Returns data for 1951-12-31

#### 4. Natural Language Still Works
**Input:** "What was the temperature in 1950?"
**Expected:**
- ✅ Returns data for entire year 1950
- ✅ No changes to existing functionality

---

## Feature B: Two-Level Response

### Test Cases

#### 1. Basic Query - Check Layman Response
**Input:** "What's the average temperature in 1950?"
**Expected Layman Response (visible by default):**
```
🌡️ Temperature Data

Quick Summary:
The average temperature during 1950 was XX.X°C
(Based on X,XXX measurements)

💡 In everyday terms: [friendly comparison]
```

#### 2. Technical Details Button Appears
**Expected:**
- ✅ "🔧 Show Technical Details" button visible below layman response
- ✅ Button is collapsed by default
- ✅ Arrow indicator (▶) present

#### 3. Expand Technical Details
**Action:** Click "🔧 Show Technical Details"
**Expected:**
- ✅ Section expands smoothly
- ✅ Arrow rotates to ▼
- ✅ Shows formatted technical information

#### 4. Technical Content Includes:
**Check for these sections:**
```
✅ === TECHNICAL DETAILS ===
✅ Query Template: [template_name]
✅ Response Format: layman/technical
✅ Property: [property_name]
✅ Property URI: [full_uri]
✅ Time Range: [start] to [end]
✅ Evidence Summary: [truncated evidence]

✅ Debug Information:
   ⏱ Validation: X.XXXs
   ⏱ Resolution: X.XXXs
   ⏱ Planning: X.XXXs
   ⏱ Query Build: X.XXXs
   ⏱ Execution: X.XXXs
   ⏱ Format: X.XXXs
   ⏱ Explanation: X.XXXs
   📊 Rows Retrieved: XXX
   🤖 LLM Provider: [provider]
   🤖 LLM Model: [model]
   💾 Session Memory: Loaded/Not found
   💾 Session Save: Success/Failed

✅ SPARQL Query:
   [formatted query]
```

#### 5. Collapse Technical Details
**Action:** Click "🔧 Show Technical Details" again
**Expected:**
- ✅ Section collapses smoothly
- ✅ Arrow rotates back to ▶

#### 6. Persistence Test
**Actions:**
1. Send a message (technical details should be visible in button)
2. Switch to another chat or create new chat
3. Return to original chat
**Expected:**
- ✅ Technical details button still present
- ✅ Can expand to see same technical details
- ✅ Content restored from localStorage

---

## Combined Feature Test

### Test Date Filtering with Technical Details

**Input:** "Show data for 2025-01-01"
**Expected:**

**Layman Response:**
```
Data for 2025-01-01 is not available. Showing data for 1951-12-31 instead (latest available date).

[Climate data results...]
```

**Technical Details (when expanded):**
```
=== TECHNICAL DETAILS ===
[Full technical breakdown with debug info]
Time Range: 1951-12-31T00:00:00 to 1952-01-01T00:00:00
[All timing and debug information]
```

---

## Visual Checks

### UI Elements to Verify

#### Dark Theme (Default)
- ✅ Technical details button has good contrast
- ✅ Hover effect visible on button
- ✅ Expanded content readable with monospace font
- ✅ Border and background colors appropriate

#### Light Theme
**Action:** Click theme toggle (🌙/☀️)
**Expected:**
- ✅ All text remains readable
- ✅ Technical details section adapts to light theme
- ✅ Colors transition smoothly

#### Responsive Design
**Test on different screen sizes:**
- ✅ Desktop: Technical details fit within message width
- ✅ Mobile: Content scrolls horizontally if needed
- ✅ Technical content doesn't break layout

---

## Error Handling Tests

### Test 1: Invalid Date Format
**Input:** "Show data for not-a-date"
**Expected:**
- ✅ Fallback to general query processing
- ✅ Or appropriate error message

### Test 2: LLM Failure
**Action:** Stop Ollama/disconnect LLM
**Input:** Any query
**Expected:**
- ✅ Fallback layman response with evidence summary
- ✅ Technical details show error information
- ✅ Error: [error message] in technical section

---

## Performance Checks

### Timing Expectations
**Typical query (1950 temperature):**
- ⏱ Validation: < 0.050s
- ⏱ Resolution: < 0.100s
- ⏱ Planning: < 0.500s (LLM dependent)
- ⏱ Query Build: < 0.010s
- ⏱ Execution: 0.5-3.0s (SPARQL dependent)
- ⏱ Format: < 0.100s
- ⏱ Explanation: < 0.500s (LLM dependent)

**Total Response Time:** Typically 1-5 seconds

### Memory Usage
- ✅ Technical details add ~2-5KB per message
- ✅ Chat history remains performant with 50+ messages

---

## Browser Console Tests

### Check for JavaScript Errors
**Action:** Open browser console (F12)
**Expected:**
- ✅ No console errors when sending messages
- ✅ No errors when expanding/collapsing technical details
- ✅ No errors when switching themes
- ✅ No errors when loading saved chats

### Network Requests
**Check /chat endpoint response:**
```json
{
  "answer": "Layman-friendly response...",
  "technical_details": "=== TECHNICAL DETAILS ===...",
  "context": "Evidence summary...",
  "sparql": "SELECT ...",
  "rows": [...],
  "used_template": "template_name"
}
```

---

## Backend Tests (Optional)

### Python Unit Tests
**Test TimeParser.parse_specific_date():**
```python
# Test exact date in range
result = TimeParser.parse_specific_date("1950-06-15", strict=True)
assert result[2] is None  # No availability message

# Test date before range
result = TimeParser.parse_specific_date("1940-01-01", strict=True)
assert "1950-01-01" in result[2]  # Should mention earliest date

# Test date after range
result = TimeParser.parse_specific_date("2023-05-20", strict=True)
assert "1951-12-31" in result[2]  # Should mention latest date
```

### Agent State Tests
```python
# Verify technical_details is populated
result = run_agent(session_id="test", user_message="Temperature in 1950?")
assert "technical_details" in result
assert "=== TECHNICAL DETAILS ===" in result["technical_details"]
assert "Debug Information" in result["technical_details"]
```

---

## Acceptance Criteria Checklist

### Feature A: Date Filtering ✓
- [x] User can request specific date (YYYY-MM-DD)
- [x] System finds nearest available date if exact date doesn't exist
- [x] Clear message tells user when alternative date is used
- [x] Message format: "Data for [requested] is not available. Showing data for [available] instead."
- [x] Date format validation works

### Feature B: Two-Level Response ✓
- [x] Layman-friendly response shown first (always visible)
- [x] Technical details hidden by default
- [x] "Show Technical Details" button present
- [x] Button expands/collapses on click
- [x] Technical details include:
  - [x] Query information
  - [x] Debug timings
  - [x] Row counts
  - [x] LLM provider/model
  - [x] SPARQL query
  - [x] Error information (if any)
- [x] Technical details persist in chat history
- [x] Responsive design works
- [x] Theme compatibility (dark/light)

---

## Known Limitations

1. **Date Parsing:**
   - Only supports YYYY-MM-DD format for specific dates
   - Other formats (MM/DD/YYYY, etc.) fall back to general parsing

2. **Technical Details:**
   - SPARQL query truncated to 1000 chars if very long
   - Evidence summary truncated to 500 chars

3. **Performance:**
   - Technical details generation adds ~50-100ms per query
   - Not significant but measurable

---

## Troubleshooting

### Issue: Technical Details Not Showing
**Check:**
1. Browser console for JavaScript errors
2. `/chat` endpoint response includes `technical_details` field
3. CSS loaded correctly (check in browser dev tools)

### Issue: Date Message Not Appearing
**Check:**
1. Date format is exactly YYYY-MM-DD
2. Date is outside 1950-1951 range
3. Console logs in backend show date parsing

### Issue: Layout Broken
**Check:**
1. CSS file loaded without errors
2. Browser cache cleared
3. Theme toggle working correctly

---

## Success Metrics

**Feature A - Date Filtering:**
- ✅ 100% of specific dates (YYYY-MM-DD) are processed correctly
- ✅ Nearest date found within 1 second
- ✅ User message clear and helpful

**Feature B - Two-Level Response:**
- ✅ Layman response always generated first
- ✅ Technical details generated for 100% of queries
- ✅ UI loads and renders without errors
- ✅ Performance impact < 100ms
- ✅ Chat history persistence works
