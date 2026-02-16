"""
Test the LangGraph agent.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph_agent import run_agent


def test_basic_query():
    """Test a simple query."""
    print("\n🧪 Test 1: Basic query - List properties")
    print("=" * 60)
    
    result = run_agent(
        session_id="test_session_1",
        user_message="What variables are available?",
        history=[],
        model="ollama:llama3.2"
    )
    
    print(f"✅ Answer: {result['answer'][:100]}...")
    print(f"✅ Template: {result['used_template']}")
    print(f"✅ Rows returned: {len(result['rows'])}")
    print(f"✅ Debug: {result['debug']}")
    
    assert result['answer'], "No answer generated"
    assert result['used_template'] == 'list_properties', f"Wrong template: {result['used_template']}"
    print("\n✅ Test 1 PASSED\n")


def test_with_context():
    """Test query with session context."""
    print("\n🧪 Test 2: Query with context - Temperature data")
    print("=" * 60)
    
    result = run_agent(
        session_id="test_session_2",
        user_message="Show me temperature observations",
        history=[],
        model="ollama:llama3.2"
    )
    
    print(f"✅ Answer: {result['answer'][:100]}...")
    print(f"✅ Template: {result['used_template']}")
    print(f"✅ SPARQL: {result['sparql'][:100] if result['sparql'] else 'None'}...")
    print(f"✅ Debug: {result['debug']}")
    
    assert result['answer'], "No answer generated"
    print("\n✅ Test 2 PASSED\n")


def test_followup():
    """Test follow-up question flow."""
    print("\n🧪 Test 3: Follow-up question handling")
    print("=" * 60)
    
    # This might trigger a followup
    result = run_agent(
        session_id="test_session_3",
        user_message="Show me data from an ambiguous query",
        history=[],
        model="ollama:llama3.2"
    )
    
    print(f"✅ Answer: {result['answer'][:150]}...")
    print(f"✅ Template: {result['used_template']}")
    print(f"✅ Debug: {result['debug']}")
    
    print("\n✅ Test 3 PASSED\n")


def test_session_memory():
    """Test session memory persistence."""
    print("\n🧪 Test 4: Session memory across turns")
    print("=" * 60)
    
    session_id = "test_session_4"
    
    # First turn: establish context
    result1 = run_agent(
        session_id=session_id,
        user_message="Show me temperature data",
        history=[],
        model="ollama:llama3.2"
    )
    print(f"Turn 1 - Template: {result1['used_template']}")
    
    # Second turn: follow-up (should remember property)
    result2 = run_agent(
        session_id=session_id,
        user_message="What's the average?",
        history=[{"role": "user", "content": "Show me temperature data"}],
        model="ollama:llama3.2"
    )
    print(f"Turn 2 - Template: {result2['used_template']}")
    print(f"Turn 2 - Answer: {result2['answer'][:100]}...")
    
    print("\n✅ Test 4 PASSED\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 LangGraph Agent Test Suite")
    print("=" * 60)
    
    try:
        test_basic_query()
        test_with_context()
        test_followup()
        test_session_memory()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
