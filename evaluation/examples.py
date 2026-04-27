"""
Quick Start Example for Climate Chat Agent Evaluation

This script demonstrates how to use the evaluation framework
with a few simple examples.
"""

from evaluation.evaluate_agent import AgentEvaluator


def example_run_all_tests():
    """Example: Run all 30 tests and generate report."""
    print("=" * 80)
    print("Example 1: Running all tests")
    print("=" * 80)
    
    evaluator = AgentEvaluator()
    evaluator.run_all_tests()
    report = evaluator.generate_report(output_file="full_report.json")
    
    print(f"\n✅ Completed {report['summary']['total_tests']} tests")
    print(f"   Success Rate: {report['summary']['success_rate']}%")


def example_run_specific_test():
    """Example: Run a single test by ID."""
    print("\n" + "=" * 80)
    print("Example 2: Running specific test (ID=1)")
    print("=" * 80)
    
    evaluator = AgentEvaluator()
    result = evaluator.run_by_id(1)
    
    print(f"\n✅ Test completed:")
    print(f"   Question: {result['question']}")
    print(f"   Template Match: {result['template_match']}")
    print(f"   Success: {result['success']}")
    print(f"   Execution Time: {result['execution_time']}s")


def example_run_by_category():
    """Example: Run tests for a specific category."""
    print("\n" + "=" * 80)
    print("Example 3: Running statistics category tests")
    print("=" * 80)
    
    evaluator = AgentEvaluator()
    results = evaluator.run_by_category("statistics")
    
    success_count = sum(1 for r in results if r['success'])
    print(f"\n✅ Completed {len(results)} statistics tests")
    print(f"   Success Rate: {success_count}/{len(results)}")


def example_custom_analysis():
    """Example: Custom analysis of results."""
    print("\n" + "=" * 80)
    print("Example 4: Custom result analysis")
    print("=" * 80)
    
    evaluator = AgentEvaluator()
    evaluator.run_all_tests()
    
    # Find slowest queries
    sorted_results = sorted(
        evaluator.results, 
        key=lambda x: x['execution_time'], 
        reverse=True
    )
    
    print("\n🐌 Top 5 slowest queries:")
    for i, result in enumerate(sorted_results[:5], 1):
        print(f"   {i}. Test {result['test_id']}: {result['execution_time']}s")
        print(f"      '{result['question'][:60]}...'")
    
    # Find template with most failures
    from collections import defaultdict
    template_failures = defaultdict(int)
    for r in evaluator.results:
        if not r['success']:
            template_failures[r['expected_template']] += 1
    
    if template_failures:
        print("\n❌ Templates with failures:")
        for template, count in template_failures.items():
            print(f"   {template}: {count} failures")
    else:
        print("\n✅ All templates passed!")


def main():
    """Run all examples."""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║          Climate Chat Agent - Evaluation Framework Examples               ║
║                                                                            ║
║  This script demonstrates various ways to use the evaluation framework    ║
║  Choose which examples to run below                                        ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("Available examples:")
    print("[1] Run all tests (30 questions)")
    print("[2] Run specific test (ID=1)")
    print("[3] Run category tests (statistics)")
    print("[4] Custom analysis (slowest queries, template failures)")
    print("[5] Run all examples")
    print("[0] Exit")
    
    choice = input("\nEnter your choice (0-5): ").strip()
    
    if choice == "1":
        example_run_all_tests()
    elif choice == "2":
        example_run_specific_test()
    elif choice == "3":
        example_run_by_category()
    elif choice == "4":
        example_custom_analysis()
    elif choice == "5":
        example_run_specific_test()
        example_run_by_category()
        example_custom_analysis()
        example_run_all_tests()
    elif choice == "0":
        print("Exiting...")
        return
    else:
        print("Invalid choice. Please run again.")
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
    print("\nFor more options, see: evaluation/README.md")
    print("Or run: python evaluation/evaluate_agent.py --help")


if __name__ == "__main__":
    main()
