"""Generate final stats table for new graph."""
import sys; sys.path.insert(0, '.')
from src.query.sparql_client import run_sparql
G = 'climateobservations/eobs-v31'

print("=" * 65)
print("E-OBS v31 — FINAL GRAPH STATISTICS")
print("=" * 65)

# Total observations
r = run_sparql(f"PREFIX sosa: <http://www.w3.org/ns/sosa/> SELECT (COUNT(*) AS ?c) FROM <{G}> WHERE {{ ?obs a sosa:Observation }}", validate=False)
total = r['results']['bindings'][0]['c']['value']
print(f"Total Observations: {int(total):,}")

# Per property
props = [
    ("air_temperature", "Temperature"),
    ("precipitation_amount", "Precipitation"),
    ("relative_humidity", "Humidity"),
    ("wind_speed", "Wind Speed"),
    ("surface_downwelling_shortwave_flux_in_air", "Radiation"),
]
for p, label in props:
    r = run_sparql(f"PREFIX sosa: <http://www.w3.org/ns/sosa/> SELECT (COUNT(*) AS ?c) FROM <{G}> WHERE {{ ?obs a sosa:Observation ; sosa:observedProperty <http://vocab.nerc.ac.uk/standard_name/{p}> }}", validate=False)
    print(f"  {label}: {int(r['results']['bindings'][0]['c']['value']):,}")

# Grids
r = run_sparql(f"PREFIX sosa: <http://www.w3.org/ns/sosa/> SELECT (COUNT(*) AS ?c) FROM <{G}> WHERE {{ ?s a sosa:FeatureOfInterest }}", validate=False)
print(f"Grid Cells (FOIs): {int(r['results']['bindings'][0]['c']['value']):,}")

# Collections
r = run_sparql(f"SELECT (COUNT(*) AS ?c) FROM <{G}> WHERE {{ ?s a <http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#ObservationCollection> }}", validate=False)
print(f"Observation Collections: {int(r['results']['bindings'][0]['c']['value']):,}")

# Geometry
r = run_sparql(f"SELECT (COUNT(*) AS ?c) FROM <{G}> WHERE {{ ?s a <http://www.opengis.net/ont/geosparql#Geometry> }}", validate=False)
print(f"Geometry Features: {int(r['results']['bindings'][0]['c']['value']):,}")

# Types
r = run_sparql(f"SELECT DISTINCT ?type FROM <{G}> WHERE {{ ?s a ?type }} LIMIT 20", validate=False)
print("RDF Types:", ", ".join(row['type']['value'].split('/')[-1].split('#')[-1] for row in r['results']['bindings']))

print("\nSPARQL Timeout: 300s (removed 400s Virtuoso limit)")
print("Feature URI: https://w3id.org/climateobservations/eobs-v31/data/grid_{lat}p{dec}_{lng}p{dec}")
print("=" * 65)
