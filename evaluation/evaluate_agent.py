"""
Climate Chat Agent Evaluation Framework

This script evaluates the agent's performance by:
1. Running predefined test questions
2. Checking if correct SPARQL templates are used
3. Verifying query execution and results
4. (Optional) Using LLM-as-judge to evaluate answer correctness
5. Generating evaluation reports

Usage:
    python evaluate_agent.py                    # Run all tests (rule-based only)
    python evaluate_agent.py --question-id 5    # Run specific test
    python evaluate_agent.py --category summary # Run category tests
    python evaluate_agent.py --report           # Generate detailed report
    python evaluate_agent.py --report --llm-judge  # Include LLM-as-judge evaluation
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.graph_agent import run_agent
from src.llm.llm_client import chat, LLMError


class AgentEvaluator:
    """Evaluates agent performance on test questions."""
    
    def __init__(self, test_file: str = "evaluation/test_questions.json", use_llm_judge: bool = False):
        """
        Initialize evaluator with test questions.
        
        Args:
            test_file: Path to test questions JSON file
            use_llm_judge: Whether to use LLM-as-judge for evaluation
        """
        self.test_file = test_file
        self.tests = self.load_tests()
        self.results = []
        self.use_llm_judge = use_llm_judge
        
    def load_tests(self) -> Dict:
        """Load test questions from JSON file."""
        with open(self.test_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def llm_judge_evaluate(
        self,
        question: str,
        expected_template: str,
        expected_coverage: List[str],
        final_answer: str,
        sparql_query: str,
        evidence: str,
        actual_template: str
    ) -> Dict[str, Any]:
        """
        Use LLM-as-judge to evaluate answer correctness.
        
        Args:
            question: Original user question
            expected_template: Expected SPARQL template
            expected_coverage: List of expected coverage items
            final_answer: Agent's final answer
            sparql_query: Generated SPARQL query
            evidence: Evidence/results from SPARQL execution
            actual_template: Actually used template
            
        Returns:
            Dict with label, score, reason, missing_coverage, incorrect_claims
            Returns judge_error label if evaluation fails
        """
        judge_prompt = f"""You are an expert evaluator for a climate data question-answering system.

Your task is to evaluate whether the agent's answer correctly addresses the user's question based on the provided evidence.

## Evaluation Criteria:

1. **Correctness**: Does the answer accurately reflect the evidence/data?
2. **Completeness**: Does the answer address all expected coverage points?
3. **Accuracy**: Are units, time periods, locations, and variables correct?
4. **Groundedness**: Is every claim supported by the evidence? (No hallucinations)

## Important Rules:

- Judge ONLY based on the provided evidence, not external knowledge
- Do NOT reward unsupported claims or hallucinated information
- Allow semantically equivalent answers (exact wording not required)
- Check that expected coverage items are addressed (explicitly or implicitly)
- Verify units, time periods, locations, climate variables are correct
- If the answer contradicts the evidence, mark as incorrect

## Input Information:

**User Question**: {question}

**Expected Template**: {expected_template}
**Actual Template**: {actual_template}

**Expected Coverage**: {json.dumps(expected_coverage, indent=2)}

**SPARQL Query**:
```sparql
{sparql_query[:500]}{'...' if len(sparql_query) > 500 else ''}
```

**Evidence/Data**:
```
{evidence[:800]}{'...' if len(evidence) > 800 else ''}
```

**Agent's Answer**:
```
{final_answer}
```

## Your Evaluation:

Return a JSON object with:
- "label": "correct" | "partially_correct" | "incorrect"
- "score": 0.0-1.0 (0.0=incorrect, 0.5=partially correct, 1.0=fully correct)
- "reason": Brief explanation (1-2 sentences)
- "missing_coverage": List of coverage items not addressed (empty if all covered)
- "incorrect_claims": List of incorrect or unsupported claims (empty if none)

**Return ONLY valid JSON, no markdown, no explanations outside JSON:**"""

        system_prompt = """You are a precise evaluator. Return only valid JSON matching the specified schema. Be strict about groundedness - do not reward unsupported claims."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": judge_prompt}
        ]
        
        try:
            # Use existing LLM infrastructure
            response = chat(messages, temperature=0.0, max_tokens=400)
            
            # Clean response (remove markdown if present)
            response_clean = response.strip()
            if response_clean.startswith("```"):
                lines = response_clean.split("\n")
                response_clean = "\n".join([l for l in lines if not l.startswith("```")])
                response_clean = response_clean.strip()
            
            # Parse JSON
            judge_result = json.loads(response_clean)
            
            # Validate required fields
            required_fields = ["label", "score", "reason"]
            for field in required_fields:
                if field not in judge_result:
                    print(f"[LLM JUDGE WARNING] Missing required field: {field}")
                    return {
                        "label": "judge_error",
                        "score": 0.0,
                        "reason": f"Judge returned invalid JSON (missing {field})",
                        "missing_coverage": [],
                        "incorrect_claims": []
                    }
            
            # Validate label
            valid_labels = ["correct", "partially_correct", "incorrect"]
            if judge_result["label"] not in valid_labels:
                print(f"[LLM JUDGE WARNING] Invalid label: {judge_result['label']}")
                judge_result["label"] = "judge_error"
            
            # Ensure optional fields exist
            judge_result.setdefault("missing_coverage", [])
            judge_result.setdefault("incorrect_claims", [])
            
            return judge_result
            
        except json.JSONDecodeError as e:
            print(f"[LLM JUDGE ERROR] Failed to parse JSON: {e}")
            print(f"[LLM JUDGE ERROR] Response was: {response[:200] if 'response' in locals() else 'N/A'}")
            return {
                "label": "judge_error",
                "score": 0.0,
                "reason": f"Judge returned invalid JSON: {str(e)}",
                "missing_coverage": [],
                "incorrect_claims": []
            }
        except LLMError as e:
            print(f"[LLM JUDGE ERROR] LLM request failed: {e}")
            return {
                "label": "judge_error",
                "score": 0.0,
                "reason": f"LLM request failed: {str(e)}",
                "missing_coverage": [],
                "incorrect_claims": []
            }
        except Exception as e:
            print(f"[LLM JUDGE ERROR] Unexpected error: {e}")
            return {
                "label": "judge_error",
                "score": 0.0,
                "reason": f"Unexpected error: {str(e)}",
                "missing_coverage": [],
                "incorrect_claims": []
            }
    
    def run_single_test(self, test_case: Dict) -> Dict[str, Any]:
        """
        Run a single test case.
        
        Args:
            test_case: Test case dictionary
            
        Returns:
            Result dictionary with success/failure and details
        """
        print(f"\n{'='*80}")
        print(f"Test {test_case['id']}: {test_case['question']}")
        print(f"Expected template: {test_case['expected_template']}")
        print(f"Category: {test_case['category']} | Difficulty: {test_case['difficulty']}")
        print(f"{'='*80}")
        
        start_time = time.time()
        
        try:
            # Run agent
            result = run_agent(
                session_id=f"eval_test_{test_case['id']}",
                user_message=test_case["question"],
                history=[],
                model=None
            )
            
            execution_time = time.time() - start_time
            
            # Extract results
            used_template = result.get("used_template")
            final_answer = result.get("answer", "")
            sparql_query = result.get("sparql", "")
            rows = result.get("rows", [])
            debug_info = result.get("debug", {})
            error_msg = debug_info.get("error") if debug_info else None
            
            # Check if correct template was used
            template_match = used_template == test_case["expected_template"]
            
            # Check if query executed successfully
            success = final_answer and final_answer != "No data found." and not final_answer.startswith("I'm sorry")
            
            result_dict = {
                "test_id": test_case["id"],
                "question": test_case["question"],
                "expected_template": test_case["expected_template"],
                "actual_template": used_template,
                "template_match": template_match,
                "success": success,
                "has_results": len(rows) > 0 if rows else False,
                "result_count": len(rows) if rows else 0,
                "execution_time": round(execution_time, 3),
                "answer_length": len(final_answer) if final_answer else 0,
                "category": test_case["category"],
                "difficulty": test_case["difficulty"],
                "error": error_msg,
                "notes": test_case.get("notes", "")
            }
            
            # Add LLM-as-judge evaluation if enabled
            if self.use_llm_judge and success:
                print(f"\n🤖 Running LLM-as-judge evaluation...")
                judge_result = self.llm_judge_evaluate(
                    question=test_case["question"],
                    expected_template=test_case["expected_template"],
                    expected_coverage=test_case.get("expected_coverage", []),
                    final_answer=final_answer,
                    sparql_query=sparql_query,
                    evidence=result.get("evidence", ""),
                    actual_template=used_template
                )
                result_dict["llm_judge_label"] = judge_result["label"]
                result_dict["llm_judge_score"] = judge_result["score"]
                result_dict["llm_judge_reason"] = judge_result["reason"]
                result_dict["llm_judge_missing_coverage"] = judge_result.get("missing_coverage", [])
                result_dict["llm_judge_incorrect_claims"] = judge_result.get("incorrect_claims", [])
                
                print(f"  Label: {judge_result['label']}")
                print(f"  Score: {judge_result['score']}")
                print(f"  Reason: {judge_result['reason'][:100]}...")
            elif self.use_llm_judge and not success:
                # Don't judge failed executions
                result_dict["llm_judge_label"] = "not_evaluated"
                result_dict["llm_judge_score"] = 0.0
                result_dict["llm_judge_reason"] = "Query execution failed"
                result_dict["llm_judge_missing_coverage"] = []
                result_dict["llm_judge_incorrect_claims"] = []
            
            # Print results
            print(f"\n✓ Template Match: {'PASS' if template_match else 'FAIL'}")
            print(f"  Expected: {test_case['expected_template']}")
            print(f"  Got: {used_template}")
            print(f"\n✓ Execution: {'PASS' if success else 'FAIL'}")
            print(f"  Result count: {len(rows) if rows else 0}")
            print(f"  Execution time: {execution_time:.3f}s")
            
            if final_answer and len(final_answer) < 300:
                print(f"\n📝 Answer: {final_answer[:200]}...")
            
            if error_msg:
                print(f"\n❌ Error: {error_msg}")
            
            return result_dict
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"\n❌ Exception: {str(e)}")
            
            result_dict = {
                "test_id": test_case["id"],
                "question": test_case["question"],
                "expected_template": test_case["expected_template"],
                "actual_template": None,
                "template_match": False,
                "success": False,
                "has_results": False,
                "result_count": 0,
                "execution_time": round(execution_time, 3),
                "answer_length": 0,
                "category": test_case["category"],
                "difficulty": test_case["difficulty"],
                "error": str(e),
                "notes": test_case.get("notes", "")
            }
            
            # Add judge fields if LLM judge is enabled
            if self.use_llm_judge:
                result_dict["llm_judge_label"] = "not_evaluated"
                result_dict["llm_judge_score"] = 0.0
                result_dict["llm_judge_reason"] = "Test execution failed"
                result_dict["llm_judge_missing_coverage"] = []
                result_dict["llm_judge_incorrect_claims"] = []
            
            return result_dict
    
    def run_all_tests(self) -> List[Dict]:
        """Run all test cases and return results."""
        print(f"\n{'#'*80}")
        print(f"# CLIMATE CHAT AGENT EVALUATION")
        print(f"# Dataset: {self.tests['metadata']['dataset']}")
        print(f"# Coverage: {self.tests['metadata']['temporal_coverage']}")
        print(f"# Total Tests: {self.tests['metadata']['total_questions']}")
        print(f"{'#'*80}\n")
        
        results = []
        for test_case in self.tests["test_cases"]:
            result = self.run_single_test(test_case)
            results.append(result)
            time.sleep(0.5)  # Small delay between tests
        
        self.results = results
        return results
    
    def run_by_category(self, category: str) -> List[Dict]:
        """Run tests for a specific category."""
        filtered_tests = [
            tc for tc in self.tests["test_cases"] 
            if tc["category"] == category
        ]
        
        print(f"\nRunning {len(filtered_tests)} tests for category: {category}\n")
        
        results = []
        for test_case in filtered_tests:
            result = self.run_single_test(test_case)
            results.append(result)
            time.sleep(0.5)
        
        self.results = results
        return results
    
    def run_by_id(self, test_id: int) -> Dict:
        """Run a specific test by ID."""
        test_case = next(
            (tc for tc in self.tests["test_cases"] if tc["id"] == test_id),
            None
        )
        
        if not test_case:
            raise ValueError(f"Test ID {test_id} not found")
        
        result = self.run_single_test(test_case)
        self.results = [result]
        return result
    
    def generate_report(self, output_file: Optional[str] = None) -> Dict:
        """
        Generate evaluation report.
        
        Args:
            output_file: Optional file to save report (JSON format)
            
        Returns:
            Report dictionary
        """
        if not self.results:
            print("No results to report. Run tests first.")
            return {}
        
        # Calculate statistics
        total_tests = len(self.results)
        template_matches = sum(1 for r in self.results if r["template_match"])
        successful = sum(1 for r in self.results if r["success"])
        with_results = sum(1 for r in self.results if r["has_results"])
        
        avg_execution_time = sum(r["execution_time"] for r in self.results) / total_tests
        
        # LLM judge statistics (if enabled)
        llm_judge_stats = {}
        if self.use_llm_judge:
            correct_count = sum(1 for r in self.results if r.get("llm_judge_label") == "correct")
            partially_correct_count = sum(1 for r in self.results if r.get("llm_judge_label") == "partially_correct")
            incorrect_count = sum(1 for r in self.results if r.get("llm_judge_label") == "incorrect")
            judge_error_count = sum(1 for r in self.results if r.get("llm_judge_label") == "judge_error")
            not_evaluated_count = sum(1 for r in self.results if r.get("llm_judge_label") == "not_evaluated")
            
            # Calculate average score (exclude not_evaluated and judge_error)
            scored_results = [
                r for r in self.results 
                if r.get("llm_judge_label") not in ["not_evaluated", "judge_error"]
            ]
            avg_judge_score = (
                sum(r.get("llm_judge_score", 0.0) for r in scored_results) / len(scored_results)
                if scored_results else 0.0
            )
            
            llm_judge_stats = {
                "enabled": True,
                "correct_count": correct_count,
                "partially_correct_count": partially_correct_count,
                "incorrect_count": incorrect_count,
                "judge_error_count": judge_error_count,
                "not_evaluated_count": not_evaluated_count,
                "average_score": round(avg_judge_score, 3),
                "correctness_rate": round(correct_count / max(len(scored_results), 1) * 100, 2) if scored_results else 0.0
            }
        else:
            llm_judge_stats = {"enabled": False}
        
        # Group by category
        by_category = {}
        for result in self.results:
            cat = result["category"]
            if cat not in by_category:
                by_category[cat] = {"total": 0, "passed": 0, "template_match": 0}
            by_category[cat]["total"] += 1
            if result["success"]:
                by_category[cat]["passed"] += 1
            if result["template_match"]:
                by_category[cat]["template_match"] += 1
        
        # Group by difficulty
        by_difficulty = {}
        for result in self.results:
            diff = result["difficulty"]
            if diff not in by_difficulty:
                by_difficulty[diff] = {"total": 0, "passed": 0}
            by_difficulty[diff]["total"] += 1
            if result["success"]:
                by_difficulty[diff]["passed"] += 1
        
        # Failures
        failures = [
            {
                "id": r["test_id"],
                "question": r["question"],
                "expected": r["expected_template"],
                "got": r["actual_template"],
                "error": r["error"]
            }
            for r in self.results if not r["success"]
        ]
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "template_matches": template_matches,
                "template_match_rate": round(template_matches / total_tests * 100, 2),
                "successful_executions": successful,
                "success_rate": round(successful / total_tests * 100, 2),
                "with_results": with_results,
                "avg_execution_time": round(avg_execution_time, 3),
                "llm_judge": llm_judge_stats
            },
            "by_category": by_category,
            "by_difficulty": by_difficulty,
            "failures": failures,
            "detailed_results": self.results
        }
        
        # Print report
        self._print_report(report)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Report saved to: {output_file}")
        
        return report
    
    def _print_report(self, report: Dict):
        """Print formatted evaluation report."""
        print(f"\n{'#'*80}")
        print(f"# EVALUATION REPORT")
        print(f"# Generated: {report['timestamp']}")
        print(f"{'#'*80}\n")
        
        summary = report["summary"]
        print("📊 OVERALL SUMMARY")
        print(f"  Total Tests: {summary['total_tests']}")
        print(f"  Template Match Rate: {summary['template_match_rate']}% ({summary['template_matches']}/{summary['total_tests']})")
        print(f"  Success Rate: {summary['success_rate']}% ({summary['successful_executions']}/{summary['total_tests']})")
        print(f"  Tests with Results: {summary['with_results']}")
        print(f"  Avg Execution Time: {summary['avg_execution_time']}s")
        
        # LLM Judge Summary
        if summary["llm_judge"]["enabled"]:
            judge = summary["llm_judge"]
            print(f"\n🤖 LLM-AS-JUDGE SUMMARY")
            print(f"  Average Score: {judge['average_score']}")
            print(f"  Correctness Rate: {judge['correctness_rate']}%")
            print(f"  Correct: {judge['correct_count']}")
            print(f"  Partially Correct: {judge['partially_correct_count']}")
            print(f"  Incorrect: {judge['incorrect_count']}")
            if judge['judge_error_count'] > 0:
                print(f"  Judge Errors: {judge['judge_error_count']}")
            if judge['not_evaluated_count'] > 0:
                print(f"  Not Evaluated: {judge['not_evaluated_count']}")
        
        print("\n📁 BY CATEGORY")
        for cat, stats in report["by_category"].items():
            success_rate = round(stats["passed"] / stats["total"] * 100, 1)
            template_rate = round(stats["template_match"] / stats["total"] * 100, 1)
            print(f"  {cat.upper()}: {stats['passed']}/{stats['total']} passed ({success_rate}%), template match: {template_rate}%")
        
        print("\n⚡ BY DIFFICULTY")
        for diff, stats in report["by_difficulty"].items():
            success_rate = round(stats["passed"] / stats["total"] * 100, 1)
            print(f"  {diff.upper()}: {stats['passed']}/{stats['total']} passed ({success_rate}%)")
        
        if report["failures"]:
            print(f"\n❌ FAILURES ({len(report['failures'])})")
            for failure in report["failures"][:10]:  # Show first 10
                print(f"\n  Test {failure['id']}: {failure['question']}")
                print(f"    Expected template: {failure['expected']}")
                print(f"    Got: {failure['got']}")
                if failure['error']:
                    print(f"    Error: {failure['error'][:100]}")


def main():
    """Main entry point for evaluation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate Climate Chat Agent")
    parser.add_argument("--question-id", type=int, help="Run specific question by ID")
    parser.add_argument("--category", type=str, help="Run tests for specific category")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--output", type=str, help="Output file for report (JSON)")
    parser.add_argument("--llm-judge", action="store_true", help="Enable LLM-as-judge evaluation")
    
    args = parser.parse_args()
    
    # Create evaluator with optional LLM judge
    evaluator = AgentEvaluator(use_llm_judge=args.llm_judge)
    
    if args.llm_judge:
        print("\n" + "="*80)
        print("🤖 LLM-AS-JUDGE MODE ENABLED")
        print("="*80 + "\n")
    
    # Run tests based on arguments
    if args.question_id:
        evaluator.run_by_id(args.question_id)
    elif args.category:
        evaluator.run_by_category(args.category)
    else:
        evaluator.run_all_tests()
    
    # Generate report
    if args.report or args.output:
        evaluator.generate_report(args.output)
    else:
        # Always show summary
        evaluator.generate_report()


if __name__ == "__main__":
    main()
