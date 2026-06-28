"""
Test multiple questions from test_questions.json
"""
from src.query.query_templates import render_template
from src.query.sparql_client import run_sparql

test_cases = [
    {
        "id": 1,
        "question": "What variables are available?",
        "template": "list_properties",
        "params": {}
    },
    {
        "id": 2,
        "question": "List all observation locations",
        "template": "list_features",
        "params": {}
    },
    {
        "id": 4,
        "question": "Give me a climate overview for 2024",
        "template": "all_properties_summary",
        "params": {"start": "2024-01-01T00:00:00", "end": "2025-01-01T00:00:00"}
    },
    {
        "id": 5,
        "question": "What was the climate like in 1950?",
        "template": "all_properties_summary",
        "params": {"start": "1950-01-01T00:00:00", "end": "1951-01-01T00:00:00"}
    },
    {
        "id": 7,
        "question": "What was the average temperature in 2020?",
        "template": "average_for_property_date_range",
        "params": {
            "property_uri": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
            "start": "2020-01-01T00:00:00",
            "end": "2021-01-01T00:00:00"
        }
    },
]

print("=" * 70)
print("Testing Multiple Queries")
print("=" * 70)

for test in test_cases:
    print(f"\n[Test {test['id']}] {test['question']}")
    print("-" * 70)
    
    try:
        query = render_template(test['template'], test['params'])
        result = run_sparql(query, validate=False)
        bindings = result.get("results", {}).get("bindings", [])
        
        if bindings:
            print(f"✓ SUCCESS - Found {len(bindings)} results")
            # Show first result
            if len(bindings) > 0:
                first = bindings[0]
                sample_keys = list(first.keys())[:3]
                print(f"  Sample keys: {sample_keys}")
        else:
            print(f"✗ FAILED - No results returned")
            
    except Exception as e:
        print(f"✗ ERROR - {str(e)[:100]}")

print("\n" + "=" * 70)
print("Testing Complete")
print("=" * 70)
