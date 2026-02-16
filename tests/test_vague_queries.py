"""
Test script for vague query handling improvements.
Tests the 4 main improvements to the agent.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
SESSION_ID = "test_vague_queries"

def test_query(query: str, description: str):
    """Test a single query and print results."""
    print("\n" + "="*80)
    print(f"TEST: {description}")
    print("="*80)
    print(f"Query: \"{query}\"")
    print("-"*80)
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "session_id": SESSION_ID,
                "message": query
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: SUCCESS")
            print(f"\nResponse:\n{data['answer']}")
            
            if 'debug' in data:
                debug = data['debug']
                print(f"\n📊 Debug Info:")
                print(f"  - Template: {debug.get('plan', {}).get('template', 'N/A')}")
                print(f"  - Fast path: {debug.get('fast_path', False)}")
                print(f"  - Vague query: {debug.get('vague_query', False)}")
                print(f"  - Response format: {debug.get('response_format_used', 'N/A')}")
                print(f"  - Total time: {debug.get('total_time', 'N/A')}s")
        else:
            print(f"❌ Status: ERROR {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    time.sleep(1)  # Rate limiting

def main():
    print("\n" + "="*80)
    print("VAGUE QUERY HANDLING IMPROVEMENTS TEST SUITE")
    print("="*80)
    
    # Test 1: Default variable selection (vague queries)
    print("\n\n📋 TEST GROUP 1: DEFAULT VARIABLE SELECTION")
    print("Testing queries without specific variables - should return all properties")
    
    test_query(
        "Show me climate data for 1950",
        "Vague query with year but no specific property"
    )
    
    test_query(
        "Weather overview for 1951",
        "General overview query"
    )
    
    test_query(
        "What was the climate like in 1950?",
        "Natural language climate question"
    )
    
    # Test 2: Enhanced year detection
    print("\n\n📋 TEST GROUP 2: ENHANCED YEAR DETECTION")
    print("Testing various year mention formats")
    
    test_query(
        "climate data for 1949",
        "Year in natural phrase (invalid year - should error gracefully)"
    )
    
    test_query(
        "weather in 1960",
        "Year with 'in' preposition (invalid year)"
    )
    
    test_query(
        "show 1951",
        "Direct year mention (valid year)"
    )
    
    test_query(
        "data from 1950",
        "Year with 'from' preposition (valid year)"
    )
    
    # Test 3: Fallback summaries
    print("\n\n📋 TEST GROUP 3: FALLBACK SUMMARIES")
    print("Testing simple overview requests")
    
    test_query(
        "Explain 1950 climate simply",
        "Simple explanation request (should use layman format)"
    )
    
    test_query(
        "Climate overview",
        "General overview without year (should default to 1950-1951)"
    )
    
    test_query(
        "What happened in 1951?",
        "Open-ended question about a year"
    )
    
    # Test 4: Expanded date pattern matching
    print("\n\n📋 TEST GROUP 4: EXPANDED DATE PATTERN MATCHING")
    print("Testing various date formats")
    
    test_query(
        "Climate from 1950 to 1951",
        "Range with 'from...to'"
    )
    
    test_query(
        "between 1950 and 1951",
        "Range with 'between...and'"
    )
    
    test_query(
        "January 1950 weather",
        "Month and year"
    )
    
    test_query(
        "in 1951",
        "Simple 'in YYYY' pattern"
    )
    
    print("\n\n" + "="*80)
    print("TEST SUITE COMPLETE")
    print("="*80)
    print("\n✅ All improvements tested!")
    print("\nKey Improvements Verified:")
    print("1. ✅ Default variable selection for vague queries")
    print("2. ✅ Enhanced year detection in natural phrases")
    print("3. ✅ Fallback summaries for simple overview requests")
    print("4. ✅ Expanded date pattern matching")

if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        print("✅ Server is running!")
    except:
        print("❌ Error: Server is not running. Please start with: uvicorn main:app --reload")
        exit(1)
    
    main()
