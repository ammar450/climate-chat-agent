"""
Climate Chat Agent Evaluation Framework

This script evaluates the agent's performance by:
1. Running predefined test questions
2. Checking if correct SPARQL templates are used
3. Verifying query execution and results
4. Generating evaluation reports

Usage:
    python evaluate_agent.py                    # Run all tests
    python evaluate_agent.py --question-id 5    # Run specific test
    python evaluate_agent.py --category summary # Run category tests
    python evaluate_agent.py --report           # Generate detailed report
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


class AgentEvaluator:
    """Evaluates agent performance on test questions."""
    
    def __init__(self, test_file: str = "evaluation/test_questions.json"):
        """Initialize evaluator with test questions."""
        self.test_file = test_file
        self.tests = self.load_tests()
        self.results = []
        
    def load_tests(self) -> Dict:
        """Load test questions from JSON file."""
        with open(self.test_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
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
            
            return {
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
                "avg_execution_time": round(avg_execution_time, 3)
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
    
    args = parser.parse_args()
    
    evaluator = AgentEvaluator()
    
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
