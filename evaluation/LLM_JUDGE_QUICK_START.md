# LLM-as-Judge Implementation - Quick Reference

## ✅ What Was Implemented

A complete LLM-as-judge evaluation system that:
- ✅ Complements (doesn't replace) existing rule-based evaluation
- ✅ Uses the existing LLM infrastructure (no new dependencies)
- ✅ Evaluates answer correctness, completeness, and groundedness
- ✅ Returns structured JSON with labels, scores, and reasoning
- ✅ Handles errors gracefully (doesn't crash evaluation)
- ✅ Provides detailed metrics in reports

## 📁 Files Modified

1. **`evaluation/evaluate_agent.py`** - Main evaluation script
   - Added `llm_judge_evaluate()` method
   - Added `--llm-judge` command-line flag
   - Updated metrics to include judge results
   
2. **`evaluation/README.md`** - Documentation
   - Added usage instructions for LLM judge
   - Documented judge metrics and labels
   - Added sample output examples

3. **`evaluation/LLM_JUDGE_IMPLEMENTATION.md`** - Implementation details (NEW)

4. **`evaluation/example_llm_judge.py`** - Example usage script (NEW)

## 🚀 How to Use

### Basic Usage

```bash
# Rule-based evaluation only (default - no change from before)
python evaluation/evaluate_agent.py --report

# WITH LLM-as-judge (NEW!)
python evaluation/evaluate_agent.py --report --llm-judge

# Save results to JSON
python evaluation/evaluate_agent.py --llm-judge --output judge_report.json
```

### Test Specific Questions

```bash
# Single test with judge
python evaluation/evaluate_agent.py --question-id 1 --llm-judge

# Category with judge
python evaluation/evaluate_agent.py --category statistics --llm-judge
```

### Programmatic Usage

```python
from evaluation.evaluate_agent import AgentEvaluator

# Create evaluator with judge enabled
evaluator = AgentEvaluator(use_llm_judge=True)

# Run tests
evaluator.run_all_tests()

# Generate report
report = evaluator.generate_report()

# Access judge metrics
print(report['summary']['llm_judge']['average_score'])
print(report['summary']['llm_judge']['correct_count'])
```

## 📊 Judge Output Format

### Per-Test Results

```python
{
  # Existing metrics (unchanged)
  "template_match": True,
  "success": True,
  "execution_time": 14.5,
  
  # NEW: Judge metrics
  "llm_judge_label": "correct",  # or "partially_correct", "incorrect", "judge_error", "not_evaluated"
  "llm_judge_score": 1.0,  # 0.0 to 1.0
  "llm_judge_reason": "Answer accurately lists all climate variables...",
  "llm_judge_missing_coverage": [],  # Empty if all covered
  "llm_judge_incorrect_claims": []   # Empty if none found
}
```

### Report Summary

```python
{
  "summary": {
    # Existing metrics...
    "template_match_rate": 93.3,
    "success_rate": 90.0,
    
    # NEW: Judge summary
    "llm_judge": {
      "enabled": true,
      "correct_count": 24,
      "partially_correct_count": 2,
      "incorrect_count": 1,
      "judge_error_count": 0,
      "not_evaluated_count": 3,
      "average_score": 0.867,
      "correctness_rate": 88.9
    }
  }
}
```

## 🎯 Judge Labels Explained

| Label | Score | Meaning |
|-------|-------|---------|
| `correct` | ~1.0 | Answer accurately reflects evidence, all coverage items addressed, no unsupported claims |
| `partially_correct` | ~0.5 | Mostly correct but missing some coverage or has minor inaccuracies |
| `incorrect` | ~0.0 | Major errors, contradicts evidence, or significant hallucinations |
| `judge_error` | 0.0 | Judge failed (LLM error, invalid JSON, timeout) |
| `not_evaluated` | 0.0 | Query execution failed, so answer wasn't judged |

## 🔍 Judge Evaluation Criteria

The judge evaluates based on:

1. **Correctness** - Does answer match the evidence?
2. **Completeness** - Are expected coverage items addressed?
3. **Accuracy** - Are units, dates, locations correct?
4. **Groundedness** - Are all claims supported by evidence?

**Important**: Judge uses ONLY provided evidence, not external knowledge!

## 📝 Example Evaluation Output

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
  Reason: Answer accurately states average temperature from evidence with correct unit and year.

################################################################################
# EVALUATION REPORT
################################################################################

📊 OVERALL SUMMARY
  Total Tests: 30
  Template Match Rate: 46.7% (14/30)
  Success Rate: 96.7% (29/30)
  Tests with Results: 28
  Avg Execution Time: 22.4s

🤖 LLM-AS-JUDGE SUMMARY
  Average Score: 0.867
  Correctness Rate: 80.0%
  Correct: 24
  Partially Correct: 2
  Incorrect: 1
  Not Evaluated: 3
```

## 🎨 The Judge Prompt

Here's the actual prompt sent to the LLM (abbreviated):

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
- Judge ONLY based on provided evidence, not external knowledge
- Do NOT reward unsupported claims or hallucinations
- Allow semantically equivalent answers (exact wording not required)
- Verify expected coverage items are addressed

## Input Information:
**User Question**: What was the average temperature in 2020?
**Expected Template**: average_for_property_date_range
**Actual Template**: timeseries_statistics
**Expected Coverage**: ["Temperature", "Average value", "Year 2020"]

**Evidence/Data**:
Temperature: mean=10.5°C, min=-5.2°C, max=28.3°C (n=365)

**Agent's Answer**:
In 2020, the average temperature was 10.5°C across...

## Your Evaluation:
Return ONLY valid JSON with:
{
  "label": "correct" | "partially_correct" | "incorrect",
  "score": 0.0-1.0,
  "reason": "Brief explanation",
  "missing_coverage": [],
  "incorrect_claims": []
}
```

## 🛡️ Safety Features

1. **Non-Breaking**: If judge fails, evaluation continues with rule-based metrics
2. **Error Isolation**: Judge error on one test doesn't affect others
3. **JSON Validation**: Validates response structure before accepting
4. **Graceful Degradation**: Returns "judge_error" label if anything fails
5. **Backwards Compatible**: Existing evaluation workflows unchanged

## ⚡ Performance

- Judge adds ~2-5 seconds per test
- For 30 tests: ~60-150 seconds additional time
- Only runs on successfully executed tests
- Can be disabled with no performance impact

## 🔧 Configuration

Uses existing LLM configuration from `.env`:

```bash
# LLM provider (used by judge)
LLM_PROVIDER=openai  # or ollama

# OpenAI config
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini

# Or Ollama config
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

No additional configuration needed!

## 📦 Dependencies

**None!** Uses existing dependencies:
- `src.llm.llm_client` - Already imported by agent
- Standard library only (json, time, etc.)

## 🧪 Testing the Implementation

```bash
# Quick test on one question
python evaluation/evaluate_agent.py --question-id 1 --llm-judge

# Test on discovery category (fast)
python evaluation/evaluate_agent.py --category discovery --llm-judge

# Full evaluation (slow - 30 tests)
python evaluation/evaluate_agent.py --report --llm-judge --output full_judge_report.json

# Run example script
python evaluation/example_llm_judge.py
```

## 💡 Use Cases

1. **Quality Assurance**: Verify answers are factually correct, not just syntactically valid
2. **Template Validation**: Discover when wrong template still produces good answers
3. **Hallucination Detection**: Find unsupported claims in answers
4. **Coverage Analysis**: Identify missing information in responses
5. **A/B Testing**: Compare different LLM models or prompt strategies

## 📈 Interpreting Results

**High template match + Low judge score** → Agent using right queries but poor explanation
**Low template match + High judge score** → Agent compensating with different approach
**High success rate + Low judge score** → Queries work but answers have issues
**Low success rate + Not evaluated** → Need to fix query execution first

## 🎓 Next Steps

After implementation:
1. Run baseline evaluation: `python evaluation/evaluate_agent.py --report --llm-judge --output baseline_judge.json`
2. Analyze judge reasoning for failed cases
3. Compare judge scores across categories
4. Use judge feedback to improve prompts
5. Track judge metrics over time

---

**Status**: ✅ Complete and Ready to Use  
**Date**: May 2, 2026  
**Backward Compatible**: Yes - all existing features unchanged  
**Breaking Changes**: None
