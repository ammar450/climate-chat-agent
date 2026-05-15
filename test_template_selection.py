"""Test agent with fixed template selection."""
from src.agent.graph_agent import run_agent
import uuid

test_cases = [
    {
        "id": 7,
        "question": "What was the average temperature in 2020?",
        "expected_template": "average_for_property_date_range"
    },
    {
        "id": 8,
        "question": "Show me average precipitation in March 1975",
        "expected_template": "average_for_property_date_range"
    },
    {
        "id": 13,
        "question": "Show daily temperature averages for January 2024",
        "expected_template": "daily_aggregates"
    },
    {
        "id": 15,
        "question": "Show monthly temperature averages for 2022",
        "expected_template": "monthly_aggregates"
    },
    {
        "id": 11,
        "question": "What were the highest temperature values in 2023?",
        "expected_template": "top_extremes_for_property"
    },
]

print("="*80)
print("TEMPLATE SELECTION TEST")
print("="*80)

successes = 0
for test in test_cases:
    session_id = str(uuid.uuid4())
    qid = test['id']
    question = test['question']
    expected = test['expected_template']
    
    print(f"\n[TEST {qid}] {question}")
    print(f"Expected template: {expected}")
    
    try:
        result = run_agent(session_id, question)
        
        # Get template from the result - agent returns 'used_template' key
        actual_template = result.get('used_template', 'unknown')
        
        match = actual_template == expected
        successes += (1 if match else 0)
        
        status = "[PASS]" if match else "[FAIL]"
        print(f"Actual template:   {actual_template}")
        print(f"{status}")
        
        # Show answer preview
        if result.get('answer'):
            answer_preview = result['answer'][:100] + "..." if len(result['answer']) > 100 else result['answer']
            print(f"Answer preview:    {answer_preview}")
        
    except Exception as e:
        print(f"[ERROR]: {str(e)[:150]}")

print("\n" + "="*80)
print(f"RESULTS: {successes}/{len(test_cases)} templates matched ({100*successes/len(test_cases):.1f}%)")
print("="*80)
