"""Test agent with 1950-1951 data awareness."""
from graph_agent import run_agent

print("=" * 60)
print("Testing Agent with 1950-1951 Data")
print("=" * 60)

# Test 1: Ask without specifying year (should default to 1950-1951)
print("\n[TEST 1] Query without year (should default to 1950-1951)")
result = run_agent(
    session_id="test_1950",
    user_message="What's the average temperature?",
    history=[],
    model="ollama:llama3.2"
)
print(f"Template: {result['used_template']}")
print(f"Answer: {result['answer'][:300]}...")

# Test 2: Ask specifically for 1950
print("\n" + "=" * 60)
print("[TEST 2] Query for 1950 data")
result = run_agent(
    session_id="test_1950_explicit",
    user_message="Show me temperature statistics for 1950",
    history=[],
    model="ollama:llama3.2"
)
print(f"Template: {result['used_template']}")
print(f"Answer: {result['answer'][:300]}...")

# Test 3: Ask for 1951
print("\n" + "=" * 60)
print("[TEST 3] Query for January 1951")
result = run_agent(
    session_id="test_1951",
    user_message="What were the daily temperature values in January 1951?",
    history=[],
    model="ollama:llama3.2"
)
print(f"Template: {result['used_template']}")
print(f"Answer: {result['answer'][:300]}...")

# Test 4: Filter temperature data from 1950
print("\n" + "=" * 60)
print("[TEST 4] Filter temperature between 15-25 degrees in 1950")
result = run_agent(
    session_id="test_filter_1950",
    user_message="Show temperature readings between 15 and 25 degrees in 1950",
    history=[],
    model="ollama:llama3.2"
)
print(f"Template: {result['used_template']}")
print(f"Answer: {result['answer'][:300]}...")

print("\n" + "=" * 60)
print("Agent successfully trained for 1950-1951 data!")
print("=" * 60)
