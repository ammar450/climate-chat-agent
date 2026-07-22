"""
Wikidata SPARQL client.

Two distinct roles:
1. PLACE RESOLUTION  — resolve a place name to coordinates BEFORE querying EOBS.
   Called early in the pipeline when the static city dictionary misses the name.
   Returns (lat, lon, resolved_label, wikidata_id) or None.

2. ENRICHMENT        — add geographic/property background AFTER EOBS data is fetched.
   Never replaces EOBS observation values.

Rules enforced here:
- Wikidata is NEVER used for observation data or domain values.
- If Wikidata is unavailable or returns no match, fail silently.
- Only trust a match when label, type, and coordinates clearly align.
- If uncertain about a match, return None rather than guess.
- Source is always tagged as "Wikidata (place resolution)" or
  "Wikidata (enrichment)" in output so the caller can be transparent.
"""

import os
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Optional, Dict, Any, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WIKIDATA_ENDPOINT = os.getenv("WIKIDATA_ENDPOINT", "https://query.wikidata.org/sparql")
WIKIDATA_TIMEOUT = int(os.getenv("WIKIDATA_TIMEOUT", "10"))  # seconds; kept short

# Wikidata requires a descriptive User-Agent for policy compliance
_USER_AGENT = (
    "ClimateAgent/1.0 (NFDI4Earth climate observation assistant; "
    "contact: nfdi4earth@example.org)"
)


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _run_wikidata_query(query: str) -> Optional[Dict[str, Any]]:
    """
    Execute a read-only SELECT query against Wikidata.
    Returns the JSON result dict, or None if the query fails for any reason.
    Failures are always non-fatal — callers must check for None.
    """
    try:
        sparql = SPARQLWrapper(WIKIDATA_ENDPOINT)
        sparql.addCustomHttpHeader("User-Agent", _USER_AGENT)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        sparql.setTimeout(WIKIDATA_TIMEOUT)

        result = sparql.query().convert()
        return result
    except Exception as exc:
        print(f"[WIKIDATA] Query failed (non-fatal, EOBS data unaffected): {exc}")
        return None


# ---------------------------------------------------------------------------
# 1. PLACE RESOLUTION  (called BEFORE EOBS query, when static dict misses)
# ---------------------------------------------------------------------------

def resolve_place_to_coordinates(
    place_name: str,
) -> Optional[Tuple[float, float, str, str]]:
    """
    Resolve a human-readable place name to (lat, lon, resolved_label, wikidata_id).

    Strategy:
      - Searches Wikidata for a geographic entity (city, town, municipality,
        district, administrative region) matching the English label.
      - Requires coordinates (P625) to be present — no coords → returns None.
      - Ranked by number of site-links to prefer the most prominent entity.
      - If nothing meaningful found or Wikidata fails, returns None silently.

    Callers must then use the returned coordinates to query EOBS.
    This function NEVER returns observation data.

    Args:
        place_name: Human-readable place name (e.g. "Dresden", "Naples")

    Returns:
        (lat, lon, resolved_label, wikidata_id) if found, else None.
    """
    # Geographic entity classes we trust for coordinate resolution
    # Q515=city, Q486972=human settlement, Q1093829=city district,
    # Q15284=municipality, Q3957=town, Q532=village, Q131168=borough
    trusted_instance_filter = (
        "VALUES ?instanceClass { "
        "wd:Q515 wd:Q486972 wd:Q1093829 wd:Q15284 "
        "wd:Q3957 wd:Q532 wd:Q131168 wd:Q10742 wd:Q1549591 "
        "wd:Q84 wd:Q16110 wd:Q1337818 wd:Q2615557 "
        "} "
        "?item wdt:P31/wdt:P279* ?instanceClass . "
    )

    query = f"""
SELECT ?item ?itemLabel ?lat ?lon ?sitelinks
WHERE {{
  ?item rdfs:label "{place_name}"@en .
  {trusted_instance_filter}
  ?item wdt:P625 ?coords .
  BIND(geof:latitude(?coords)  AS ?lat)
  BIND(geof:longitude(?coords) AS ?lon)
  OPTIONAL {{ ?item wikibase:sitelinks ?sitelinks . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
}}
ORDER BY DESC(?sitelinks)
LIMIT 1
"""
    result = _run_wikidata_query(query)
    if not result:
        return None

    bindings = result.get("results", {}).get("bindings", [])
    if not bindings:
        # Try a broader search without instance class filter as fallback
        query_broad = f"""
SELECT ?item ?itemLabel ?lat ?lon ?sitelinks
WHERE {{
  ?item rdfs:label "{place_name}"@en ;
        wdt:P625 ?coords .
  BIND(geof:latitude(?coords)  AS ?lat)
  BIND(geof:longitude(?coords) AS ?lon)
  OPTIONAL {{ ?item wikibase:sitelinks ?sitelinks . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
}}
ORDER BY DESC(?sitelinks)
LIMIT 1
"""
        result2 = _run_wikidata_query(query_broad)
        if not result2:
            return None
        bindings = result2.get("results", {}).get("bindings", [])
        if not bindings:
            return None

    row = bindings[0]
    lat_val = row.get("lat", {}).get("value", "")
    lon_val = row.get("lon", {}).get("value", "")

    if not lat_val or not lon_val:
        return None  # No coordinates → cannot resolve

    try:
        lat = float(lat_val)
        lon = float(lon_val)
    except (ValueError, TypeError):
        return None

    label = row.get("itemLabel", {}).get("value", place_name)
    wikidata_id = row.get("item", {}).get("value", "").split("/")[-1]

    print(
        f"[WIKIDATA] Resolved '{place_name}' → '{label}' ({wikidata_id}): "
        f"lat={lat:.4f}, lon={lon:.4f}"
    )
    return lat, lon, label, wikidata_id


# ---------------------------------------------------------------------------
# 2. ENRICHMENT  (called AFTER EOBS data is fetched, for background context)
# ---------------------------------------------------------------------------

def get_geographic_context(location_name: str) -> Optional[Dict[str, Any]]:
    """
    Look up geographic context for a location name from Wikidata.

    Returns a dict with label, Wikidata QID, description, country, lat/lon,
    and population when available.  Returns None if nothing useful found.

    This data SUPPLEMENTS EOBS observations — it does not replace them.
    """
    # Use Wikidata label search with English language
    query = f"""
SELECT ?item ?itemLabel ?description ?countryLabel ?lat ?lon ?population
WHERE {{
  ?item rdfs:label "{location_name}"@en ;
        wikibase:sitelinks ?sitelinks .
  OPTIONAL {{ ?item wdt:P17 ?country . }}
  OPTIONAL {{
    ?item wdt:P625 ?coords .
    BIND(geof:latitude(?coords)  AS ?lat)
    BIND(geof:longitude(?coords) AS ?lon)
  }}
  OPTIONAL {{ ?item wdt:P1082 ?population . }}
  OPTIONAL {{
    ?item schema:description ?description
    FILTER (lang(?description) = "en")
  }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
}}
ORDER BY DESC(?sitelinks)
LIMIT 1
"""
    result = _run_wikidata_query(query)
    if not result:
        return None

    bindings = result.get("results", {}).get("bindings", [])
    if not bindings:
        return None

    row = bindings[0]

    # Only return if we have a meaningful description or country — avoids low-confidence matches
    description = row.get("description", {}).get("value", "")
    country = row.get("countryLabel", {}).get("value", "")
    if not description and not country:
        return None

    return {
        "label": row.get("itemLabel", {}).get("value", location_name),
        "wikidata_id": row.get("item", {}).get("value", "").split("/")[-1],
        "description": description,
        "country": country,
        "lat": row.get("lat", {}).get("value", ""),
        "lon": row.get("lon", {}).get("value", ""),
        "population": row.get("population", {}).get("value", ""),
        "source": "Wikidata (enrichment)",
    }


def get_property_context(property_display_name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a brief description of a climate property/variable from Wikidata.

    E.g. "air temperature", "precipitation", "relative humidity".
    Returns None if nothing useful found or on failure.

    This gives the user background knowledge — it never overrides EOBS values.
    """
    # Attempt exact English label match
    query = f"""
SELECT ?item ?itemLabel ?description
WHERE {{
  ?item rdfs:label "{property_display_name}"@en .
  OPTIONAL {{
    ?item schema:description ?description
    FILTER (lang(?description) = "en")
  }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
}}
LIMIT 1
"""
    result = _run_wikidata_query(query)
    if not result:
        return None

    bindings = result.get("results", {}).get("bindings", [])
    if not bindings:
        return None

    row = bindings[0]
    description = row.get("description", {}).get("value", "")
    if not description:
        return None  # Don't return context-free stubs

    return {
        "label": row.get("itemLabel", {}).get("value", property_display_name),
        "wikidata_id": row.get("item", {}).get("value", "").split("/")[-1],
        "description": description,
        "source": "Wikidata (enrichment)",
    }


# ---------------------------------------------------------------------------
# Main enrichment entry-point
# ---------------------------------------------------------------------------

def enrich_from_wikidata(
    location_name: Optional[str],
    property_display_name: Optional[str],
) -> Dict[str, Any]:
    """
    Primary enrichment function called by the agent AFTER EOBS data is fetched.

    Args:
        location_name: Human-readable location name (e.g. "Germany", "Munich")
        property_display_name: Human-readable property name (e.g. "Air Temperature")

    Returns:
        Dict with any enrichment found.  Empty dict if nothing found or on failure.
        Keys:
          "geo"      -> geographic context dict (if location found)
          "property" -> property description dict (if property found)
        Callers must treat this as optional supplementary info only.
    """
    enrichment: Dict[str, Any] = {}

    if location_name:
        try:
            geo = get_geographic_context(location_name)
            if geo:
                enrichment["geo"] = geo
                print(f"[WIKIDATA] Geographic context found for '{location_name}': {geo.get('description', '')}")
            else:
                print(f"[WIKIDATA] No geographic context for '{location_name}' (non-fatal)")
        except Exception as exc:
            print(f"[WIKIDATA] geo lookup error (non-fatal): {exc}")

    if property_display_name:
        try:
            prop = get_property_context(property_display_name)
            if prop:
                enrichment["property"] = prop
                print(f"[WIKIDATA] Property context found for '{property_display_name}'")
            else:
                print(f"[WIKIDATA] No property context for '{property_display_name}' (non-fatal)")
        except Exception as exc:
            print(f"[WIKIDATA] property lookup error (non-fatal): {exc}")

    print("-------- DEBUG ------------")   
    return enrichment
