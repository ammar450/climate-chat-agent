"""
Test query: Show me climate data for 2000
"""
from src.query.query_templates import render_template, GRAPH
from src.query.sparql_client import run_sparql, ENDPOINT

print(f"Endpoint: {ENDPOINT}")
print(f"Graph: {GRAPH}")
print()

# Test the all_properties_summary template for year 2000
print("=" * 70)
print("Query: Show me climate data for 2000")
print("=" * 70)

# Year 2000: 2000-01-01 to 2001-01-01
query = render_template("all_properties_summary", {
    "start": "2000-01-01T00:00:00",
    "end": "2001-01-01T00:00:00"
})

print(f"\nGenerated SPARQL Query:")
print("-" * 70)
print(query)
print("-" * 70)

try:
    print("\nExecuting query...")
    result = run_sparql(query, validate=False)
    bindings = result.get("results", {}).get("bindings", [])
    
    if bindings:
        print(f"\n✓ Found {len(bindings)} climate variables for year 2000:\n")
        for i, binding in enumerate(bindings, 1):
            prop = binding.get("property", {}).get("value", "N/A")
            avg = binding.get("avg_value", {}).get("value", "N/A")
            min_val = binding.get("min_value", {}).get("value", "N/A")
            max_val = binding.get("max_value", {}).get("value", "N/A")
            count = binding.get("count", {}).get("value", "0")
            unit = binding.get("unit", {}).get("value", "N/A")
            
            # Extract readable name from URI
            prop_name = prop.split("/")[-1].replace("_", " ").title()
            
            print(f"{i}. {prop_name}")
            print(f"   Average: {avg}")
            print(f"   Min: {min_val}, Max: {max_val}")
            print(f"   Unit: {unit}")
            print(f"   Count: {int(count):,}")
            print()
    else:
        print("✗ No data found")
        print(f"Result: {result}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Also test a simpler query to verify data exists for 2000
print("\n" + "=" * 70)
print("Verification: Count observations in 2000")
print("=" * 70)

simple_query = f"""
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT (COUNT(*) AS ?count)
FROM <{GRAPH}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:resultTime ?time .
  FILTER(?time >= "2000-01-01T00:00:00"^^xsd:dateTime && ?time < "2001-01-01T00:00:00"^^xsd:dateTime)
}}
"""

print(f"\nSimple count query:")
print("-" * 70)
print(simple_query)
print("-" * 70)

try:
    result = run_sparql(simple_query, validate=False)
    bindings = result.get("results", {}).get("bindings", [])
    if bindings:
        count = bindings[0].get("count", {}).get("value", "0")
        print(f"\n✓ Found {int(count):,} total observations in year 2000")
    else:
        print("✗ No count returned")
except Exception as e:
    print(f"✗ Error: {e}")
