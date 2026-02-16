"""
Test daily/monthly aggregation wording and scope detection.
"""

from graph_agent import run_agent
import json


def test_daily_aggregates():
    """Test daily aggregation query."""
    print("=" * 60)
    print("TEST: Daily aggregates for January 1950")
    print("=" * 60)
    
    result = run_agent(
        session_id="test_daily",
        user_message="Show me daily temperature in January 1950",
        history=[],
        model="ollama:llama3.2"
    )
    
    print(f"\n📊 Answer:\n{result['answer']}")
    print(f"\n🔍 Debug Info:")
    print(f"  - Template: {result.get('debug', {}).get('template_used', 'N/A')}")
    print(f"  - Aggregation Scope: {result.get('debug', {}).get('aggregation_scope', 'N/A')}")
    print(f"  - Scope Label: {result.get('debug', {}).get('scope_label', 'N/A')}")
    print(f"  - Feature Count: {result.get('debug', {}).get('feature_count', 'N/A')}")
    print(f"  - Row Count: {result.get('debug', {}).get('row_count', 'N/A')}")
    
    # Check for incorrect wording
    answer_lower = result['answer'].lower()
    if "not enough" in answer_lower or "insufficient" in answer_lower:
        print("\n❌ FAIL: Answer incorrectly says 'not enough info'")
    elif "daily means" in answer_lower or "daily values" in answer_lower:
        print("\n✅ PASS: Answer correctly describes daily means")
    else:
        print("\n⚠️  WARNING: Check answer wording")


def test_monthly_aggregates():
    """Test monthly aggregation query."""
    print("\n" + "=" * 60)
    print("TEST: Monthly aggregates for 1950")
    print("=" * 60)
    
    result = run_agent(
        session_id="test_monthly",
        user_message="Show me monthly temperature in 1950",
        history=[],
        model="ollama:llama3.2"
    )
    
    print(f"\n📊 Answer:\n{result['answer']}")
    print(f"\n🔍 Debug Info:")
    print(f"  - Template: {result.get('debug', {}).get('template_used', 'N/A')}")
    print(f"  - Aggregation Scope: {result.get('debug', {}).get('aggregation_scope', 'N/A')}")
    print(f"  - Scope Label: {result.get('debug', {}).get('scope_label', 'N/A')}")


def test_place_name_followup():
    """Test place name follow-up logic."""
    print("\n" + "=" * 60)
    print("TEST: Place name follow-up (Berlin)")
    print("=" * 60)
    
    result = run_agent(
        session_id="test_place",
        user_message="Show me temperature in Berlin in 1950",
        history=[],
        model="ollama:llama3.2"
    )
    
    print(f"\n📊 Answer:\n{result['answer']}")
    print(f"\n🔍 Debug Info:")
    print(f"  - Has Followup: {result.get('debug', {}).get('has_followup', False)}")


def test_exclusive_end_bounds():
    """Test that time ranges use exclusive end bounds."""
    print("\n" + "=" * 60)
    print("TEST: Exclusive end bounds")
    print("=" * 60)
    
    from time_parser import TimeParser
    
    # Test month range
    month_range = TimeParser._month_year_to_range(1950, 1)
    print(f"January 1950 range: {month_range}")
    assert month_range == ('1950-01-01T00:00:00', '1950-02-01T00:00:00'), "Month range incorrect"
    print("✅ Month range uses exclusive end (1950-02-01)")
    
    # Test day range
    day_range = TimeParser.parse_day(1950, 1, 15)
    print(f"January 15, 1950 range: {day_range}")
    assert day_range == ('1950-01-15T00:00:00', '1950-01-16T00:00:00'), "Day range incorrect"
    print("✅ Day range uses exclusive end (next day at 00:00:00)")
    
    # Test year range
    year_range = TimeParser.parse("in 1950")
    print(f"Year 1950 range: {year_range}")
    assert year_range == ('1950-01-01T00:00:00', '1951-01-01T00:00:00'), "Year range incorrect"
    print("✅ Year range uses exclusive end (1951-01-01)")


if __name__ == "__main__":
    # Test exclusive bounds first (no LLM needed)
    test_exclusive_end_bounds()
    
    # Test with LLM
    print("\n" + "=" * 60)
    print("RUNNING LLM-BASED TESTS")
    print("=" * 60)
    
    test_daily_aggregates()
    # test_monthly_aggregates()  # Uncomment to test monthly
    # test_place_name_followup()  # Uncomment to test place names
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETE")
    print("=" * 60)
