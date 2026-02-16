"""Test new statistical and filtering capabilities."""
from graph_agent import run_agent

print("=" * 60)
print("Testing Time Series Statistics and Filtering")
print("=" * 60)

# Test 1: Statistics query
print("\n[TEST 1] Calculate statistics for temperature in 2020")
result = run_agent(
    session_id="test_stats",
    user_message="What are the mean, min, and max temperature in 2020?",
    history=[],
    model="ollama:llama3.2"
)
print(f"Template used: {result['used_template']}")
print(f"Answer: {result['answer'][:200]}...")
print(f"Evidence:\n{result['evidence'][:300]}...")

# Test 2: Daily aggregates
print("\n" + "=" * 60)
print("[TEST 2] Daily aggregates for temperature")
result = run_agent(
    session_id="test_daily",
    user_message="Show me daily temperature statistics for January 2020",
    history=[],
    model="ollama:llama3.2"
)
print(f"Template used: {result['used_template']}")
print(f"Answer: {result['answer'][:200]}...")
print(f"Evidence:\n{result['evidence'][:300]}...")

# Test 3: Filtered data
print("\n" + "=" * 60)
print("[TEST 3] Filter temperature data")
result = run_agent(
    session_id="test_filter",
    user_message="Show me temperature values between 20 and 30 degrees in 2020",
    history=[],
    model="ollama:llama3.2"
)
print(f"Template used: {result['used_template']}")
print(f"Answer: {result['answer'][:200]}...")
print(f"Evidence:\n{result['evidence'][:300]}...")

print("\n" + "=" * 60)
print("Tests Complete!")
print("=" * 60)
