# Climate Chat Agent Evaluation Framework

This folder contains the evaluation framework for testing and assessing the Climate Chat Agent's performance on the E-OBS gridded climate dataset (1950-2024).

## 📁 Files

- **`test_questions.json`**: 30 comprehensive test cases covering all 18 SPARQL query templates
- **`evaluate_agent.py`**: Python script to run evaluations and generate reports
- **`README.md`**: This file

## 🎯 Test Coverage

The test suite includes 30 questions designed to evaluate:

- **All 18 Query Templates**: Every SPARQL template is tested at least once
- **Multiple Categories**: 
  - Discovery (3 tests)
  - Statistics (7 tests)
  - Aggregation (6 tests)
  - Filtering (2 tests)
  - Spatial (4 tests)
  - Location (2 tests)
  - Trends (1 test)
  - Comparison (1 test)
  - Extremes (2 tests)
  - Long-term (1 test)
  - Exploration (1 test)

- **Difficulty Levels**:
  - Easy: 6 tests (basic queries)
  - Medium: 10 tests (moderate complexity)
  - Hard: 14 tests (complex queries, multiple conditions)

## 🚀 Usage

### Rule-Based Evaluation (Default)

Run all tests with rule-based metrics only:

```bash
python evaluation/evaluate_agent.py
```

This will:
1. Execute all 30 test questions
2. Check template matching accuracy
3. Verify query execution success
4. Display a summary report

### LLM-as-Judge Evaluation (Optional)

Run evaluation with LLM-as-judge to assess answer correctness:

```bash
python evaluation/evaluate_agent.py --llm-judge
```

This adds AI-powered evaluation that:
- Checks if the answer correctly reflects the evidence
- Verifies expected coverage items are addressed
- Detects unsupported claims or hallucinations
- Validates units, time periods, and locations
- Returns a label (correct/partially_correct/incorrect) and score (0.0-1.0)

**Note**: LLM-as-judge requires an LLM provider to be configured (OpenAI or Ollama). It adds ~2-5 seconds per test.

### Run All Tests with Report

```bash
python evaluation/evaluate_agent.py --report
```

### Run All Tests with LLM Judge and Save Report

```bash
python evaluation/evaluate_agent.py --report --llm-judge --output judge_report.json
```

### Run Specific Test by ID

```bash
python evaluation/evaluate_agent.py --question-id 5
```

### Run Tests by Category

```bash
python evaluation/evaluate_agent.py --category statistics
```

Available categories: `discovery`, `exploration`, `summary`, `statistics`, `extremes`, `aggregation`, `filtering`, `spatial`, `location`, `trends`, `comparison`, `long-term`

### Generate Detailed Report

```bash
python evaluation/evaluate_agent.py --report
```

### Save Report to File

```bash
python evaluation/evaluate_agent.py --output evaluation_report.json
```

## 📊 Evaluation Metrics

### Rule-Based Metrics (Always Included)

1. **Template Match Rate**: Percentage of questions where the correct SPARQL template was selected
2. **Success Rate**: Percentage of queries that executed without errors
3. **Result Coverage**: Number of tests that returned data
4. **Execution Time**: Average query execution time
5. **Category Performance**: Success rates broken down by question category
6. **Difficulty Performance**: Success rates by difficulty level

### LLM-as-Judge Metrics (When `--llm-judge` flag is used)

Additional AI-powered evaluation metrics:

7. **LLM Judge Score**: Average score from 0.0 to 1.0 across all evaluated answers
8. **Correctness Rate**: Percentage of answers judged as "correct"
9. **Judge Labels**:
   - **`correct`** (score ~1.0): Answer accurately reflects evidence, covers expected items, no unsupported claims
   - **`partially_correct`** (score ~0.5): Answer mostly correct but missing some coverage or has minor issues
   - **`incorrect`** (score ~0.0): Answer contradicts evidence, has major hallucinations, or misses critical information
   - **`judge_error`**: Judge failed to evaluate (LLM error or invalid JSON response)
   - **`not_evaluated`**: Query execution failed, so answer wasn't evaluated

10. **Missing Coverage**: List of expected coverage items not addressed in the answer
11. **Incorrect Claims**: List of unsupported or contradictory statements in the answer

### Judge Evaluation Criteria

The LLM judge evaluates based on:
- ✅ **Groundedness**: Every claim must be supported by the provided evidence
- ✅ **Completeness**: Expected coverage items should be addressed (explicitly or implicitly)
- ✅ **Accuracy**: Units, time periods, locations, and climate variables must be correct
- ✅ **Semantic Equivalence**: Exact wording not required, semantically equivalent answers are accepted
- ❌ **No External Knowledge**: Judge only uses provided evidence, not external knowledge
- ❌ **No Hallucinations**: Unsupported claims result in lower scores

## 📝 Sample Output

### Rule-Based Evaluation

```
################################################################################
# EVALUATION REPORT
# Generated: 2024-12-31T10:30:00
################################################################################

📊 OVERALL SUMMARY
  Total Tests: 30
  Template Match Rate: 93.3% (28/30)
  Success Rate: 90.0% (27/30)
  Tests with Results: 27
  Avg Execution Time: 2.451s

📁 BY CATEGORY
  DISCOVERY: 3/3 passed (100.0%), template match: 100.0%
  STATISTICS: 6/7 passed (85.7%), template match: 85.7%
  AGGREGATION: 5/6 passed (83.3%), template match: 100.0%
  ...

⚡ BY DIFFICULTY
  EASY: 6/6 passed (100.0%)
  MEDIUM: 9/10 passed (90.0%)
  HARD: 12/14 passed (85.7%)
```

### With LLM-as-Judge

```
================================================================================
🤖 LLM-AS-JUDGE MODE ENABLED
================================================================================

================================================================================
Test 1: What variables are available?
Expected template: list_properties
Category: discovery | Difficulty: easy
================================================================================

✓ Template Match: PASS
  Expected: list_properties
  Got: list_properties

✓ Execution: PASS
  Result count: 5
  Execution time: 14.349s

📝 Answer: Here are the available climate variables...

🤖 Running LLM-as-judge evaluation...
  Label: correct
  Score: 1.0
  Reason: Answer accurately lists all climate variables from evidence, includes counts, and matches...

################################################################################
# EVALUATION REPORT
# Generated: 2026-05-02T15:30:00
################################################################################

📊 OVERALL SUMMARY
  Total Tests: 30
  Template Match Rate: 93.3% (28/30)
  Success Rate: 90.0% (27/30)
  Tests with Results: 27
  Avg Execution Time: 2.451s

🤖 LLM-AS-JUDGE SUMMARY
  Average Score: 0.867
  Correctness Rate: 80.0%
  Correct: 24
  Partially Correct: 2
  Incorrect: 1
  Not Evaluated: 3

📁 BY CATEGORY
  DISCOVERY: 3/3 passed (100.0%), template match: 100.0%
  ...
```

## 🔍 Test Question Structure

Each test case in `test_questions.json` includes:

```json
{
  "id": 1,
  "question": "What climate variables are available?",
  "expected_template": "list_properties",
  "category": "discovery",
  "difficulty": "easy",
  "expected_coverage": ["All 5 climate variables"],
  "notes": "Basic discovery query to list available properties"
}
```

## 🛠️ Adding New Tests

To add new test questions:

1. Open `test_questions.json`
2. Add a new test case to the `test_cases` array:
   ```json
   {
     "id": 31,
     "question": "Your new question here",
     "expected_template": "appropriate_template_name",
     "category": "appropriate_category",
     "difficulty": "easy|medium|hard",
     "expected_coverage": ["Expected result description"],
     "notes": "Purpose of this test"
   }
   ```
3. Update the `total_questions` in metadata
4. Run evaluation to verify

## 📦 Dependencies

The evaluation script uses the agent's existing dependencies:
- `src/agent/graph_agent` - Main agent logic
- `src/agent/state` - Agent state management
- Standard library: `json`, `time`, `requests`, `datetime`, `pathlib`

## 🎓 Best Practices

1. **Run Before Deployment**: Always run the full evaluation suite before deploying changes
2. **Monitor Template Accuracy**: Template match rate should be >90%
3. **Check Execution Time**: Queries should complete in <10 seconds on average
4. **Review Failures**: Investigate any test failures to identify bugs or template issues
5. **Update Tests**: When adding new templates or features, add corresponding test cases

## 📈 Continuous Improvement

Use evaluation results to:
- Identify weak query templates
- Improve agent's template selection logic
- Optimize slow queries
- Expand test coverage for edge cases
- Track performance improvements over time

## 🐛 Troubleshooting

**No results returned**:
- Verify SPARQL endpoint is accessible
- Check `.env` configuration
- Ensure Virtuoso server is running

**Template mismatch**:
- Review agent's RAG context
- Check if question phrasing aligns with examples
- Update test question to be more specific

**Timeout errors**:
- Increase timeout in `src/query/sparql_client.py`
- Optimize query templates
- Check Virtuoso server load

## 📄 License

Part of the Climate Chat Agent project.
