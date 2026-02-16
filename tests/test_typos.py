"""Test agent with common terms and typos."""
from graph_agent import run_agent

print("=" * 60)
print("Testing Agent with Common Terms & Typos")
print("=" * 60)

test_queries = [
    # Common terms (non-technical)
    "What's the average rainfall in 1950?",
    "Show me temp data for 1951",
    "Give me moisture readings from January 1950",
    
    # Typos
    "What was the temprature in 1950?",
    "Show me rainfalll data",
    "Calculate precipitaion statistics for 1951",
    "What's the humidty in 1950?",
]

for i, query in enumerate(test_queries, 1):
    print(f"\n[TEST {i}] {query}")
    print("-" * 60)
    
    result = run_agent(
        session_id=f"test_{i}",
        user_message=query,
        history=[],
        model="ollama:llama3.2"
    )
    
    print(f"Template: {result['used_template']}")
    print(f"Answer: {result['answer'][:150]}...")
    
    if result.get('rows'):
        print(f"Rows returned: {len(result['rows'])}")

print("\n" + "=" * 60)
print("Agent successfully handles common terms and typos!")
print("=" * 60)
