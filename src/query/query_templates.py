"""
SPARQL query templates for climate observations.
All templates are pre-validated and safe.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Load graph IRI from environment
GRAPH = os.getenv("GRAPH_IRI", "climateobservations/eobs-v31")

TEMPLATES = {
    "list_properties": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
SELECT DISTINCT ?property (COUNT(*) AS ?count)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:observedProperty ?property .
}}
GROUP BY ?property
ORDER BY DESC(?count)""",

    "list_features_of_interest": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
SELECT DISTINCT ?feature (COUNT(*) AS ?count)
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
       sosa:resultTime ?time ;
       sosa:observedProperty ?property ;
       sosa:hasFeatureOfInterest ?feature ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  {property_filter}
  {feature_filter}
}}
ORDER BY ?time
LIMIT {limit}""",

    "all_properties_summary": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?property 
       (AVG(?value) AS ?avg_value) 
       (MIN(?value) AS ?min_value) 
       (MAX(?value) AS ?max_value) 
       (COUNT(?value) AS ?count)
       (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {{
  {{
    SELECT ?property ?value ?unit
    WHERE {{
      ?obs a sosa:Observation ;
           sosa:resultTime ?time ;
           sosa:observedProperty ?property ;
           sosa:hasResult ?result .
      ?result qudt:numericValue ?value .
      OPTIONAL {{ ?result qudt:unit ?unit }}
      FILTER (?time >= \"{start}\"^^xsd:dateTime && ?time < \"{end}\"^^xsd:dateTime)
    }}
    LIMIT 1000000
  }}
}}
GROUP BY ?property
ORDER BY ?property""",

    "timeseries_for_feature_property": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
SELECT ?time ?value ?unit
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:resultTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasFeatureOfInterest <{feature_uri}> ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
}}
ORDER BY ?time
LIMIT 500""",

    "top_extremes_for_property": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?time ?feature ?value ?unit
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:resultTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasFeatureOfInterest ?feature ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
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
       sosa:resultTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
}}""",

    "timeseries_statistics_with_feature": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
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
       sosa:resultTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasFeatureOfInterest <{feature_uri}> ;
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
       sosa:resultTime ?time ;
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
       sosa:resultTime ?time ;
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
       sosa:resultTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
}}
GROUP BY (SUBSTR(STR(?time), 1, 10))
ORDER BY ?date
LIMIT 500""",

    "daily_aggregates_with_feature": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
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
       sosa:resultTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasFeatureOfInterest <{feature_uri}> ;
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
       sosa:resultTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
}}
GROUP BY (SUBSTR(STR(?time), 1, 7))
ORDER BY ?month
LIMIT 500""",

    "monthly_aggregates_with_feature": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
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
       sosa:resultTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasFeatureOfInterest <{feature_uri}> ;
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
           sosa:resultTime ?time ;
           sosa:observedProperty <{property_uri}> ;
           sosa:hasResult ?result .
      ?result qudt:numericValue ?value .
      OPTIONAL {{ ?result qudt:unit ?unit }}
      FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
    }}
    GROUP BY (SUBSTR(STR(?time), 1, 10))
  }}
}}""",

    "features_with_coordinates": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
SELECT DISTINCT ?feature ?lat ?lng ?geometry (COUNT(?obs) AS ?obs_count)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?feature .
  OPTIONAL {{ ?feature wgs84:lat ?lat }}
  OPTIONAL {{ ?feature wgs84:long ?lng }}
  OPTIONAL {{ 
    ?feature geo:hasGeometry ?geom .
    ?geom geo:asWKT ?geometry .
  }}
}}
GROUP BY ?feature ?lat ?lng ?geometry
ORDER BY DESC(?obs_count)
LIMIT 50""",

    "features_near_coordinates": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
SELECT DISTINCT ?feature ?lat ?lng ?geometry (COUNT(?obs) AS ?obs_count)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?feature .
  ?feature wgs84:lat ?lat ;
           wgs84:long ?lng .
  OPTIONAL {{ 
    ?feature geo:hasGeometry ?geom .
    ?geom geo:asWKT ?geometry .
  }}
  # Filter features within bounding box (if lat/lng provided)
  {lat_lng_filter}
}}
GROUP BY ?feature ?lat ?lng ?geometry
ORDER BY DESC(?obs_count)
LIMIT 50""",

    "location_based_summary": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
SELECT ?property ?feature ?lat ?lng
       (AVG(?value) AS ?avg_value) 
       (MIN(?value) AS ?min_value) 
       (MAX(?value) AS ?max_value) 
       (COUNT(?value) AS ?count)
       (SAMPLE(?unit) AS ?unit)
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:resultTime ?time ;
       sosa:observedProperty ?property ;
       sosa:hasFeatureOfInterest ?feature ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  OPTIONAL {{ ?feature wgs84:lat ?lat }}
  OPTIONAL {{ ?feature wgs84:long ?lng }}
  FILTER (?time >= \"{start}\"^^xsd:dateTime && ?time < \"{end}\"^^xsd:dateTime)
  {feature_filter}
}}
GROUP BY ?property ?feature ?lat ?lng
ORDER BY ?property""",

    "timeseries_with_location": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
SELECT ?time ?value ?unit ?feature ?lat ?lng
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:resultTime ?time ;
       sosa:observedProperty <{property_uri}> ;
       sosa:hasFeatureOfInterest ?feature ;
       sosa:hasResult ?result .
  ?result qudt:numericValue ?value .
  OPTIONAL {{ ?result qudt:unit ?unit }}
  OPTIONAL {{ ?feature wgs84:lat ?lat }}
  OPTIONAL {{ ?feature wgs84:long ?lng }}
  FILTER(?time >= "{start}"^^xsd:dateTime && ?time < "{end}"^^xsd:dateTime)
  {feature_filter}
}}
ORDER BY ?time
LIMIT 500""",

    "features_by_location": """PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
SELECT DISTINCT ?feature ?lat ?lng ?geometry
FROM <{graph}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?feature .
  ?feature wgs84:lat ?lat ;
           wgs84:long ?lng .
  OPTIONAL {{ 
    ?feature geo:hasGeometry ?geom .
    ?geom geo:asWKT ?geometry .
  }}
  FILTER(?lat >= {min_lat} && ?lat <= {max_lat})
  FILTER(?lng >= {min_lng} && ?lng <= {max_lng})
}}
LIMIT 100"""
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
    
    # Add filter parameters for optional filtering
    if "property_filter" not in params_with_graph:
        if "property_uri" in params_with_graph and params_with_graph["property_uri"]:
            params_with_graph["property_filter"] = f'FILTER(?property = <{params_with_graph["property_uri"]}>)'
        else:
            params_with_graph["property_filter"] = ""
    
    if "feature_filter" not in params_with_graph:
        if "feature_uri" in params_with_graph and params_with_graph["feature_uri"]:
            params_with_graph["feature_filter"] = f'FILTER(?feature = <{params_with_graph["feature_uri"]}>)'
        else:
            params_with_graph["feature_filter"] = ""
    
    # Add lat/lng filter for location-based queries
    if "lat_lng_filter" not in params_with_graph:
        if all(k in params_with_graph for k in ["min_lat", "max_lat", "min_lng", "max_lng"]):
            lat_filter = f'FILTER(?lat >= {params_with_graph["min_lat"]} && ?lat <= {params_with_graph["max_lat"]})'
            lng_filter = f'FILTER(?lng >= {params_with_graph["min_lng"]} && ?lng <= {params_with_graph["max_lng"]})'
            params_with_graph["lat_lng_filter"] = f'{lat_filter}\n  {lng_filter}'
        else:
            params_with_graph["lat_lng_filter"] = ""
    
    # Ensure limit is set and reasonable
    if "limit" not in params_with_graph:
        params_with_graph["limit"] = 20
    
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
    
    # Default: use 1950-2024 range (available data)
    return "1950-01-01T00:00:00", "2025-01-01T00:00:00"
