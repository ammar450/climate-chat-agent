"""
Test the query: What variables are available?
"""
from src.query.query_templates import render_template, GRAPH
from src.query.sparql_client import run_sparql, ENDPOINT

print(f"Endpoint: {ENDPOINT}")
print(f"Graph: {GRAPH}")
print()

# Test the list_properties template
print("=" * 70)
print("Query: What variables are available?")
print("=" * 70)

query = render_template("list_properties", {})
print(f"\nGenerated SPARQL Query:")
print("-" * 70)
print(query)
print("-" * 70)

try:
    result = run_sparql(query, validate=False)
    bindings = result.get("results", {}).get("bindings", [])
    
    if bindings:
        print(f"\n✓ Found {len(bindings)} climate variables:\n")
        for i, binding in enumerate(bindings, 1):
            prop = binding.get("property", {}).get("value", "N/A")
            count = binding.get("count", {}).get("value", "0")
            
            # Extract readable name from URI
            prop_name = prop.split("/")[-1].replace("_", " ").title()
            
            print(f"{i}. {prop_name}")
            print(f"   URI: {prop}")
            print(f"   Observations: {int(count):,}")
            print()
    else:
        print("✗ No variables found")
        print(f"Result: {result}")
except Exception as e:
    print(f"✗ Error: {e}")
