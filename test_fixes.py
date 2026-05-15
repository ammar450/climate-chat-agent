"""Quick test for agent fixes"""
from src.agent.graph_agent import run_agent

print("=" * 60)
print("TEST 1: Value filtering (between 5 and 15)")
print("=" * 60)
result = run_agent('test', 'Show me wind speed between 5 and 15 m/s in 2020', model='openai:gpt-4o-mini')
print(f"Keys: {list(result.keys())}")
print(f"Answer: {result.get('answer', 'N/A')[:200]}...")
print()

print("=" * 60)
print("TEST 2: Monthly aggregation")
print("=" * 60)
result = run_agent('test', 'Show monthly temperature averages for 2022', model='openai:gpt-4o-mini')
print(f"Answer has 'monthly': {'monthly' in result.get('answer', '').lower() or 'month' in result.get('answer', '').lower()}")
print(f"Answer: {result.get('answer', 'N/A')[:200]}...")
print()

print("=" * 60)
print("TEST 3: Daily aggregation")
print("=" * 60)
result = run_agent('test', 'Show daily temperature averages for January 2024', model='openai:gpt-4o-mini')
print(f"Answer has 'daily': {'daily' in result.get('answer', '').lower() or 'day' in result.get('answer', '').lower()}")
print(f"Answer: {result.get('answer', 'N/A')[:200]}...")
print()

print("=" * 60)
print("TEST 4: Statistics with count")
print("=" * 60)
result = run_agent('test', 'Calculate temperature statistics for 2024', model='openai:gpt-4o-mini')
print(f"Answer has 'count/observations': {'count' in result.get('answer', '').lower() or 'observation' in result.get('answer', '').lower()}")
print(f"Answer: {result.get('answer', 'N/A')[:300]}...")
