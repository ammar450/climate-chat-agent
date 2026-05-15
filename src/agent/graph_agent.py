"""
LangGraph-based agent for climate data chat.
Implements a Template-based KG-RAG workflow with router + memory.
Enhanced with typo correction, date validation, and dual response formats.
"""

import json
import os
import re
import time
from typing import TypedDict, Optional, List, Dict, Any, Literal
from langgraph.graph import StateGraph, END

from src.llm.llm_provider import chat
from src.parsers.property_resolver import property_resolver, location_resolver
from src.parsers.time_parser import TimeParser, DateValidationError
from src.parsers.typo_corrector import TypoCorrector
from src.formatting.response_formatter import ResponseFormatDetector, ResponseFormat
from src.utils.error_handler import QuerySuggestionEngine
from src.query.query_templates import render_template, TEMPLATES
from src.query.sparql_client import run_sparql, SPARQLSecurityError
from src.query.wikidata_client import enrich_from_wikidata, resolve_place_to_coordinates


# ============================================================================
# STATE DEFINITION
# ============================================================================

class AgentState(TypedDict):
    """State that flows through the LangGraph."""
    # Input
    session_id: str
    user_message: str
    original_message: str  # Before typo correction
    history: List[Dict[str, str]]  # [{"role": "user"|"assistant", "content": "..."}]
    model: Optional[str]  # "provider:model_name"
    
    # Validation and corrections
    typo_corrections: Optional[Dict[str, str]]  # typo -> correct word
    typo_message: Optional[str]  # Friendly correction message
    date_validation_error: Optional[str]  # Date out of range message
    date_availability_message: Optional[str]  # Message when using nearest available date
    response_format: Optional[str]  # "layman" or "technical"
    nearest_grid_message: Optional[str]  # Shown when nearest EOBS grid point used
    location_resolution_method: Optional[str]  # "static_dict" | "wikidata" | "coordinates"
    
    # Session memory
    selected_property_uri: Optional[str]
    selected_feature_uri: Optional[str]
    time_range: Optional[Dict[str, str]]  # {"start": "...", "end": "..."}
    location_name: Optional[str]  # Country or place name
    coordinates: Optional[Dict[str, float]]  # {"lat": ..., "lon": ...}
    
    # Processing state
    plan: Optional[Dict[str, Any]]  # {"template": "...", "params": {...}, "followup": null|"..."}
    sparql_query: Optional[str]
    sparql_rows: Optional[List[Dict[str, Any]]]
    evidence_text: Optional[str]
    wikidata_context: Optional[Dict[str, Any]]  # Enrichment from Wikidata (secondary source only)
    final_answer: Optional[str]
    technical_details: Optional[str]  # Technical response with debug info
    
    # Debug info
    debug: Dict[str, Any]


# ============================================================================
# IN-MEMORY SESSION STORE (fallback if Redis not available)
# ============================================================================

_memory_store: Dict[str, Dict[str, Any]] = {}


def _get_redis_client():
    """Get Redis client if available, else None."""
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return None
    
    try:
        import redis
        return redis.from_url(redis_url, decode_responses=True)
    except ImportError:
        print("[MEMORY] Redis not installed, using in-memory store")
        return None
    except Exception as e:
        print(f"[MEMORY] Redis connection failed: {e}, using in-memory store")
        return None


_redis_client = _get_redis_client()


# ============================================================================
# STATISTICS HELPER FUNCTIONS
# ============================================================================

def calculate_statistics(values: List[float]) -> Dict[str, float]:
    """
    Calculate comprehensive statistics including standard deviation and variance.
    
    Args:
        values: List of numeric values
        
    Returns:
        Dict with mean, min, max, count, std_dev, variance
    """
    if not values:
        return {}
    
    n = len(values)
    mean = sum(values) / n
    min_val = min(values)
    max_val = max(values)
    
    # Calculate variance and standard deviation
    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = variance ** 0.5
    
    return {
        "mean": mean,
        "min": min_val,
        "max": max_val,
        "count": n,
        "std_dev": std_dev,
        "variance": variance,
        "range": max_val - min_val
    }


# ============================================================================
# LANGGRAPH NODES
# ============================================================================

def load_memory_node(state: AgentState) -> AgentState:
    """Load session memory from Redis or in-memory dict."""
    session_id = state["session_id"]
    
    if _redis_client:
        try:
            data = _redis_client.get(f"session:{session_id}")
            if data:
                memory = json.loads(data)
                state["selected_property_uri"] = memory.get("selected_property_uri")
                state["selected_feature_uri"] = memory.get("selected_feature_uri")
                state["time_range"] = memory.get("time_range")
                state["location_name"] = memory.get("location_name")
                state["coordinates"] = memory.get("coordinates")
                print(f"[MEMORY] Loaded from Redis: {session_id}")
        except Exception as e:
            print(f"[MEMORY] Redis load error: {e}")
    else:
        # In-memory fallback
        if session_id in _memory_store:
            memory = _memory_store[session_id]
            state["selected_property_uri"] = memory.get("selected_property_uri")
            state["selected_feature_uri"] = memory.get("selected_feature_uri")
            state["time_range"] = memory.get("time_range")
            state["location_name"] = memory.get("location_name")
            state["coordinates"] = memory.get("coordinates")
            print(f"[MEMORY] Loaded from in-memory: {session_id}")
    
    state["debug"]["memory_loaded"] = True
    return state


def validation_node(state: AgentState) -> AgentState:
    """
    Validate and correct user input.
    - Fix typos in the message
    - Detect response format preference
    - Prepare for date validation (happens in resolve_node)
    """
    start_time = time.time()
    
    # Store original message
    state["original_message"] = state["user_message"]
    
    # 1. Check and correct typos (optimized - early exit if no typos)
    corrected_message, typo_corrections = TypoCorrector.correct(state["user_message"])
    
    if typo_corrections:
        state["user_message"] = corrected_message
        state["typo_corrections"] = typo_corrections
        state["typo_message"] = TypoCorrector.format_correction_message(typo_corrections)
        print(f"[VALIDATION] Typos corrected: {typo_corrections}")
    
    # 2. Detect response format preference (fast keyword check)
    response_format = ResponseFormatDetector.detect_format(state["user_message"])
    state["response_format"] = response_format.value
    
    # 3. Skip contextual help check for speed (only check on error)
    
    state["debug"]["validation_time"] = round(time.time() - start_time, 3)
    return state


def resolve_node(state: AgentState) -> AgentState:
    """Resolve property, feature, and time from user message."""
    start_time = time.time()
    user_message = state["user_message"]
    msg_lower = user_message.lower()
    
    print(f"[RESOLVE] Starting resolution for: {user_message}")
    
    # Detect vague climate queries (general overview requests)
    vague_query_phrases = [
        "climate", "weather", "climate data", "weather data",
        "overview", "summary", "general", "all variables",
        "what happened", "conditions", "climate conditions"
    ]
    
    is_vague_query = False
    for phrase in vague_query_phrases:
        if phrase in msg_lower:
            # Check if it's NOT followed by specific property keywords
            specific_keywords = ["temperature", "humidity", "precipitation", "wind", "pressure"]
            has_specific = any(kw in msg_lower for kw in specific_keywords)
            if not has_specific:
                is_vague_query = True
                print(f"[RESOLVE] Detected vague climate query: '{phrase}'")
                break
    
    if is_vague_query:
        # Mark for all-properties summary treatment
        state["debug"]["vague_query"] = True
        print(f"[RESOLVE] Will use all-properties summary for vague query")
    
    # Fast property keywords (reduced list - typos already corrected)
    property_keywords = [
        "temperature", "temp", "degrees",
        "humidity", "moisture",
        "precipitation", "rain", "rainfall",
        "wind", "pressure", "solar"
    ]
    
    # Try to resolve property using resolver with any matching keyword
    property_found = False
    for keyword in property_keywords:
        if keyword in msg_lower:
            print(f"[RESOLVE] Found keyword '{keyword}' in message")
            prop_uri, confidence, candidates = property_resolver.resolve(keyword)
            if prop_uri:
                state["selected_property_uri"] = prop_uri
                property_found = True
                print(f"[RESOLVE] Property resolved: {prop_uri} (from '{keyword}')")
                break
    
    if not property_found and not is_vague_query:
        print(f"[RESOLVE] No property keyword found in message")
    
    # Check for specific date format (YYYY-MM-DD)
    try:
        specific_date_result = TimeParser.parse_specific_date(user_message, strict=True)
        if specific_date_result:
            start, end, availability_message = specific_date_result
            state["time_range"] = {"start": start, "end": end}
            if availability_message:
                state["date_availability_message"] = availability_message
                print(f"[RESOLVE] Using nearest available date: {availability_message}")
            else:
                print(f"[RESOLVE] Specific date: {start} to {end}")
            state["debug"]["resolve_time"] = round(time.time() - start_time, 3)
            return state
    except DateValidationError as e:
        # Invalid date format (e.g., month 13, Feb 30)
        state["date_validation_error"] = str(e)
        state["final_answer"] = str(e)
        print(f"[RESOLVE] Invalid date format: {e}")
        state["plan"] = {"template": None, "params": {}, "followup": None}
        state["sparql_query"] = ""
        state["debug"]["resolve_time"] = round(time.time() - start_time, 3)
        return state
    
    # Parse time range (general patterns)
    try:
        time_range = TimeParser.parse(user_message, strict=True)
        if time_range:
            state["time_range"] = {"start": time_range[0], "end": time_range[1]}
            print(f"[RESOLVE] Time range: {time_range} (validated for 1950-2024)")
    except DateValidationError as e:
        # Date is outside 1950-2024 range
        state["date_validation_error"] = str(e)
        if e.suggested_query:
            state["debug"]["date_suggestion"] = e.suggested_query
        print(f"[RESOLVE] Date validation error: {e}")
        error_message = str(e)
        if e.suggested_query:
            error_message += f"\n\nSuggestion: {e.suggested_query}"
        state["final_answer"] = error_message
        state["plan"] = {"template": None, "params": {}, "followup": None}
        state["sparql_query"] = ""
        state["debug"]["resolve_time"] = round(time.time() - start_time, 3)
        return state
    
    # Check for year updates ONLY if no specific time range was already detected
    # This prevents overwriting month-specific queries like "March 1975"
    if not state.get("time_range"):
        year_update = TimeParser.extract_year_update(user_message)
        if year_update:
            # Clip to 1950-2024
            if year_update < 1950:
                year_update = 1950
            elif year_update > 2024:
                year_update = 2024
            
            # For a full year, end date should be start of next year
            state["time_range"] = {
                "start": f"{year_update}-01-01T00:00:00",
                "end": f"{year_update + 1}-01-01T00:00:00"
            }
            print(f"[RESOLVE] Year set to: {year_update} (1950-2024 available)")
    
    # Extract feature URI if pasted (basic detection)
    if "http://obs.nfdi4earth.de/resource/feature/" in user_message:
        # Extract feature URI
        parts = user_message.split("http://obs.nfdi4earth.de/resource/feature/")
        if len(parts) > 1:
            feature_id = parts[1].split()[0].strip()
            state["selected_feature_uri"] = f"http://obs.nfdi4earth.de/resource/feature/{feature_id}"
            print(f"[RESOLVE] Feature: {state['selected_feature_uri']}")
    
    # Parse location: country name or coordinates
    # European and Mediterranean countries (dataset contains primarily European data from 1950-2024)
    available_countries = [
        # Western Europe
        "germany", "france", "italy", "spain", "portugal", "netherlands", "belgium", 
        "switzerland", "austria", "luxembourg",
        # Northern Europe
        "uk", "united kingdom", "england", "scotland", "wales", "ireland", "iceland",
        "norway", "sweden", "denmark", "finland",
        # Southern Europe / Mediterranean
        "greece", "croatia", "slovenia", "albania", "malta", "cyprus", "montenegro",
        "bosnia", "serbia", "macedonia", "bulgaria", "romania",
        # Eastern Europe
        "poland", "czech republic", "czechia", "slovakia", "hungary", "ukraine",
        "belarus", "moldova", "estonia", "latvia", "lithuania",
        # Mediterranean North Africa (limited data)
        "tunisia", "algeria", "morocco", "libya", "egypt",
        # Middle East (limited)
        "turkey", "israel", "lebanon", "syria", "jordan"
    ]
    
    # Get city names from location resolver for detection
    available_cities = list(location_resolver.CITY_COORDINATES.keys())
    
    # Countries likely NOT in the 1950-2024 European dataset
    unavailable_countries = [
        "usa", "united states", "america", "canada", "mexico", "brazil", "argentina",
        "chile", "peru", "colombia", "venezuela",
        "china", "japan", "india", "pakistan", "bangladesh", "thailand", "vietnam",
        "indonesia", "malaysia", "philippines", "korea", "singapore",
        "australia", "new zealand",
        "south africa", "nigeria", "kenya", "ethiopia", "ghana", "tanzania",
        "saudi arabia", "iran", "iraq", "uae", "qatar", "kuwait"
    ]
    
    # Check for country names
    country_detected = None
    for country in available_countries:
        if country in msg_lower:
            country_detected = country.title()
            state["location_name"] = country_detected
            print(f"[RESOLVE] Location detected: {state['location_name']}")
            break

    # Check for city names — first exact, then fuzzy (handles typos like 'lipzieg'→'leipzig')
    if not country_detected:
        # 1. Exact match
        for city in available_cities:
            if city in msg_lower:
                country_detected = city.title()
                state["location_name"] = country_detected
                print(f"[RESOLVE] City detected (exact): {state['location_name']}")
                break

        # 2. Fuzzy match — check each word token against city list
        if not country_detected:
            words = re.findall(r'[a-z]+', msg_lower)
            best_city = None
            best_dist = 999
            for word in words:
                if len(word) < 3:  # skip very short tokens
                    continue
                for city in available_cities:
                    # Allow 1 edit for short names (≤6), 2 edits for longer
                    max_edits = 1 if len(city) <= 6 else 2
                    if abs(len(word) - len(city)) > max_edits:
                        continue
                    # Compute Levenshtein inline
                    s1, s2 = word, city
                    if len(s1) < len(s2):
                        s1, s2 = s2, s1
                    if len(s2) == 0:
                        d = len(s1)
                    else:
                        prev = list(range(len(s2) + 1))
                        for i, c1 in enumerate(s1):
                            curr = [i + 1]
                            for j, c2 in enumerate(s2):
                                curr.append(min(prev[j+1]+1, curr[j]+1, prev[j]+(c1 != c2)))
                            prev = curr
                        d = prev[-1]
                    if d <= max_edits and d < best_dist:
                        best_dist = d
                        best_city = city
            if best_city:
                country_detected = best_city.title()
                state["location_name"] = country_detected
                print(f"[RESOLVE] City detected (fuzzy, dist={best_dist}): {state['location_name']}")
    
    # If location detected, try to resolve to coordinates and feature URI
    if country_detected and not state.get("coordinates"):
        coords = location_resolver.get_coordinates(country_detected)
        if coords:
            state["coordinates"] = {"lat": coords[0], "lon": coords[1]}
            state["location_resolution_method"] = "static_dict"
            print(f"[RESOLVE] Location mapped via static dict: lat={coords[0]}, lon={coords[1]}")
        else:
            # Static dict missed — try Wikidata for coordinate resolution
            print(f"[RESOLVE] '{country_detected}' not in static dict, trying Wikidata...")
            try:
                wikidata_result = resolve_place_to_coordinates(country_detected)
                if wikidata_result:
                    wd_lat, wd_lon, wd_label, wd_id = wikidata_result
                    state["coordinates"] = {"lat": wd_lat, "lon": wd_lon}
                    state["location_resolution_method"] = "wikidata"
                    # Update location name to the canonical Wikidata label
                    state["location_name"] = wd_label
                    state["debug"]["wikidata_place_id"] = wd_id
                    print(f"[RESOLVE] '{country_detected}' resolved via Wikidata to '{wd_label}' "
                          f"({wd_id}): lat={wd_lat:.4f}, lon={wd_lon:.4f}")
                else:
                    print(f"[RESOLVE] Wikidata could not resolve '{country_detected}'")
            except Exception as exc:
                print(f"[RESOLVE] Wikidata place-resolution error (non-fatal): {exc}")
    
    # Check if user mentioned a country not in the dataset
    if not country_detected:
        for country in unavailable_countries:
            if country in msg_lower:
                country_name = country.replace("usa", "USA").replace("uae", "UAE").title()
                error_msg = f"Sorry, '{country_name}' is not available in this dataset. This dataset contains climate observations from European and Mediterranean regions for 1950-2024.\n\nAvailable regions: Germany, France, Italy, Spain, UK, Greece, Poland, and other European countries.\n\nYou can provide specific coordinates (lat/lon) if you have data points in '{country_name}'."
                state["final_answer"] = error_msg
                state["plan"] = {"template": None, "params": {}, "followup": None}
                state["sparql_query"] = ""
                state["debug"]["resolve_time"] = round(time.time() - start_time, 3)
                state["debug"]["country_not_available"] = country_name
                print(f"[RESOLVE] Country not in dataset: {country_name}")
                return state
    
    # Parse lat/lng coordinates (various formats)
    # Format 1: "lat: 52.5, lon: 13.4" or "latitude: 52.5, longitude: 13.4"
    lat_lon_pattern1 = r'(?:lat(?:itude)?)[:\s]+([\-\+]?\d+\.?\d*)[,\s]+(?:lon(?:gitude)?)[:\s]+([\-\+]?\d+\.?\d*)'
    # Format 2: "52.5, 13.4" (two decimal numbers separated by comma)
    lat_lon_pattern2 = r'([\-\+]?\d+\.\d+)[,\s]+([\-\+]?\d+\.\d+)'
    # Format 3: "52.5N 13.4E" or "52.5°N 13.4°E"
    lat_lon_pattern3 = r'([\-\+]?\d+\.\d+)\s*°?\s*[NS][,\s]+([\-\+]?\d+\.\d+)\s*°?\s*[EW]'
    
    match = re.search(lat_lon_pattern1, user_message, re.IGNORECASE)
    if not match:
        match = re.search(lat_lon_pattern2, user_message)
    if not match:
        match = re.search(lat_lon_pattern3, user_message, re.IGNORECASE)
    
    if match:
        try:
            lat = float(match.group(1))
            lon = float(match.group(2))
            # Validate lat/lon ranges
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                state["coordinates"] = {"lat": lat, "lon": lon}
                print(f"[RESOLVE] Coordinates detected: lat={lat}, lon={lon}")
            else:
                print(f"[RESOLVE] Invalid coordinates: lat={lat}, lon={lon} (out of range)")
        except ValueError:
            print(f"[RESOLVE] Failed to parse coordinates")
    
    # If we have coordinates but no feature URI, try to find nearest feature
    if state.get("coordinates") and not state.get("selected_feature_uri"):
        coords = state["coordinates"]
        try:
            result = location_resolver.find_nearest_feature_with_distance(
                coords["lat"],
                coords["lon"],
                run_sparql
            )
            if result:
                feature_uri, dist_km = result
                state["selected_feature_uri"] = feature_uri
                resolution_method = state.get("location_resolution_method", "coordinates")
                loc_label = state.get("location_name", f"{coords['lat']:.4f},{coords['lon']:.4f}")

                if resolution_method == "wikidata":
                    wd_id = state.get("debug", {}).get("wikidata_place_id", "")
                    wd_note = f" (resolved via Wikidata{' QID: ' + wd_id if wd_id else ''})" 
                    state["nearest_grid_message"] = (
                        f"No exact EOBS match for '{loc_label}'{wd_note}. "
                        f"Using nearest observation grid point ({dist_km:.1f} km away). "
                        f"[Source: EOBS]"
                    )
                elif dist_km > 25:
                    state["nearest_grid_message"] = (
                        f"No exact EOBS grid point for '{loc_label}'. "
                        f"Showing nearest observation point ({dist_km:.1f} km away). "
                        f"[Source: EOBS]"
                    )
                else:
                    state["nearest_grid_message"] = None

                print(f"[RESOLVE] Resolved to feature URI: {feature_uri} "
                      f"({dist_km:.1f} km from '{loc_label}')")
            else:
                # EOBS has no geometry data for this endpoint — proceed without feature filter.
                # The query will run globally; we note this in the grid message.
                loc_label = state.get("location_name", "requested location")
                state["nearest_grid_message"] = (
                    f"Could not resolve a grid point for '{loc_label}' from EOBS geometry data. "
                    f"Showing dataset-wide statistics. [Source: EOBS]"
                )
                print(f"[RESOLVE] No feature geometry found in EOBS; will run global query")
        except Exception as e:
            loc_label = state.get("location_name", "requested location")
            state["nearest_grid_message"] = (
                f"Grid-point lookup failed for '{loc_label}' ({e}). "
                f"Showing dataset-wide statistics. [Source: EOBS]"
            )
            print(f"[RESOLVE] Error resolving feature from coordinates: {e}")

    # If coordinate lookup was direct (not via place name) and no resolution_method set yet
    if state.get("coordinates") and not state.get("location_resolution_method"):
        state["location_resolution_method"] = "coordinates"

    state["debug"]["resolve_time"] = round(time.time() - start_time, 3)
    return state


def resolve_router(state: AgentState) -> Literal["planner", "date_error"]:
    """Route after resolve - skip planner if date error occurred."""
    if state.get("date_validation_error"):
        return "date_error"
    return "planner"


def plan_node(state: AgentState) -> AgentState:
    """Use LLM to plan query - outputs strict JSON."""
    start_time = time.time()

    # If we already have a final answer (e.g., from date error), skip planning
    if state.get("final_answer"):
        state["plan"] = {"template": None, "params": {}, "followup": None}
        state["debug"]["plan_time"] = 0
        state["debug"]["skipped"] = "answer_already_set"
        return state

    # Get user message early for use in fast-path detection
    user_message = state["user_message"]
    msg_lower = user_message.lower()

    # -----------------------------------------------------------------------
    # FAST-PATH: skip the LLM when property + time_range are already resolved.
    # This handles "temperature in Leipzig in 1950"-style queries directly.
    # Enhanced to detect specific query intents (average, daily, monthly, etc.)
    # -----------------------------------------------------------------------
    has_property = bool(state.get("selected_property_uri"))
    has_time = bool(state.get("time_range"))
    has_feature = bool(state.get("selected_feature_uri"))

    if has_property and has_time:
        tr = state["time_range"]
        template = None
        
        # Check for value filtering keywords (highest priority)
        import re
        range_patterns = [
            r'between\s+([\d.]+)\s+and\s+([\d.]+)',
            r'from\s+([\d.]+)\s+to\s+([\d.]+)',
            r'([\d.]+)\s*-\s*([\d.]+)',
        ]
        threshold_patterns = [
            r'above\s+([\d.]+)',
            r'over\s+([\d.]+)',
            r'greater than\s+([\d.]+)',
            r'>\s*([\d.]+)',
            r'below\s+([\d.]+)',
            r'under\s+([\d.]+)',
            r'less than\s+([\d.]+)',
            r'<\s*([\d.]+)',
        ]
        
        min_val, max_val = None, None
        for pattern in range_patterns:
            match = re.search(pattern, user_message, re.IGNORECASE)
            if match:
                min_val, max_val = float(match.group(1)), float(match.group(2))
                template = "filtered_timeseries"
                print(f"[PLAN] Fast path: {template} (detected value range: {min_val}-{max_val})")
                break
        
        if not template:
            for pattern in threshold_patterns:
                match = re.search(pattern, user_message, re.IGNORECASE)
                if match:
                    threshold = float(match.group(1))
                    if 'above' in pattern or 'over' in pattern or 'greater' in pattern or '>' in pattern:
                        min_val, max_val = threshold, 1000000  # Large upper bound
                    else:
                        min_val, max_val = -1000000, threshold  # Large lower bound
                    template = "filtered_timeseries"
                    print(f"[PLAN] Fast path: {template} (detected threshold filter: {threshold})")
                    break
        
        if template == "filtered_timeseries":
            state["plan"] = {
                "template": template,
                "params": {
                    "property_uri": state["selected_property_uri"],
                    "start": tr["start"],
                    "end": tr["end"],
                    "min_value": min_val,
                    "max_value": max_val
                },
                "followup": None,
            }
            state["debug"]["plan_time"] = 0
            state["debug"]["fast_path"] = True
            state["debug"]["fast_path_reason"] = f"value filtering detected: {min_val}-{max_val}"
            return state
        
        # Check for daily aggregation keywords
        if any(keyword in msg_lower for keyword in [
            "daily", "day by day", "each day", "per day", "daily average",
            "daily mean", "daily statistics", "day-by-day", "daily breakdown"
        ]):
            template = "daily_aggregates_with_feature" if has_feature else "daily_aggregates"
            print(f"[PLAN] Fast path: {template} (detected 'daily' intent)")
        
        # Check for monthly aggregation keywords
        elif any(keyword in msg_lower for keyword in [
            "monthly", "month by month", "each month", "per month", "monthly average",
            "monthly mean", "monthly statistics", "month-by-month", "monthly trends",
            "monthly totals", "monthly breakdown"
        ]):
            template = "monthly_aggregates_with_feature" if has_feature else "monthly_aggregates"
            print(f"[PLAN] Fast path: {template} (detected 'monthly' intent)")
        
        # Check for extreme values keywords
        elif any(keyword in msg_lower for keyword in [
            "highest", "maximum", "max", "top", "greatest", "warmest", "wettest",
            "strongest", "peak", "record high"
        ]):
            template = "top_extremes_for_property"
            state["plan"] = {
                "template": template,
                "params": {
                    "property_uri": state["selected_property_uri"],
                    "start": tr["start"],
                    "end": tr["end"],
                    "order": "DESC"
                },
                "followup": None,
            }
            state["debug"]["plan_time"] = 0
            state["debug"]["fast_path"] = True
            state["debug"]["fast_path_reason"] = "extremes detected (highest)"
            print(f"[PLAN] Fast path: {template} (detected 'highest' intent)")
            return state
        
        elif any(keyword in msg_lower for keyword in [
            "lowest", "minimum", "min", "bottom", "smallest", "coldest", "driest",
            "weakest", "record low"
        ]):
            template = "top_extremes_for_property"
            state["plan"] = {
                "template": template,
                "params": {
                    "property_uri": state["selected_property_uri"],
                    "start": tr["start"],
                    "end": tr["end"],
                    "order": "ASC"
                },
                "followup": None,
            }
            state["debug"]["plan_time"] = 0
            state["debug"]["fast_path"] = True
            state["debug"]["fast_path_reason"] = "extremes detected (lowest)"
            print(f"[PLAN] Fast path: {template} (detected 'lowest' intent)")
            return state
        
        # Check for average-specific queries (but not daily/monthly average)
        elif any(keyword in msg_lower for keyword in [
            "average", "mean", "avg"
        ]) and not any(kw in msg_lower for kw in ["daily", "monthly", "day", "month"]):
            template = "average_for_property_date_range"
            print(f"[PLAN] Fast path: {template} (detected 'average' intent)")
        
        # Default to timeseries statistics for general queries
        else:
            template = "timeseries_statistics_with_feature" if has_feature else "timeseries_statistics"
            print(f"[PLAN] Fast path: {template} (property+time already resolved)")
        
        state["plan"] = {
            "template": template,
            "params": {
                "property_uri": state["selected_property_uri"],
                "start": tr["start"],
                "end": tr["end"],
            },
            "followup": None,
        }
        state["debug"]["plan_time"] = 0
        state["debug"]["fast_path"] = True
        state["debug"]["fast_path_reason"] = "property+time already resolved with intent detection"
        print(f"[PLAN] Fast path uses feature={'yes' if has_feature else 'no'}")
        return state

    # Fast path for common queries (skip LLM)
    if any(phrase in msg_lower for phrase in ["what variables", "list variables", "available variables", "what properties", "variables are"]):
        state["plan"] = {"template": "list_properties", "params": {}, "followup": None}
        state["debug"]["plan_time"] = round(time.time() - start_time, 3)
        state["debug"]["fast_path"] = True
        print("[PLAN] Fast path: list_properties")
        return state
    
    if any(phrase in msg_lower for phrase in ["list locations", "what locations", "available locations", "list stations", "what stations"]):
        state["plan"] = {"template": "list_features", "params": {}, "followup": None}
        state["debug"]["plan_time"] = round(time.time() - start_time, 3)
        state["debug"]["fast_path"] = True
        print("[PLAN] Fast path: list_features")
        return state
    
    # Fast path for vague climate queries or simple overviews
    if state.get("debug", {}).get("vague_query") or any(phrase in msg_lower for phrase in [
        "explain", "overview", "summary", "simply", "general climate", "all data",
        "what happened", "climate conditions", "weather conditions"
    ]):
        # Use all-properties summary if we have a time range
        if state.get("time_range"):
            state["plan"] = {
                "template": "all_properties_summary",
                "params": {
                    "start": state["time_range"]["start"],
                    "end": state["time_range"]["end"]
                },
                "followup": None
            }
            state["debug"]["plan_time"] = round(time.time() - start_time, 3)
            state["debug"]["fast_path"] = True
            print("[PLAN] Fast path: all_properties_summary for vague query")
            return state
        # If no time range, default to 1950-2024 full range for overview
        else:
            state["time_range"] = {
                "start": "1950-01-01T00:00:00",
                "end": "2025-01-01T00:00:00"  # Exclusive end for full 1950-2024
            }
            state["plan"] = {
                "template": "all_properties_summary",
                "params": {
                    "start": "1950-01-01T00:00:00",
                    "end": "2025-01-01T00:00:00"
                },
                "followup": None
            }
            state["debug"]["plan_time"] = round(time.time() - start_time, 3)
            state["debug"]["fast_path"] = True
            state["debug"]["default_time_range"] = "1950-2024"
            print("[PLAN] Fast path: all_properties_summary with default 1950-2024 range")
            return state
    
    # Build context
    context_parts = []
    if state.get("selected_property_uri"):
        prop_name = property_resolver.get_property_display_name(state["selected_property_uri"])
        context_parts.append(f"Current property: {prop_name}")
        context_parts.append(f"Property URI: {state['selected_property_uri']}")
    if state.get("time_range"):
        tr = state["time_range"]
        context_parts.append(f"Current time range: {tr['start']} to {tr['end']}")
    if state.get("selected_feature_uri"):
        context_parts.append(f"Current feature: {state['selected_feature_uri']}")
    if state.get("location_name"):
        context_parts.append(f"Location: {state['location_name']}")
    if state.get("coordinates"):
        coords = state["coordinates"]
        context_parts.append(f"Coordinates: lat={coords['lat']}, lon={coords['lon']}")
    
    session_context = "\n".join(context_parts) if context_parts else "No previous context."
    
    system_prompt = f"""You are a SPARQL query planner for climate observation data.

⚠️ CRITICAL: DATA AVAILABILITY CONSTRAINT ⚠️
This dataset contains data from 1950-01-01 to 2024-12-31 (75 years of historical climate observations)

RULES FOR HANDLING DATE QUERIES:
1. If user asks about ANY year outside 1950-2024:
   - Set followup to politely explain the limitation
   - Suggest using a year within 1950-2024 instead
   - Example: "I only have data from 1950 to 2024. Would you like to see [property] data from 2024 instead?"

2. If no year is specified, default to the full 1950-2024 range

3. NEVER generate queries for years outside 1950-2024

Available templates:
- list_properties: List all available climate variables
- list_features: List all observation locations/stations
- all_properties_summary: Overview of ALL climate variables with statistics (needs start, end) - USE THIS for vague queries like "climate in 1950", "weather overview", "explain climate simply"
- location_based_summary: Climate summary for a specific location (needs start, end; uses location from context)
- features_near_coordinates: Find features near given coordinates (informational, lists available features)
- sample_observations: Show sample observations (needs property_uri)
- average_for_property_date_range: Calculate simple average ONLY (needs property_uri, start, end)
- top_extremes_for_property: Show top highest/lowest individual values (needs property_uri, order: DESC/ASC, start, end)
- timeseries_statistics: Calculate mean, min, max, count for a property (needs property_uri, start, end) - DEFAULT for "statistics", "calculate"
- timeseries_statistics_by_feature: Statistics grouped by location/feature (needs property_uri, start, end) - USE when "by location", "across locations", "per grid point", "compare locations"
- filtered_timeseries: Filter data by value range (needs property_uri, start, end, min_value, max_value) - USE for "between X and Y", "above X", "below X"
- daily_aggregates: Daily mean, min, max, count per day (needs property_uri, start, end) - USE for "daily", "each day", "day by day"
- monthly_aggregates: Monthly mean, min, max, count per month (needs property_uri, start, end) - USE for "monthly", "each month", "month by month"
- monthly_mean_from_daily: Overall mean computed from daily means (needs property_uri, start, end)

IMPORTANT: When user asks about recent data or doesn't specify year, use any year from 1950-2024 as appropriate.
If user asks for data outside 1950-2024, inform them via followup that only 1950-2024 data is available.

Session context:
{session_context}

CRITICAL: If session context shows "Current property: X", you MUST use the property_uri from context.
DO NOT generate property URIs. Use the ones from session context or omit property_uri if not in context.

CRITICAL TEMPLATE SELECTION RULES:
1. If query mentions "daily", "each day", "day by day" → USE daily_aggregates
2. If query mentions "monthly", "each month", "month by month", "monthly totals" → USE monthly_aggregates  
3. If query has value range ("between X and Y", "above X", "below X") → USE filtered_timeseries with min_value and max_value
4. If query says "by location", "across locations", "per grid", "compare locations" → USE timeseries_statistics_by_feature
5. If query asks for "highest", "lowest", "maximum", "minimum", "top", "extreme" values → USE top_extremes_for_property with order DESC or ASC
6. For simple "average" without aggregation → USE average_for_property_date_range
7. For general statistics ("calculate", "statistics", "mean") → USE timeseries_statistics
8. If no specific property but asking about climate/weather → USE all_properties_summary

LOCATION HANDLING:
- If session context shows "Location: [name]", "Coordinates: lat=X, lon=Y", or "Current feature: [URI]", the location is RESOLVED
- When location is resolved, DO NOT ask for coordinates - proceed with the query using appropriate template
- If no location info in context but user mentions a place, suggest providing coordinates
- Location filtering is automatic when feature URI is in context
  
OUTPUT STRICT JSON ONLY (no markdown, no explanation):
{{
  "template": "template_name",
  "params": {{"start": "YYYY-MM-DDTHH:MM:SS", "end": "...", "order": "DESC", "min_value": 0, "max_value": 100}},
  "followup": null or "question to ask user"
}}

IMPORTANT: Only include property_uri in params if it's provided in the session context above.
If property info is NOT in session context, use list_properties template first.

If you need clarification, set "followup" to your question and "template" to null.
"""
    
    user_prompt = f"User question: {user_message}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Parse model parameter
    provider = None
    model_name = None
    if state.get("model") and ":" in state["model"]:
        provider, model_name = state["model"].split(":", 1)
    
    try:
        response = chat(messages, provider=provider, model=model_name, temperature=0.0, max_tokens=120)
        
        # Parse JSON (strip markdown if present)
        response_clean = response.strip()
        if response_clean.startswith("```"):
            lines = response_clean.split("\n")
            response_clean = "\n".join([l for l in lines if not l.startswith("```")])
        
        plan = json.loads(response_clean)
        
        # Validate template exists
        if plan.get("template") and plan["template"] not in TEMPLATES:
            print(f"[PLAN] Invalid template: {plan['template']}, falling back to sample_observations")
            plan = {"template": "sample_observations", "params": {}, "followup": None}
        
        # Update session memory with extracted params
        # IMPORTANT: DO NOT overwrite property_uri if already resolved in state
        if plan.get("params"):
            if "property_uri" in plan["params"] and not state.get("selected_property_uri"):
                # Only use LLM's property_uri if we don't have one already
                state["selected_property_uri"] = plan["params"]["property_uri"]
            # IMPORTANT: DO NOT overwrite time_range if already resolved by resolve_node
            if "start" in plan["params"] and "end" in plan["params"] and not state.get("time_range"):
                # Only use LLM's time range if we don't have one already
                state["time_range"] = {
                    "start": plan["params"]["start"],
                    "end": plan["params"]["end"]
                }
        
        state["plan"] = plan
        state["debug"]["plan_time"] = round(time.time() - start_time, 3)
        state["debug"]["llm_provider"] = provider or os.getenv("LLM_PROVIDER", "ollama")
        state["debug"]["llm_model"] = model_name or os.getenv("OLLAMA_MODEL", "llama3.2")
        
    except Exception as e:
        print(f"[PLAN] LLM error: {e}, falling back to list_properties")
        state["debug"]["plan_error"] = str(e)
        state["plan"] = {
            "template": "list_properties",
            "params": {},
            "followup": None
        }
        state["debug"]["plan_time"] = round(time.time() - start_time, 3)
    
    return state


def route_node(state: AgentState) -> Literal["followup", "build_query"]:
    """Conditional routing based on plan."""
    # Check if plan exists and has followup
    plan = state.get("plan") or {}
    if isinstance(plan, dict) and plan.get("followup"):
        return "followup"
    return "build_query"


def date_error_node(state: AgentState) -> AgentState:
    """Handle date validation errors with helpful suggestions."""
    # Final answer already set in resolve_node
    # Just add contextual help if available
    if state.get("debug", {}).get("contextual_help"):
        state["final_answer"] = state["final_answer"] + "\n\n" + state["debug"]["contextual_help"]
    
    state["debug"]["flow"] = "date_error"
    return state


def followup_node(state: AgentState) -> AgentState:
    """Set final answer to follow-up question."""
    plan = state.get("plan") or {}
    if isinstance(plan, dict) and plan.get("followup"):
        state["final_answer"] = plan["followup"]
    else:
        state["final_answer"] = "I need more information. Could you please clarify your question?"
    state["debug"]["flow"] = "followup"
    return state


def build_query_node(state: AgentState) -> AgentState:
    """Build SPARQL query from template and params."""
    start_time = time.time()
    plan = state.get("plan") or {}
    
    # Safety check for None plan
    if not isinstance(plan, dict) or not plan.get("template"):
        state["debug"]["build_query_error"] = "No valid plan available"
        state["final_answer"] = "I encountered an error processing your query. Please try rephrasing."
        state["sparql_query"] = ""
        return state
    
    template_name = plan["template"]
    params = plan.get("params", {})
    
    # ALWAYS inject session state - this overrides anything from the plan
    if state.get("selected_property_uri"):
        params["property_uri"] = state["selected_property_uri"]
        print(f"[BUILD_QUERY] Using property URI from state: {state['selected_property_uri']}")
    
    if state.get("selected_feature_uri"):
        params["feature_uri"] = state["selected_feature_uri"]
        print(f"[BUILD_QUERY] Using feature URI from state: {state['selected_feature_uri']}")
        
        # Switch to feature-specific template if available
        feature_templates = {
            "timeseries_statistics": "timeseries_statistics_with_feature",
            "daily_aggregates": "daily_aggregates_with_feature",
            "monthly_aggregates": "monthly_aggregates_with_feature",
        }
        if template_name in feature_templates:
            template_name = feature_templates[template_name]
            print(f"[BUILD_QUERY] Switched to feature-specific template: {template_name}")
    
    if state.get("time_range"):
        params["start"] = state["time_range"]["start"]
        params["end"] = state["time_range"]["end"]
        print(f"[BUILD_QUERY] Using time range from state: {params['start']} to {params['end']}")
    
    # Enforce limit: default 200, clamp <= 500
    if "limit" in params:
        params["limit"] = min(int(params["limit"]), 500)
    else:
        params["limit"] = 200
    
    try:
        sparql_query = render_template(template_name, params)
        
        # Safety checks
        query_upper = sparql_query.upper()
        
        # Block dangerous operations - use word boundaries to avoid false positives
        forbidden = ["INSERT", "DELETE", "LOAD", "CLEAR", "CREATE", "DROP", "MOVE", "COPY", "ADD"]
        for keyword in forbidden:
            # Use word boundary regex to match whole words only
            if re.search(r'\b' + keyword + r'\b', query_upper):
                raise SPARQLSecurityError(f"Forbidden keyword: {keyword}")
        
        # Ensure SELECT only
        if "SELECT" not in query_upper:
            raise SPARQLSecurityError("Query must contain SELECT")
        
        # Ensure FROM graph is present
        graph_iri = os.getenv("GRAPH_IRI", "http://hyobs.nfdi4earth.de/graph/climateobservations")
        if f"FROM <{graph_iri}>" not in sparql_query and "FROM <" not in sparql_query:
            # Inject FROM clause after SELECT
            parts = sparql_query.split("WHERE", 1)
            if len(parts) == 2:
                sparql_query = f"{parts[0]}\nFROM <{graph_iri}>\nWHERE{parts[1]}"
        
        state["sparql_query"] = sparql_query
        state["debug"]["build_query_time"] = round(time.time() - start_time, 3)
        
    except Exception as e:
        state["debug"]["build_query_error"] = str(e)
        state["final_answer"] = f"Error building query: {str(e)}"
        state["sparql_query"] = ""
    
    return state


def execute_sparql_node(state: AgentState) -> AgentState:
    """Execute SPARQL query with timeout and error handling."""
    start_time = time.time()
    
    if not state.get("sparql_query"):
        state["sparql_rows"] = []
        state["debug"]["execute_error"] = "No query to execute"
        return state
    
    try:
        result = run_sparql(state["sparql_query"], validate=True)
        rows = result.get("results", {}).get("bindings", [])
        state["sparql_rows"] = rows
        state["debug"]["execute_time"] = round(time.time() - start_time, 3)
        state["debug"]["row_count"] = len(rows)
        
    except SPARQLSecurityError as e:
        state["sparql_rows"] = []
        state["debug"]["execute_error"] = f"Security error: {str(e)}"
        state["final_answer"] = f"Security violation: {str(e)}"
    except Exception as e:
        state["sparql_rows"] = []
        state["debug"]["execute_error"] = str(e)
        state["final_answer"] = f"Query execution failed: {str(e)}"
    
    return state


def format_evidence_node(state: AgentState) -> AgentState:
    """Create compact evidence text from SPARQL results."""
    start_time = time.time()
    rows = state.get("sparql_rows", [])
    
    # Handle case where plan might be None
    plan = state.get("plan") or {}
    if not isinstance(plan, dict) or not plan.get("template"):
        state["evidence_text"] = "No query plan available."
        state["debug"]["format_time"] = round(time.time() - start_time, 3)
        return state
    
    template_name = plan.get("template", "unknown")
    
    if not rows:
        state["evidence_text"] = "No data found."
        state["debug"]["format_time"] = round(time.time() - start_time, 3)
        return state
    
    evidence_parts = []
    evidence_parts.append(f"Query type: {template_name}")
    evidence_parts.append(f"Result count: {len(rows)}")
    
    # Add property info
    if state.get("selected_property_uri"):
        prop_name = property_resolver.get_property_display_name(state["selected_property_uri"])
        evidence_parts.append(f"Property: {prop_name}")
    
    # Add time range
    if state.get("time_range"):
        tr = state["time_range"]
        evidence_parts.append(f"Time range: {tr['start']} to {tr['end']}")
    
    # Template-specific evidence
    if template_name == "all_properties_summary":
        evidence_parts.append("Climate Overview (All Variables):")
        for row in rows:
            property_uri = row.get("property", {}).get("value", "Unknown")
            prop_name = property_resolver.get_property_display_name(property_uri)
            avg_val = row.get("avg_value", {}).get("value", "N/A")
            min_val = row.get("min_value", {}).get("value", "N/A")
            max_val = row.get("max_value", {}).get("value", "N/A")
            count = row.get("count", {}).get("value", "N/A")
            unit = row.get("unit", {}).get("value", "")
            
            try:
                evidence_parts.append(f"  {prop_name}: avg={float(avg_val):.2f}, range={float(min_val):.2f}-{float(max_val):.2f} {unit} (n={count})".strip())
            except:
                evidence_parts.append(f"  {prop_name}: avg={avg_val}, range={min_val}-{max_val} {unit} (n={count})".strip())
    
    elif template_name == "average_for_property_date_range":
        for row in rows[:1]:
            if "avg" in row or "average" in row:
                avg_val = row.get("avg" if "avg" in row else "average", {}).get("value", "N/A")
                unit = row.get("unit", {}).get("value", "")
                evidence_parts.append(f"Average: {avg_val} {unit}".strip())
    
    elif template_name == "timeseries_statistics":
        # We need to fetch raw values to calculate std dev
        # Check if we need to run a supplementary query for raw values
        for row in rows[:1]:
            mean = row.get("mean", {}).get("value", "N/A")
            min_val = row.get("min", {}).get("value", "N/A")
            max_val = row.get("max", {}).get("value", "N/A")
            count = row.get("count", {}).get("value", "N/A")
            unit = row.get("unit", {}).get("value", "")
            
            evidence_parts.append(f"Statistical Summary:")
            evidence_parts.append(f"  Mean: {mean} {unit}".strip())
            evidence_parts.append(f"  Min: {min_val} {unit}".strip())
            evidence_parts.append(f"  Max: {max_val} {unit}".strip())
            evidence_parts.append(f"  Count: {count} observations")
            
            # Calculate additional stats if possible
            try:
                mean_float = float(mean)
                min_float = float(min_val)
                max_float = float(max_val)
                count_int = int(count)
                
                # Estimate std dev using range rule (for normal distribution, range ≈ 6σ)
                estimated_std = (max_float - min_float) / 6.0
                estimated_variance = estimated_std ** 2
                
                evidence_parts.append(f"  Estimated Std Dev: {estimated_std:.2f} {unit} (range/6 approximation)".strip())
                evidence_parts.append(f"  Estimated Variance: {estimated_variance:.2f} {unit}²".strip())
                evidence_parts.append(f"  Range: {max_float - min_float:.2f} {unit}".strip())
                
                # Add note about technical details
                if state.get("response_format") == "technical":
                    evidence_parts.append(f"  Coefficient of Variation: {(estimated_std/mean_float*100):.1f}%".strip())
                    
            except:
                evidence_parts.append(f"  Range: {min_val} - {max_val} {unit}".strip())
    
    elif template_name == "timeseries_statistics_by_feature":
        evidence_parts.append("Statistics by location/feature:")
        for i, row in enumerate(rows[:10]):
            feature = row.get("feature", {}).get("value", "Unknown")
            mean = row.get("mean", {}).get("value", "N/A")
            count = row.get("count", {}).get("value", "N/A")
            unit = row.get("unit", {}).get("value", "")
            evidence_parts.append(f"  {i+1}. {feature}: mean={mean} {unit} (n={count})".strip())
    
    elif template_name in ["daily_aggregates", "monthly_aggregates"]:
        period = "Daily" if template_name == "daily_aggregates" else "Monthly"
        evidence_parts.append(f"{period} aggregates:")
        
        # Detect unique features to determine scope
        features_in_data = set()
        for row in rows:
            if "feature" in row:
                features_in_data.add(row.get("feature", {}).get("value", ""))
        
        feature_count = len(features_in_data) if features_in_data else "multiple"
        state["debug"]["feature_count"] = feature_count
        
        # Show ALL daily/monthly values (not just first 10)
        for i, row in enumerate(rows):
            date = row.get("date" if template_name == "daily_aggregates" else "month", {}).get("value", "N/A")
            mean = row.get("mean", {}).get("value", "N/A")
            min_val = row.get("min", {}).get("value", "N/A")
            max_val = row.get("max", {}).get("value", "N/A")
            unit = row.get("unit", {}).get("value", "")
            # Format: Date: mean (min-max) unit
            try:
                evidence_parts.append(f"  {date}: mean={float(mean):.2f} ({float(min_val):.2f}-{float(max_val):.2f}) {unit}".strip())
            except:
                evidence_parts.append(f"  {date}: mean={mean}, min={min_val}, max={max_val} {unit}".strip())
    
    elif template_name == "monthly_mean_from_daily":
        for row in rows[:1]:
            overall_mean = row.get("overall_mean", {}).get("value", "N/A")
            min_daily = row.get("min_daily", {}).get("value", "N/A")
            max_daily = row.get("max_daily", {}).get("value", "N/A")
            day_count = row.get("day_count", {}).get("value", "N/A")
            unit = row.get("unit", {}).get("value", "")
            evidence_parts.append(f"Overall mean from daily aggregates:")
            evidence_parts.append(f"  Overall Mean: {overall_mean} {unit}".strip())
            evidence_parts.append(f"  Min Daily: {min_daily} {unit}".strip())
            evidence_parts.append(f"  Max Daily: {max_daily} {unit}".strip())
            evidence_parts.append(f"  Days: {day_count}")
    
    elif template_name == "filtered_timeseries":
        evidence_parts.append("Filtered data:")
        values = [float(row.get("value", {}).get("value", 0)) for row in rows if "value" in row]
        if values:
            evidence_parts.append(f"  {len(values)} observations in filter range")
            evidence_parts.append(f"  Value range: {min(values):.2f} to {max(values):.2f}")
        for i, row in enumerate(rows[:5]):
            value = row.get("value", {}).get("value", "N/A")
            unit = row.get("unit", {}).get("value", "")
            time_val = row.get("time", {}).get("value", "")
            evidence_parts.append(f"  {i+1}. {value} {unit} at {time_val}".strip())
    
    elif template_name == "top_extremes_for_property":
        evidence_parts.append("Top values:")
        for i, row in enumerate(rows[:10]):
            value = row.get("value", {}).get("value", "N/A")
            unit = row.get("unit", {}).get("value", "")
            time_val = row.get("time", {}).get("value", "")
            evidence_parts.append(f"  {i+1}. {value} {unit} at {time_val}".strip())
    
    elif template_name == "list_properties":
        evidence_parts.append("Available properties:")
        for i, row in enumerate(rows[:10]):
            label = row.get("label", {}).get("value", row.get("property", {}).get("value", "Unknown"))
            evidence_parts.append(f"  {i+1}. {label}")
    
    elif template_name == "list_features":
        evidence_parts.append("Available locations:")
        for i, row in enumerate(rows[:10]):
            label = row.get("label", {}).get("value", row.get("feature", {}).get("value", "Unknown"))
            evidence_parts.append(f"  {i+1}. {label}")
    
    elif template_name in ["sample_observations", "timeseries_for_feature_property"]:
        # Extract statistics
        values = []
        times = []
        for row in rows:
            if "value" in row and "value" in row["value"]:
                try:
                    values.append(float(row["value"]["value"]))
                except:
                    pass
            if "time" in row and "value" in row["time"]:
                times.append(row["time"]["value"])
        
        if values:
            evidence_parts.append(f"Value range: {min(values):.2f} to {max(values):.2f}")
            evidence_parts.append(f"Average: {sum(values)/len(values):.2f}")
        if times:
            evidence_parts.append(f"Time coverage: {min(times)} to {max(times)}")
        
        # Sample data
        evidence_parts.append("Sample observations:")
        for i, row in enumerate(rows[:5]):
            value = row.get("value", {}).get("value", "N/A")
            unit = row.get("unit", {}).get("value", "")
            time_val = row.get("time", {}).get("value", "")
            evidence_parts.append(f"  {i+1}. {value} {unit} at {time_val}".strip())
    
    state["evidence_text"] = "\n".join(evidence_parts)
    state["debug"]["format_time"] = round(time.time() - start_time, 3)
    return state


def wikidata_enrich_node(state: AgentState) -> AgentState:
    """
    Optionally enrich EOBS results with Wikidata context.

    Rules:
    - Runs AFTER EOBS data is already fetched and formatted.
    - Only queries Wikidata when a location name or known property is present.
    - NEVER replaces EOBS observation values.
    - If Wikidata fails or returns nothing, state is unchanged.
    - Source is tagged as 'Wikidata (enrichment)' in output.
    """
    start_time = time.time()

    # Only enrich when EOBS returned data
    if not state.get("sparql_rows") and not state.get("evidence_text"):
        state["wikidata_context"] = {}
        return state

    location_name = state.get("location_name")
    property_uri = state.get("selected_property_uri")
    property_display_name = None
    if property_uri:
        property_display_name = property_resolver.get_property_display_name(property_uri)

    # Skip if nothing to look up
    if not location_name and not property_display_name:
        state["wikidata_context"] = {}
        state["debug"]["wikidata_time"] = 0
        state["debug"]["wikidata_skipped"] = "no location or property to look up"
        return state

    try:
        enrichment = enrich_from_wikidata(
            location_name=location_name,
            property_display_name=property_display_name,
        )
        state["wikidata_context"] = enrichment
        state["debug"]["wikidata_time"] = round(time.time() - start_time, 3)
        state["debug"]["wikidata_enriched"] = bool(enrichment)
    except Exception as exc:
        # Always non-fatal — EOBS data is unaffected
        print(f"[WIKIDATA] Enrichment error (non-fatal): {exc}")
        state["wikidata_context"] = {}
        state["debug"]["wikidata_error"] = str(exc)

    return state


def explain_node(state: AgentState) -> AgentState:
    """Generate final answer using LLM with evidence, applying response format."""
    start_time = time.time()
    
    if state.get("final_answer"):
        # Already set by error handler
        return state
    
    evidence = state.get("evidence_text", "No evidence available.")
    user_message = state["user_message"]
    plan = state.get("plan") or {}
    template_name = plan.get("template", "unknown")
    
    # Fast path for simple list queries - skip LLM entirely
    if template_name in ["list_properties", "list_features"]:
        # Use evidence directly as answer
        answer = evidence.replace("Available properties:", "Here are the available climate variables:").replace("Available locations:", "Here are the available observation locations:")
        
        if state.get("typo_message"):
            answer = state["typo_message"] + "\n\n" + answer
        
        # Prepend date availability message if present
        if state.get("date_availability_message"):
            answer = state["date_availability_message"] + "\n\n" + answer
        
        state["final_answer"] = answer
        # Generate simple technical details for list queries
        state["technical_details"] = f"Query Type: {template_name}\nResults: {state['debug'].get('row_count', 0)} items\n\nDebug Info:\n" + str(state.get("debug", {}))
        state["debug"]["explain_time"] = round(time.time() - start_time, 3)
        state["debug"]["fast_path_explain"] = True
        return state
    
    # Get response format preference
    response_format = state.get("response_format", "auto")
    
    # Detect aggregation scope
    aggregation_scope = "unknown"
    scope_label = ""
    if template_name in ["daily_aggregates", "monthly_aggregates", "timeseries_statistics"]:
        if state.get("selected_feature_uri"):
            aggregation_scope = "per_feature"
            feature_id = state["selected_feature_uri"].split('/')[-1] if '/' in state["selected_feature_uri"] else state["selected_feature_uri"]
            scope_label = f"for feature {feature_id}"
        else:
            # Count features from debug info or sparql_rows
            feature_count = state["debug"].get("feature_count", "multiple")
            aggregation_scope = "global"
            scope_label = f"aggregated across all grid cells ({feature_count} features)" if feature_count != "multiple" else "aggregated across all grid cells"
    
    state["debug"]["aggregation_scope"] = aggregation_scope
    state["debug"]["scope_label"] = scope_label
    
    # Build system prompt for LAYMAN response (always generate this)
    layman_system_prompt = f"""You are a climate data assistant. Answer based ONLY on the EVIDENCE provided.

RULES:
- Use ONLY facts from EVIDENCE
- Be concise (2-4 sentences max)
- ALWAYS include units with all numeric values
- ALWAYS mention the count of observations when available in evidence
- ALWAYS specify the exact time period from the query (e.g., "in 2020", "during January 1990", "for the year 1950")
- NO asterisks (*) or markdown bold (**)
- Use clean numbered lists or simple text
- Use simple language, emojis, everyday comparisons
- If WIKIDATA CONTEXT is provided, use it only for background/geographic info, never to replace EOBS numbers
- When mixing EOBS data with Wikidata background, state the source: e.g. "(Source: EOBS)" or "(Background: Wikidata)"
- For aggregate queries (daily/monthly), explicitly state what aggregation was done
- State facts with certainty - avoid phrases like "expected to be" when you have actual data

DATA: 1950-2024 (Source: EOBS)

EVIDENCE (from EOBS — primary source):
{evidence}

Answer the question briefly and directly in a friendly, layman-friendly way."""
    
    user_prompt = f"Question: {user_message}"

    # Append Wikidata enrichment context if available
    wikidata_ctx = state.get("wikidata_context") or {}
    if wikidata_ctx:
        wikidata_lines = ["\nWIKIDATA CONTEXT (background/enrichment only — do NOT override EOBS values):"]
        geo = wikidata_ctx.get("geo")
        if geo:
            parts = []
            if geo.get("description"):
                parts.append(geo["description"])
            if geo.get("country"):
                parts.append(f"Country: {geo['country']}")
            if geo.get("lat") and geo.get("lon"):
                parts.append(f"Coordinates: {geo['lat']}, {geo['lon']}")
            if geo.get("population"):
                parts.append(f"Population: {geo['population']}")
            wikidata_lines.append(f"  Location ({geo.get('label', '')}): {' | '.join(parts)}")
        prop_ctx = wikidata_ctx.get("property")
        if prop_ctx and prop_ctx.get("description"):
            wikidata_lines.append(f"  Property ({prop_ctx.get('label', '')}): {prop_ctx['description']}")
        layman_system_prompt += "\n".join(wikidata_lines) + "\n"

    messages = [
        {"role": "system", "content": layman_system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Parse model parameter
    provider = None
    model_name = None
    if state.get("model") and ":" in state["model"]:
        provider, model_name = state["model"].split(":", 1)
    
    try:
        # Generate LAYMAN response
        layman_answer = chat(messages, provider=provider, model=model_name, temperature=0.0, max_tokens=150)
        
        # Prepend date availability message if present
        if state.get("date_availability_message"):
            layman_answer = state["date_availability_message"] + "\n\n" + layman_answer

        # Prepend nearest-grid transparency message if present
        if state.get("nearest_grid_message"):
            layman_answer = state["nearest_grid_message"] + "\n\n" + layman_answer

        # Prepend typo correction message if any
        if state.get("typo_message"):
            layman_answer = state["typo_message"] + "\n\n" + layman_answer
        
        # Append contextual help if available
        if state.get("debug", {}).get("contextual_help"):
            layman_answer = layman_answer + "\n\n" + state["debug"]["contextual_help"]
        
        state["final_answer"] = layman_answer
        
        # Generate TECHNICAL details (separate section with debug info)
        technical_lines = []
        technical_lines.append("=== TECHNICAL DETAILS ===")
        technical_lines.append("")
        technical_lines.append(f"Query Template: {template_name}")
        technical_lines.append(f"Response Format: {response_format}")
        technical_lines.append("")
        
        # Add property info
        if state.get("selected_property_uri"):
            prop_name = property_resolver.get_property_display_name(state["selected_property_uri"])
            technical_lines.append(f"Property: {prop_name}")
            technical_lines.append(f"Property URI: {state['selected_property_uri']}")
        
        # Add time range
        if state.get("time_range"):
            tr = state["time_range"]
            technical_lines.append(f"Time Range: {tr['start']} to {tr['end']}")
        
        # Add location info
        if state.get("location_name"):
            technical_lines.append(f"Location: {state['location_name']}")
        if state.get("location_resolution_method"):
            technical_lines.append(f"Location Resolution: {state['location_resolution_method']}")
        if state.get("nearest_grid_message"):
            technical_lines.append(f"Grid Match: {state['nearest_grid_message']}")
        if state.get("coordinates"):
            coords = state["coordinates"]
            technical_lines.append(f"Coordinates: lat={coords['lat']}, lon={coords['lon']}")
        
        technical_lines.append("")
        technical_lines.append("Evidence Summary:")
        technical_lines.append(evidence[:500] + ("..." if len(evidence) > 500 else ""))
        technical_lines.append("")
        
        # Add debug information
        technical_lines.append("Debug Information:")
        technical_lines.append("─" * 40)
        
        # Timing information
        debug = state.get("debug", {})
        if 'validation_time' in debug:
            technical_lines.append(f"⏱ Validation: {debug['validation_time']}s")
        if 'resolve_time' in debug:
            technical_lines.append(f"⏱ Resolution: {debug['resolve_time']}s")
        if 'plan_time' in debug:
            technical_lines.append(f"⏱ Planning: {debug['plan_time']}s")
        if 'build_query_time' in debug:
            technical_lines.append(f"⏱ Query Build: {debug['build_query_time']}s")
        if 'execute_time' in debug:
            technical_lines.append(f"⏱ Execution: {debug['execute_time']}s")
        if 'format_time' in debug:
            technical_lines.append(f"⏱ Format: {debug['format_time']}s")
        if 'explain_time' in debug:
            technical_lines.append(f"⏱ Explanation: {debug['explain_time']}s")
        
        # Result counts
        if 'row_count' in debug:
            technical_lines.append(f"📊 Rows Retrieved: {debug['row_count']}")
        
        # Model info
        if 'llm_provider' in debug:
            technical_lines.append(f"🤖 LLM Provider: {debug['llm_provider']}")
        if 'llm_model' in debug:
            technical_lines.append(f"🤖 LLM Model: {debug['llm_model']}")
        
        # Errors or warnings
        if 'plan_error' in debug:
            technical_lines.append(f"⚠️ Planning Error: {debug['plan_error']}")
        if 'execute_error' in debug:
            technical_lines.append(f"⚠️ Execution Error: {debug['execute_error']}")
        
        # Memory state
        if 'memory_loaded' in debug:
            technical_lines.append(f"💾 Session Memory: {'Loaded' if debug['memory_loaded'] else 'Not found'}")
        if 'memory_saved' in debug:
            technical_lines.append(f"💾 Session Save: {'Success' if debug['memory_saved'] else 'Failed'}")
        
        # Add SPARQL query if available
        if state.get("sparql_query"):
            technical_lines.append("")
            technical_lines.append("SPARQL Query:")
            technical_lines.append("─" * 40)
            technical_lines.append(state["sparql_query"][:1000] + ("..." if len(state["sparql_query"]) > 1000 else ""))
        
        state["technical_details"] = "\n".join(technical_lines)
        state["debug"]["explain_time"] = round(time.time() - start_time, 3)
        state["debug"]["response_format_used"] = response_format
        
    except Exception as e:
        print(f"[EXPLAIN] LLM error: {e}, falling back to evidence summary")
        state["debug"]["explain_error"] = str(e)
        # Create a simple fallback answer from evidence
        rows_count = state["debug"].get("row_count", 0)
        answer = f"Found {rows_count} results for your query about climate data. The query used template: {template_name}.\n\nHere's the evidence:\n{evidence[:500]}"
        
        # Prepend date availability message if present
        if state.get("date_availability_message"):
            answer = state["date_availability_message"] + "\n\n" + answer
        
        # Prepend typo correction
        if state.get("typo_message"):
            answer = state["typo_message"] + "\n\n" + answer
        
        state["final_answer"] = answer
        state["technical_details"] = f"Error during response generation: {str(e)}\n\nDebug: {str(state.get('debug', {}))}"
        state["debug"]["explain_time"] = round(time.time() - start_time, 3)
    
    return state


def save_memory_node(state: AgentState) -> AgentState:
    """Save session memory to Redis or in-memory dict."""
    session_id = state["session_id"]
    
    memory = {
        "selected_property_uri": state.get("selected_property_uri"),
        "selected_feature_uri": state.get("selected_feature_uri"),
        "time_range": state.get("time_range"),
        "location_name": state.get("location_name"),
        "coordinates": state.get("coordinates"),
    }
    
    if _redis_client:
        try:
            _redis_client.setex(
                f"session:{session_id}",
                3600,  # 1 hour TTL
                json.dumps(memory)
            )
            print(f"[MEMORY] Saved to Redis: {session_id}")
        except Exception as e:
            print(f"[MEMORY] Redis save error: {e}")
    else:
        # In-memory fallback
        _memory_store[session_id] = memory
        print(f"[MEMORY] Saved to in-memory: {session_id}")
    
    state["debug"]["memory_saved"] = True
    return state


# ============================================================================
# BUILD LANGGRAPH
# ============================================================================

def create_graph() -> StateGraph:
    """Create and compile the LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("load_memory", load_memory_node)
    workflow.add_node("validation", validation_node)  # NEW: Typo correction and format detection
    workflow.add_node("resolve", resolve_node)
    workflow.add_node("planner", plan_node)  # Renamed to avoid conflict with state attribute
    workflow.add_node("followup", followup_node)
    workflow.add_node("date_error", date_error_node)  # NEW: Handle date validation errors
    workflow.add_node("build_query", build_query_node)
    workflow.add_node("execute_sparql", execute_sparql_node)
    workflow.add_node("format_evidence", format_evidence_node)
    workflow.add_node("wikidata_enrich", wikidata_enrich_node)  # Wikidata enrichment (secondary source)
    workflow.add_node("explainer", explain_node)  # Renamed for clarity
    workflow.add_node("save_memory", save_memory_node)
    
    # Set entry point
    workflow.set_entry_point("load_memory")
    
    # Add edges
    workflow.add_edge("load_memory", "validation")  # NEW: Add validation step
    workflow.add_edge("validation", "resolve")
    
    # Conditional routing after resolve (skip planner if date error)
    workflow.add_conditional_edges(
        "resolve",
        resolve_router,
        {
            "date_error": "date_error",
            "planner": "planner"
        }
    )
    
    # Conditional routing after plan
    workflow.add_conditional_edges(
        "planner",
        route_node,
        {
            "followup": "followup",
            "build_query": "build_query"
        }
    )
    
    # Followup path
    workflow.add_edge("followup", "save_memory")
    
    # Date error path
    workflow.add_edge("date_error", "save_memory")  # NEW: Save memory after date error
    
    # Main execution path
    workflow.add_edge("build_query", "execute_sparql")
    workflow.add_edge("execute_sparql", "format_evidence")
    workflow.add_edge("format_evidence", "wikidata_enrich")  # Enrich AFTER EOBS data fetched
    workflow.add_edge("wikidata_enrich", "explainer")
    workflow.add_edge("explainer", "save_memory")
    
    # End
    workflow.add_edge("save_memory", END)
    
    return workflow.compile()


# Compile graph at module load
compiled_graph = create_graph()


def _friendly_unable_to_answer_message() -> str:
    """
    Standard friendly message returned to users when the agent cannot answer
    due to unusual queries, missing data, or internal errors. Keep this
    user-facing and avoid exposing technical details or tracebacks.
    """
    return (
        "I'm sorry — I don't have enough information to answer that question. "
        "I may not have the required data or the question is outside my scope. "
        "This system only contains climate observations for 1950-01-01 to 2024-12-31. "
        "Could you please rephrase your question or ask about a date within 1950-2024?"
    )


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def run_agent(
    session_id: str,
    user_message: str,
    history: Optional[List[Dict[str, str]]] = None,
    model: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run the LangGraph agent.
    
    Args:
        session_id: Session identifier
        user_message: User's question
        history: Chat history
        model: Optional model override (format: "provider:model_name")
    
    Returns:
        Dict with answer, technical_details, template, sparql, rows, debug
    """
    try:
        initial_state: AgentState = {
            "session_id": session_id,
            "user_message": user_message,
            "original_message": user_message,
            "history": history or [],
            "model": model,
            # Validation fields
            "typo_corrections": None,
            "typo_message": None,
            "date_validation_error": None,
            "date_availability_message": None,
            "response_format": None,
            "nearest_grid_message": None,
            "location_resolution_method": None,
            # Session memory
            "selected_property_uri": None,
            "selected_feature_uri": None,
            "time_range": None,
            "location_name": None,
            "coordinates": None,
            # Processing state
            "plan": {"template": None, "params": {}, "followup": None},  # Initialize with empty plan
            "sparql_query": None,
            "sparql_rows": None,
            "evidence_text": None,
            "wikidata_context": None,
            "final_answer": None,
            "technical_details": None,
            "debug": {}
        }
        
        # Run the graph
        result = compiled_graph.invoke(initial_state)
        
        # Check if result is None
        if result is None:
            # Provide helpful error message with available date range
            error_answer = (
                "I'm sorry, but I don't have data available for that date. "
                "The climate data in this system is only available from **1950-01-01 to 1951-12-31**.\n\n"
                "Please try asking about a date within this range. For example:\n"
                "- 'Show temperature for 1950-06-15'\n"
                "- 'What was the humidity on 1951-12-25?'\n"
                "- 'Give me precipitation for 1950-01-01'"
            )
            return {
                "answer": error_answer,
                "technical_details": "Error: Graph execution returned None. The requested date may be outside the available data range (1950-01-01 to 1951-12-31).",
                "used_template": "error",
                "sparql": "",
                "rows": [],
                "evidence": "",
                "typo_corrections": {},
                "response_format": "auto",
                "debug": {"error": "Graph returned None", "available_range": "1950-01-01 to 1951-12-31"}
            }
        
        # Safely extract plan template
        plan = result.get("plan")
        template_used = "unknown"
        if plan and isinstance(plan, dict):
            template_used = plan.get("template", "unknown") or "unknown"
        
        # Safely get sparql_rows with default empty list
        sparql_rows = result.get("sparql_rows") or []
        rows_to_return = sparql_rows[:10] if isinstance(sparql_rows, list) else []
        
        # Format response and sanitize technical errors into friendly user messages
        raw_answer = result.get("final_answer") or ""
        raw_tech = result.get("technical_details") or "No technical details available."

        # Only suppress the answer if it looks like a raw Python exception/traceback,
        # not if it naturally contains words like 'error' or 'not available'.
        _TECHNICAL_ERROR_PATTERN = re.compile(
            r"(Traceback \(most recent call|Exception:|SPARQLSecurityError:|Query execution failed:|Error building query:)",
            re.IGNORECASE,
        )
        if _TECHNICAL_ERROR_PATTERN.search(raw_answer):
            user_answer = _friendly_unable_to_answer_message()
            tech_details = "Internal error (logged)."
        else:
            user_answer = raw_answer
            tech_details = raw_tech

        return {
            "answer": user_answer or "No answer generated.",
            "technical_details": tech_details,
            "used_template": template_used,
            "sparql": result.get("sparql_query") or "",
            "rows": rows_to_return,
            "evidence": result.get("evidence_text") or "",
            "typo_corrections": result.get("typo_corrections") or {},
            "response_format": result.get("response_format") or "auto",
            "debug": result.get("debug") or {}
        }
    except Exception as e:
        # Catch any unexpected errors and return a safe response
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Agent execution failed: {e}")
        print(error_trace)
        
        return {
            "answer": _friendly_unable_to_answer_message(),
            "technical_details": "Internal error (logged).",
            "used_template": "error",
            "sparql": "",
            "rows": [],
            "evidence": "",
            "typo_corrections": {},
            "response_format": "auto",
            "debug": {"error": str(e), "trace": error_trace}
        }
