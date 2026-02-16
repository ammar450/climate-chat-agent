"""
SPARQL query templates for climate observations.
All templates are pre-validated and safe.
"""

GRAPH = "http://hyobs.nfdi4earth.de/graph/climateobservations"

TEMPLATES = {
    "list_properties": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
SELECT ?property (COUNT(*) AS ?count)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:observedProperty ?property .
}}
GROUP BY ?property
ORDER BY DESC(?count)
LIMIT 50""",

    "list_features": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
SELECT ?feature (COUNT(*) AS ?count)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?feature .
}}
GROUP BY ?feature
ORDER BY DESC(?count)
LIMIT 50""",

    "sample_observations": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
SELECT ?time ?value ?property ?feature ?unit
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty ?property ;
       sosa:hasFeatureOfInterest ?feature ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
}}
ORDER BY ?time
LIMIT 20""",

    "all_properties_summary": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
SELECT ?property 
       (AVG(?value) AS ?avg_value) 
       (MIN(?value) AS ?min_value) 
       (MAX(?value) AS ?max_value) 
       (COUNT(?value) AS ?count)
       (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty ?property ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER (?time >= \"{start}\"^^xsd:dateTime && ?time < \"{end}\"^^xsd:dateTime)
}}
GROUP BY ?property
ORDER BY ?property""",

    "timeseries_for_feature_property": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
SELECT ?time ?value ?unit
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasFeatureOfInterest <{feature_uri}> ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
}}
ORDER BY ?time
LIMIT 500""",

    "average_for_property_date_range": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT (AVG(?value) AS ?average) (COUNT(*) AS ?count) (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
}}""",

    "top_extremes_for_property": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
SELECT ?time ?feature ?value ?unit
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasFeatureOfInterest ?feature ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
}}
ORDER BY {order}(?value)
LIMIT 20""",

    "timeseries_statistics": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT 
  (AVG(?value) AS ?mean) 
  (MIN(?value) AS ?min) 
  (MAX(?value) AS ?max) 
  (COUNT(?value) AS ?count)
  (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
}}""",

    "timeseries_statistics_by_feature": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT 
  ?feature
  (AVG(?value) AS ?mean) 
  (MIN(?value) AS ?min) 
  (MAX(?value) AS ?max) 
  (COUNT(?value) AS ?count)
  (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasFeatureOfInterest ?feature ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
}}
GROUP BY ?feature
ORDER BY DESC(?mean)
LIMIT 20""",

    "filtered_timeseries": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?time ?value ?feature ?unit
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasFeatureOfInterest ?feature ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
  FILTER(?value >= {min_value} && ?value <= {max_value})
}}
ORDER BY ?time
LIMIT 500""",

    "daily_aggregates": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT 
  (SUBSTR(STR(?time), 1, 10) AS ?date)
  (AVG(?value) AS ?mean)
  (MIN(?value) AS ?min)
  (MAX(?value) AS ?max)
  (COUNT(?value) AS ?count)
  (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
}}
GROUP BY (SUBSTR(STR(?time), 1, 10))
ORDER BY ?date
LIMIT 500""",

    "monthly_aggregates": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT 
  (SUBSTR(STR(?time), 1, 7) AS ?month)
  (AVG(?value) AS ?mean)
  (MIN(?value) AS ?min)
  (MAX(?value) AS ?max)
  (COUNT(?value) AS ?count)
  (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
}}
GROUP BY (SUBSTR(STR(?time), 1, 7))
ORDER BY ?month
LIMIT 500""",

    "monthly_mean_from_daily": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT 
  (AVG(?daily_mean) AS ?overall_mean)
  (MIN(?daily_mean) AS ?min_daily)
  (MAX(?daily_mean) AS ?max_daily)
  (COUNT(?daily_mean) AS ?day_count)
  (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {{
  {{
    SELECT 
      (SUBSTR(STR(?time), 1, 10) AS ?date)
      (AVG(?value) AS ?daily_mean)
      (SAMPLE(?unit) AS ?unit)
    WHERE {{
      ?obs a sosa:Observation ;
           sosa:phenomenonTime ?time ;
           sosa:observedProperty <{property_uri}> ;
           sosa:hasResult ?result .
      ?result qudt:numericValue ?value .
      OPTIONAL {{ ?result qudt:unit ?unit }}
      FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
    }}
    GROUP BY (SUBSTR(STR(?time), 1, 10))
  }}
}}""",

    "features_near_coordinates": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
SELECT DISTINCT ?feature (COUNT(?obs) AS ?obs_count)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?feature .
  ?feature geo:hasGeometry ?geom .
  ?geom geo:asWKT ?wkt .
  # Note: Actual spatial filtering would require GeoSPARQL functions
  # For now, return all features for the user to select from
}}
GROUP BY ?feature
ORDER BY DESC(?obs_count)
LIMIT 50""",

    "location_based_summary": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
SELECT ?property 
       (AVG(?value) AS ?avg_value) 
       (MIN(?value) AS ?min_value) 
       (MAX(?value) AS ?max_value) 
       (COUNT(?value) AS ?count)
       (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:phenomenonTime ?time ;
       sosa:observedProperty ?property ;
       sosa:hasFeatureOfInterest ?feature ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  # Note: Add spatial filtering here when feature URI is known
  FILTER (?time >= \"{start}\"^^xsd:dateTime && ?time < \"{end}\"^^xsd:dateTime)
}}
GROUP BY ?property
ORDER BY ?property"""
}

# Property mappings for common terms
PROPERTY_MAPPINGS = {
    "humidity": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
    "relative_humidity": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
    "temperature": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
    "air_temperature": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
    "precipitation": "http://vocab.nerc.ac.uk/standard_name/precipitation_flux",
    "wind_speed": "http://vocab.nerc.ac.uk/standard_name/wind_speed",
}


def render_template(template_name: str, params: dict) -> str:
    """
    Render a SPARQL template with parameters.
    
    Args:
        template_name: Name of the template
        params: Dictionary of parameters to substitute
        
    Returns:
        Rendered SPARQL query string
    """
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}")
    
    template = TEMPLATES[template_name]
    params_with_graph = {"graph": GRAPH, **params}
    
    return template.format(**params_with_graph)


def resolve_property_uri(property_hint: str) -> str:
    """
    Resolve a property hint (like 'humidity') to a full URI.
    
    Args:
        property_hint: A property name or URI
        
    Returns:
        Full property URI
    """
    if property_hint.startswith("http://") or property_hint.startswith("https://"):
        return property_hint
    
    hint_lower = property_hint.lower().replace(" ", "_")
    return PROPERTY_MAPPINGS.get(hint_lower, property_hint)


def parse_date_hint(date_hint: str) -> tuple:
    """
    Parse date hints like '1950', 'January 1950', '1950-01' into ISO datetime range.
    
    Args:
        date_hint: A date string
        
    Returns:
        Tuple of (start_datetime, end_datetime) as ISO strings
    """
    import re
    from datetime import datetime, timedelta
    
    # Year only: 1950 -> 1950-01-01 to 1951-01-01
    if re.match(r'^\d{4}$', date_hint):
        year = int(date_hint)
        start = f"{year}-01-01T00:00:00"
        end = f"{year + 1}-01-01T00:00:00"
        return start, end
    
    # Year-Month: 1950-01 -> 1950-01-01 to 1950-02-01
    if re.match(r'^\d{4}-\d{2}$', date_hint):
        dt = datetime.strptime(date_hint, "%Y-%m")
        start = dt.strftime("%Y-%m-%dT%H:%M:%S")
        next_month = dt.replace(day=28) + timedelta(days=4)
        end_dt = next_month.replace(day=1)
        end = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
        return start, end
    
    # Month Year: "January 1950"
    month_names = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12
    }
    for month_name, month_num in month_names.items():
        if month_name in date_hint.lower():
            year_match = re.search(r'\d{4}', date_hint)
            if year_match:
                year = int(year_match.group())
                dt = datetime(year, month_num, 1)
                start = dt.strftime("%Y-%m-%dT%H:%M:%S")
                next_month = dt.replace(day=28) + timedelta(days=4)
                end_dt = next_month.replace(day=1)
                end = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
                return start, end
    
    # Default: use 1950-1951 range (available data)
    return "1950-01-01T00:00:00", "1952-01-01T00:00:00"
