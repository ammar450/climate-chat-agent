"""
Comprehensive test of all 30 questions from test_questions.json
"""
import json
from src.agent.graph_agent import run_agent

# Load test questions
with open('evaluation/test_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

test_cases = data['test_cases']

print("=" * 80)
print(f"TESTING ALL {len(test_cases)} QUESTIONS")
print("=" * 80)

results = {
    'passed': [],
    'failed': [],
    'errors': []
}

for i, test in enumerate(test_cases, 1):
    question = test['question']
    expected_template = test['expected_template']
    test_id = test['id']
    
    print(f"\n[{i}/30] Testing Question ID {test_id}")
    print(f"Question: {question}")
    print(f"Expected template: {expected_template}")
    print("-" * 80)
    
    try:
        result = run_agent("test-session", question)
        
        if result.get("error"):
            print(f"[FAIL] Error: {result['error'][:100]}")
            results['failed'].append({
                'id': test_id,
                'question': question,
                'expected': expected_template,
                'error': result['error']
            })
        elif "I don't have enough information" in result.get("answer", "") or \
             "No data found" in result.get("answer", "") or \
             "I'm sorry" in result.get("answer", ""):
            print(f"[FAIL] No data returned")
            print(f"   Answer: {result.get('answer', '')[:150]}...")
            results['failed'].append({
                'id': test_id,
                'question': question,
                'expected': expected_template,
                'actual': result.get('used_template'),
                'answer': result.get('answer', '')[:200]
            })
        else:
            used_template = result.get('used_template', 'unknown')
            answer_preview = result.get('answer', '')[:100]
            
            # Check if template matches
            template_match = used_template == expected_template
            
            if template_match:
                print(f"[PASS] Template: {used_template}")
                print(f"   Answer: {answer_preview}...")
                results['passed'].append({
                    'id': test_id,
                    'question': question,
                    'template': used_template
                })
            else:
                print(f"[PARTIAL] Wrong template")
                print(f"   Expected: {expected_template}")
                print(f"   Got: {used_template}")
                print(f"   Answer: {answer_preview}...")
                results['failed'].append({
                    'id': test_id,
                    'question': question,
                    'expected': expected_template,
                    'actual': used_template,
                    'answer': answer_preview
                })
                
    except Exception as e:
        print(f"[ERROR] {str(e)[:100]}")
        results['errors'].append({
            'id': test_id,
            'question': question,
            'error': str(e)[:200]
        })

# Print summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Passed: {len(results['passed'])}/30")
print(f"Failed: {len(results['failed'])}/30")
print(f"Errors: {len(results['errors'])}/30")

if results['failed']:
    print("\n" + "=" * 80)
    print("FAILED TESTS")
    print("=" * 80)
    for item in results['failed']:
        print(f"\nID {item['id']}: {item['question']}")
        print(f"  Expected: {item.get('expected')}")
        print(f"  Got: {item.get('actual', 'N/A')}")
        if 'answer' in item:
            print(f"  Answer: {item['answer'][:100]}...")

if results['errors']:
    print("\n" + "=" * 80)
    print("ERRORS")
    print("=" * 80)
    for item in results['errors']:
        print(f"\nID {item['id']}: {item['question']}")
        print(f"  Error: {item['error']}")

# Save results to file
with open('test_results_all_30.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
    
print(f"\nResults saved to: test_results_all_30.json")
