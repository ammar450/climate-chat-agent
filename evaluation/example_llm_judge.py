"""
Example: Using LLM-as-Judge Evaluation

This script demonstrates how to use the LLM-as-judge feature
both from command-line and programmatically.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from evaluation.evaluate_agent import AgentEvaluator


def example_single_test_with_judge():
    """Run a single test with LLM-as-judge evaluation."""
    print("="*80)
    print("Example 1: Single Test with LLM-as-Judge")
    print("="*80)
    
    # Create evaluator with LLM judge enabled
    evaluator = AgentEvaluator(use_llm_judge=True)
    
    # Run a specific test
    result = evaluator.run_by_id(1)  # Test ID 1: "What variables are available?"
    
    # Display judge results
    if "llm_judge_label" in result:
        print("\n🤖 LLM Judge Results:")
        print(f"  Label: {result['llm_judge_label']}")
        print(f"  Score: {result['llm_judge_score']}")
        print(f"  Reason: {result['llm_judge_reason']}")
        
        if result['llm_judge_missing_coverage']:
            print(f"  Missing Coverage: {result['llm_judge_missing_coverage']}")
        if result['llm_judge_incorrect_claims']:
            print(f"  Incorrect Claims: {result['llm_judge_incorrect_claims']}")


def example_category_comparison():
    """Compare rule-based vs LLM judge evaluation on a category."""
    print("\n" + "="*80)
    print("Example 2: Category Comparison (Rule-Based vs LLM Judge)")
    print("="*80)
    
    # Run without judge
    print("\n📊 Running rule-based evaluation...")
    evaluator_basic = AgentEvaluator(use_llm_judge=False)
    evaluator_basic.run_by_category("discovery")
    
    basic_success_rate = sum(1 for r in evaluator_basic.results if r['success']) / len(evaluator_basic.results) * 100
    basic_template_match_rate = sum(1 for r in evaluator_basic.results if r['template_match']) / len(evaluator_basic.results) * 100
    
    print(f"\nRule-Based Results:")
    print(f"  Success Rate: {basic_success_rate:.1f}%")
    print(f"  Template Match Rate: {basic_template_match_rate:.1f}%")
    
    # Run with judge
    print("\n🤖 Running with LLM-as-judge...")
    evaluator_judge = AgentEvaluator(use_llm_judge=True)
    evaluator_judge.run_by_category("discovery")
    
    judge_correct_rate = sum(1 for r in evaluator_judge.results if r.get('llm_judge_label') == 'correct') / len(evaluator_judge.results) * 100
    avg_judge_score = sum(r.get('llm_judge_score', 0) for r in evaluator_judge.results) / len(evaluator_judge.results)
    
    print(f"\nLLM Judge Results:")
    print(f"  Correctness Rate: {judge_correct_rate:.1f}%")
    print(f"  Average Score: {avg_judge_score:.3f}")
    
    # Show comparison
    print("\n📈 Comparison:")
    print(f"  Rule-based success vs Judge correctness: {basic_success_rate:.1f}% vs {judge_correct_rate:.1f}%")
    print("\n  This shows whether successful queries actually produce correct answers!")


def example_analyze_judge_reasoning():
    """Analyze judge reasoning for failed cases."""
    print("\n" + "="*80)
    print("Example 3: Analyzing Judge Reasoning")
    print("="*80)
    
    evaluator = AgentEvaluator(use_llm_judge=True)
    
    # Run a few tests
    print("\nRunning first 5 tests with LLM judge...")
    evaluator.tests["test_cases"] = evaluator.tests["test_cases"][:5]  # Limit to 5
    evaluator.run_all_tests()
    
    # Analyze results
    print("\n🔍 Judge Analysis:")
    for result in evaluator.results:
        label = result.get('llm_judge_label', 'not_evaluated')
        score = result.get('llm_judge_score', 0.0)
        
        if label == 'partially_correct' or label == 'incorrect':
            print(f"\n  Test {result['test_id']}: {result['question'][:50]}...")
            print(f"    Rule-based: {'PASS' if result['success'] else 'FAIL'}")
            print(f"    Judge: {label} (score: {score})")
            print(f"    Reason: {result.get('llm_judge_reason', 'N/A')}")
            
            if result.get('llm_judge_missing_coverage'):
                print(f"    Missing: {result['llm_judge_missing_coverage']}")
            if result.get('llm_judge_incorrect_claims'):
                print(f"    Incorrect: {result['llm_judge_incorrect_claims']}")


def main():
    """Run all examples."""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║          LLM-as-Judge Evaluation - Usage Examples                         ║
║                                                                            ║
║  This demonstrates the new LLM-as-judge feature for evaluation            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Choose which example to run:
1. Single test with LLM judge
2. Compare rule-based vs LLM judge on a category
3. Analyze judge reasoning for failed cases
4. Run all examples

Enter choice (1-4, or Enter to skip): """)
    
    choice = input().strip()
    
    if not choice or choice == "0":
        print("\nSkipping examples. You can run them from command line:")
        print("\n  Command-Line Usage:")
        print("  ------------------")
        print("  python evaluation/evaluate_agent.py --question-id 1 --llm-judge")
        print("  python evaluation/evaluate_agent.py --category discovery --llm-judge")
        print("  python evaluation/evaluate_agent.py --report --llm-judge --output results.json")
        return
    
    if choice == "1":
        example_single_test_with_judge()
    elif choice == "2":
        example_category_comparison()
    elif choice == "3":
        example_analyze_judge_reasoning()
    elif choice == "4":
        example_single_test_with_judge()
        example_category_comparison()
        example_analyze_judge_reasoning()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
