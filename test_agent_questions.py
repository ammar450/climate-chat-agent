"""
Test the full agent with actual questions
"""
from src.agent.graph_agent import run_agent

test_questions = [
    "What variables are available?",
    "Show me climate data for 2000",
    "What was the average temperature in 2020?",
    "Give me a climate overview for 2024",
]

print("=" * 70)
print("Testing Full Agent with Real Questions")
print("=" * 70)

for i, question in enumerate(test_questions, 1):
    print(f"\n[Question {i}] {question}")
    print("-" * 70)
    
    try:
        result = run_agent("test-session", question)
        
        if result.get("answer"):
            answer = result["answer"]
            # Show first 200 chars of answer
            preview = answer[:200] + "..." if len(answer) > 200 else answer
            print(f"✓ Got answer:")
            print(f"  {preview}")
            print(f"\n  Used template: {result.get('used_template', 'N/A')}")
            print(f"  Results count: {len(result.get('results', []))}")
        else:
            print(f"✗ No answer returned")
            print(f"  Result: {result}")
            
    except Exception as e:
        print(f"✗ ERROR - {str(e)[:200]}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
print("Agent Testing Complete")
print("=" * 70)
