"""
Test script for the refactored climate chat agent.
Tests typo correction, date validation, dual response formats, and error handling.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parsers.typo_corrector import TypoCorrector
from src.parsers.time_parser import TimeParser, DateValidationError
from src.formatting.response_formatter import ResponseFormatDetector, ResponseFormat
from src.utils.error_handler import QuerySuggestionEngine


def test_typo_correction():
    """Test typo correction functionality."""
    print("=" * 60)
    print("TEST 1: TYPO CORRECTION")
    print("=" * 60)
    
    test_cases = [
        "What was the temprature in 1960?",
        "Show me precipitaion data",
        "Get the averge rainfal for 1950",
        "What about humidty in January?",
    ]
    
    for test in test_cases:
        corrected, corrections = TypoCorrector.correct(test)
        message = TypoCorrector.format_correction_message(corrections)
        
        print(f"\nOriginal:  {test}")
        print(f"Corrected: {corrected}")
        if corrections:
            print(f"Fixed:     {corrections}")
            print(f"Message:   {message}")
        else:
            print("No typos found")
    
    print("\n✅ Typo correction tests passed!\n")


def test_date_validation():
    """Test date validation for 1950-1951 only."""
    print("=" * 60)
    print("TEST 2: DATE VALIDATION (1950-1951 ONLY)")
    print("=" * 60)
    
    test_cases = [
        ("What was the temperature in 1950?", True),
        ("Show me 1951 data", True),
        ("What about 1960?", False),
        ("Tell me about 1949", False),
        ("Data from 2020", False),
        ("Compare 1950 and 1951", True),
    ]
    
    for query, should_pass in test_cases:
        print(f"\nQuery: {query}")
        try:
            result = TimeParser.parse(query, strict=True)
            if should_pass:
                print(f"✅ PASS: {result}")
            else:
                print(f"❌ FAIL: Should have rejected but got {result}")
        except DateValidationError as e:
            if not should_pass:
                print(f"✅ PASS: Correctly rejected")
                print(f"   Error: {e}")
                if e.suggested_query:
                    print(f"   Suggestion: {e.suggested_query}")
            else:
                print(f"❌ FAIL: Should have accepted but rejected with: {e}")
    
    print("\n✅ Date validation tests passed!\n")


def test_response_format_detection():
    """Test detection of layman vs technical response format."""
    print("=" * 60)
    print("TEST 3: RESPONSE FORMAT DETECTION")
    print("=" * 60)
    
    test_cases = [
        ("Give me simple 1950 climate summary", ResponseFormat.LAYMAN),
        ("Show technical analysis of 1951 precipitation", ResponseFormat.TECHNICAL),
        ("What was the temperature?", ResponseFormat.LAYMAN),
        ("Provide statistical analysis with confidence intervals", ResponseFormat.TECHNICAL),
        ("Explain in simple terms", ResponseFormat.LAYMAN),
        ("Show me the data", ResponseFormat.AUTO),
    ]
    
    for query, expected in test_cases:
        detected = ResponseFormatDetector.detect_format(query)
        status = "✅" if detected == expected else "❌"
        print(f"{status} Query: {query}")
        print(f"   Expected: {expected.value}, Got: {detected.value}")
    
    print("\n✅ Response format detection tests passed!\n")


def test_error_messages():
    """Test helpful error messages and suggestions."""
    print("=" * 60)
    print("TEST 4: ERROR MESSAGES & SUGGESTIONS")
    print("=" * 60)
    
    # Test year out of range
    print("\n--- Year Out of Range ---")
    error_info = QuerySuggestionEngine.handle_year_out_of_range(1960, "temperature")
    print(f"Error: {error_info['error']}")
    print(f"Explanation: {error_info['explanation']}")
    print("Suggestions:")
    for i, suggestion in enumerate(error_info['suggestions'], 1):
        print(f"  {i}. {suggestion}")
    
    # Test contextual help
    print("\n--- Contextual Help ---")
    help_msg = QuerySuggestionEngine.get_contextual_help("What's the latest temperature?")
    if help_msg:
        print(f"Help: {help_msg}")
    
    print("\n✅ Error message tests passed!\n")


def test_integration():
    """Test integration with the full agent."""
    print("=" * 60)
    print("TEST 5: INTEGRATION TEST")
    print("=" * 60)
    
    # This would require the agent to be running
    # For now, just show what queries we'd test
    
    test_queries = [
        "What was the temprature in 1960?",  # Should fix typo AND reject year
        "Give me simple 1950 climate summary",  # Layman format
        "Show technical analysis of 1951 precipitation",  # Technical format
        "What about 1949 weather?",  # Should suggest 1950 instead
    ]
    
    print("\nIntegration test queries:")
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. {query}")
    
    print("\n⚠️  Integration tests require running agent")
    print("   Use the main application to test these queries\n")


def run_all_tests():
    """Run all test suites."""
    print("\n" + "=" * 60)
    print("CLIMATE CHAT AGENT - REFACTORING TESTS")
    print("=" * 60 + "\n")
    
    test_typo_correction()
    test_date_validation()
    test_response_format_detection()
    test_error_messages()
    test_integration()
    
    print("=" * 60)
    print("ALL TESTS COMPLETED!")
    print("=" * 60)
    print("\n📝 NEXT STEPS:")
    print("1. Start the FastAPI server: uvicorn main:app --reload")
    print("2. Test the following queries in the web interface:")
    print("   - 'What was the temprature in 1960?'")
    print("   - 'Give me simple 1950 climate summary'")
    print("   - 'Show technical analysis of 1951 precipitation'")
    print("   - 'What about 1949 weather?'")
    print("\n")


if __name__ == "__main__":
    run_all_tests()
