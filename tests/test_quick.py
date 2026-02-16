"""Quick test to see what error is happening."""
import traceback
from graph_agent import run_agent

try:
    result = run_agent(
        session_id="test",
        user_message="What variables are available?",
        history=[],
        model="ollama:llama3.2"
    )
    print("SUCCESS!")
    print(f"Answer: {result['answer']}")
except Exception as e:
    print(f"ERROR: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
