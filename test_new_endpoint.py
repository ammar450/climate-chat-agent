"""
Test the new SPARQL endpoint to find available graphs and data
"""
from SPARQLWrapper import SPARQLWrapper, JSON

ENDPOINT = "http://141.76.19.254:8890/sparql"

print(f"Testing endpoint: {ENDPOINT}")
print("=" * 70)

# Test 1: Basic connectivity
print("\nTEST 1: Endpoint Connectivity")
print("-" * 70)
try:
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery("SELECT * WHERE { ?s ?p ?o } LIMIT 1")
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(10)
    result = sparql.query().convert()
    print("✓ Endpoint is reachable and responding")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Test 2: List all available graphs
print("\nTEST 2: List Available Graphs")
print("-" * 70)
graphs_query = """
SELECT DISTINCT ?g (COUNT(*) AS ?triples)
WHERE {
  GRAPH ?g { ?s ?p ?o }
}
GROUP BY ?g
ORDER BY DESC(?triples)
LIMIT 50
"""
try:
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(graphs_query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(30)
    result = sparql.query().convert()
    bindings = result.get("results", {}).get("bindings", [])
    
    if bindings:
        print(f"Found {len(bindings)} graphs:\n")
        for i, binding in enumerate(bindings, 1):
            graph = binding.get("g", {}).get("value", "N/A")
            count = binding.get("triples", {}).get("value", "0")
            print(f"{i:2d}. {graph}")
            print(f"    Triples: {count:,}")
    else:
        print("No graphs found")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Check for climate/observation graphs specifically
print("\nTEST 3: Search for Climate/Observation Graphs")
print("-" * 70)
climate_graphs_query = """
SELECT DISTINCT ?g (COUNT(*) AS ?triples)
WHERE {
  GRAPH ?g { ?s ?p ?o }
  FILTER(CONTAINS(STR(?g), "climate") || CONTAINS(STR(?g), "obs") || CONTAINS(STR(?g), "eobs"))
}
GROUP BY ?g
ORDER BY DESC(?triples)
"""
try:
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(climate_graphs_query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(30)
    result = sparql.query().convert()
    bindings = result.get("results", {}).get("bindings", [])
    
    if bindings:
        print(f"Found {len(bindings)} climate-related graphs:\n")
        for binding in bindings:
            graph = binding.get("g", {}).get("value", "N/A")
            count = binding.get("triples", {}).get("value", "0")
            print(f"  - {graph}")
            print(f"    Triples: {count:,}")
    else:
        print("No climate-related graphs found")
except Exception as e:
    print(f"Note: {e}")

# Test 4: Check for SOSA Observations in different potential graphs
print("\nTEST 4: Check for SOSA Observations")
print("-" * 70)
test_graphs = [
    "http://eobs/gridded",
    "http://example.org/eobs",
    "climateobservations/eobs-v31",
    "http://hyobs.nfdi4earth.de/graph/climateobservations/eobs-v31",
    "http://hyobs.nfdi4earth.de/graph/climateobservations",
]

for test_graph in test_graphs:
    count_query = f"""
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    SELECT (COUNT(*) AS ?count)
    FROM <{test_graph}>
    WHERE {{
      ?obs a sosa:Observation .
    }}
    """
    try:
        sparql = SPARQLWrapper(ENDPOINT)
        sparql.setQuery(count_query)
        sparql.setReturnFormat(JSON)
        sparql.setTimeout(30)
        result = sparql.query().convert()
        bindings = result.get("results", {}).get("bindings", [])
        
        if bindings:
            count = bindings[0].get("count", {}).get("value", "0")
            if int(count) > 0:
                print(f"✓ {test_graph}")
                print(f"  Observations: {int(count):,}")
            else:
                print(f"✗ {test_graph}: 0 observations")
        else:
            print(f"✗ {test_graph}: No results")
    except Exception as e:
        print(f"✗ {test_graph}: {e}")

# Test 5: Check properties in the most likely graph
print("\nTEST 5: Check Properties in http://eobs/gridded")
print("-" * 70)
props_query = """
PREFIX sosa: <http://www.w3.org/ns/sosa/>
SELECT ?property (COUNT(*) AS ?count)
FROM <http://eobs/gridded>
WHERE {
  ?obs a sosa:Observation ;
       sosa:observedProperty ?property .
}
GROUP BY ?property
ORDER BY DESC(?count)
LIMIT 10
"""
try:
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(props_query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(30)
    result = sparql.query().convert()
    bindings = result.get("results", {}).get("bindings", [])
    
    if bindings:
        print(f"Found {len(bindings)} properties:\n")
        for binding in bindings:
            prop = binding.get("property", {}).get("value", "N/A")
            count = binding.get("count", {}).get("value", "0")
            print(f"  - {prop}")
            print(f"    Count: {int(count):,}")
    else:
        print("No properties found")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 70)
print("Testing complete!")
