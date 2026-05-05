# LLM-as-Judge Evaluation - Implementation Summary

## Overview

Added an optional LLM-as-judge evaluation mode to complement the existing rule-based evaluation system. The judge uses the same LLM infrastructure as the main agent to assess answer correctness.

## Files Changed

### 1. `evaluation/evaluate_agent.py` ⭐ Main Changes

**New Features Added:**

- **`llm_judge_evaluate()` method** (lines ~45-170): Core judge function that sends structured prompts to LLM
- **Updated `__init__`**: Added `use_llm_judge` parameter
- **Updated `run_single_test()`**: Optionally calls judge after successful execution
- **Updated `generate_report()`**: Calculates and includes judge statistics
- **Updated `_print_report()`**: Displays judge metrics in summary
- **Updated `main()`**: Added `--llm-judge` command-line flag

**New Imports:**
```python
from src.llm.llm_client import chat, LLMError
```

### 2. `evaluation/README.md` 📚 Documentation

**Sections Added:**
- "LLM-as-Judge Evaluation (Optional)" in Usage section
- "LLM-as-Judge Metrics" in Evaluation Metrics section
- "Judge Evaluation Criteria" explaining how the judge works
- Updated sample output showing judge results

## How It Works

### 1. Command-Line Usage

```bash
# Rule-based evaluation only (default)
python evaluation/evaluate_agent.py --report

# With LLM-as-judge
python evaluation/evaluate_agent.py --report --llm-judge

# Save results with judge evaluation
python evaluation/evaluate_agent.py --llm-judge --output judge_report.json
```

### 2. Judge Prompt Structure

The judge receives:
- **User Question**: Original query
- **Expected Template**: What SPARQL template should be used
- **Actual Template**: What template was actually used
- **Expected Coverage**: List of items the answer should address
- **SPARQL Query**: Generated query (first 500 chars)
- **Evidence**: SPARQL results/evidence (first 800 chars)
- **Agent's Answer**: The final answer to evaluate

### 3. Judge Response Format

Returns strict JSON:
```json
{
  "label": "correct" | "partially_correct" | "incorrect",
  "score": 0.0-1.0,
  "reason": "Brief explanation (1-2 sentences)",
  "missing_coverage": ["coverage item 1", "coverage item 2"],
  "incorrect_claims": ["claim 1", "claim 2"]
}
```

### 4. Error Handling

- If judge fails (LLM error, invalid JSON, timeout): Returns `"label": "judge_error"`
- If query execution failed: Returns `"label": "not_evaluated"`
- Invalid label values automatically converted to `"judge_error"`
- Evaluation continues even if judge fails on individual tests

## Judge Evaluation Criteria

The LLM judge enforces these rules (via prompt):

1. ✅ **Groundedness**: Judge only based on provided evidence, no external knowledge
2. ✅ **No Hallucinations**: Do not reward unsupported claims
3. ✅ **Coverage Check**: Verify expected_coverage items are addressed
4. ✅ **Accuracy**: Units, time periods, locations, variables must be correct
5. ✅ **Semantic Equivalence**: Allow different wording if meaning is the same

## New Metrics in Reports

### Per-Test Metrics (when `--llm-judge` enabled)

Each test result now includes:
```python
{
  # Existing metrics
  "template_match": bool,
  "success": bool,
  "execution_time": float,
  
  # New LLM judge metrics
  "llm_judge_label": str,  # "correct" | "partially_correct" | "incorrect" | "judge_error" | "not_evaluated"
  "llm_judge_score": float,  # 0.0 to 1.0
  "llm_judge_reason": str,
  "llm_judge_missing_coverage": list,
  "llm_judge_incorrect_claims": list
}
```

### Aggregate Metrics in Report Summary

```python
{
  "summary": {
    # Existing metrics...
    "llm_judge": {
      "enabled": true,
      "correct_count": int,
      "partially_correct_count": int,
      "incorrect_count": int,
      "judge_error_count": int,
      "not_evaluated_count": int,
      "average_score": float,  # 0.0-1.0
      "correctness_rate": float  # percentage
    }
  }
}
```

## Example Judge Prompt (Abbreviated)

```
You are an expert evaluator for a climate data question-answering system.

Evaluate whether the agent's answer correctly addresses the user's question 
based on the provided evidence.

## Evaluation Criteria:
1. Correctness: Does the answer accurately reflect the evidence?
2. Completeness: Does it address all expected coverage points?
3. Accuracy: Are units, time periods, locations correct?
4. Groundedness: Is every claim supported by evidence?

## Important Rules:
- Judge ONLY based on provided evidence
- Do NOT reward unsupported claims
- Allow semantically equivalent answers
- Verify expected coverage items are addressed

**User Question**: What was the average temperature in 2020?
**Expected Coverage**: ["Temperature", "Average value", "Year 2020"]
**Evidence**: Temperature: mean=10.5°C, min=-5.2°C, max=28.3°C
**Agent's Answer**: In 2020, the average temperature was 10.5°C...

Return ONLY valid JSON with label, score, reason, missing_coverage, incorrect_claims.
```

## Example Output for One Test

```
================================================================================
Test 7: What was the average temperature in 2020?
Expected template: average_for_property_date_range
Category: statistics | Difficulty: medium
================================================================================

✓ Template Match: FAIL
  Expected: average_for_property_date_range
  Got: timeseries_statistics

✓ Execution: PASS
  Result count: 1
  Execution time: 18.234s

📝 Answer: In 2020, the average temperature was 10.5°C across...

🤖 Running LLM-as-judge evaluation...
  Label: correct
  Score: 1.0
  Reason: Answer accurately states the average temperature from evidence with correct unit and year.
```

**Interpretation**: 
- ❌ Template mismatch (used wrong template)
- ✅ Execution successful (query ran)
- ✅ Judge says answer is correct (despite wrong template, the answer is right)

This shows the value of LLM-as-judge: it can catch cases where the wrong template still produces a correct answer!

## Integration with Existing Infrastructure

**Reuses existing components:**
- `src.llm.llm_client.chat()` - same LLM client used by the agent
- Uses configured LLM provider (OpenAI or Ollama) from environment
- Same timeout and error handling patterns

**No new dependencies required** - everything uses existing imports.

## Performance Considerations

- Each LLM judge call adds ~2-5 seconds per test
- For 30 tests: adds ~60-150 seconds total
- Judge is optional - can be disabled for faster runs
- Judge only runs on successfully executed tests

## Future Enhancements

Possible improvements:
1. Add `--judge-provider` flag to use different LLM for judging (e.g., GPT-4 to judge GPT-3.5 answers)
2. Save judge reasoning to separate file for analysis
3. Add judge consensus mode (multiple judges vote)
4. Compare judge scores to human annotations
5. Fine-tune judge prompt based on error analysis

## Testing the Implementation

```bash
# Test on a single question
python evaluation/evaluate_agent.py --question-id 1 --llm-judge

# Test on a category
python evaluation/evaluate_agent.py --category discovery --llm-judge

# Full evaluation with report
python evaluation/evaluate_agent.py --report --llm-judge --output judge_results.json
```

Check the JSON output for:
- `llm_judge` section in summary
- Per-test `llm_judge_*` fields in detailed_results
- No crashes even if some judge evaluations fail

## Safety Features

1. **Graceful Degradation**: If judge fails, test still passes/fails based on rule-based metrics
2. **Error Isolation**: Judge error on one test doesn't stop evaluation of other tests
3. **JSON Validation**: Validates required fields before accepting judge response
4. **Label Validation**: Invalid labels converted to "judge_error"
5. **Timeout Protection**: LLM client has timeout configuration
6. **Non-blocking**: Judge is optional, existing workflows unaffected

---

**Implementation Date**: May 2, 2026  
**Author**: AI Assistant  
**Status**: ✅ Complete and Ready for Testing
