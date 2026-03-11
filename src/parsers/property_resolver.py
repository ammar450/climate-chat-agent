"""
Property URI resolver with domain dictionary and caching.
"""

from typing import Optional, List, Tuple
from src.query.sparql_client import run_sparql, GRAPH
import threading


class PropertyResolver:
    """Resolve natural language property names to URIs."""
    
    # Expanded domain dictionary with common terms, synonyms, and typo variants
    DOMAIN_DICTIONARY = {
        # Temperature variations
        "temperature": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "temp": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "air_temperature": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "air temp": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "degrees": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "warmth": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "heat": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "cold": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "hot": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        # Common typos for temperature
        "temprature": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "temperatur": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "tempature": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "temerature": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        "temperture": "http://vocab.nerc.ac.uk/standard_name/air_temperature",
        
        # Humidity variations
        "humidity": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
        "relative_humidity": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
        "relative humidity": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
        "moisture": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
        "dampness": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
        "wetness": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
        # Common typos for humidity
        "humidty": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
        "humiditiy": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
        "humitidy": "http://vocab.nerc.ac.uk/standard_name/relative_humidity",
        
        # Precipitation/Rain variations
        "rain": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "rainfall": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "precipitation": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "precipitation_amount": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "precipitation amount": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "precip": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "rainy": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "raining": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "shower": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "showers": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "downpour": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        # Common typos for precipitation/rain
        "rainfal": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "rainfalll": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "precipitaion": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "percipitation": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        "precipiation": "http://vocab.nerc.ac.uk/standard_name/precipitation_amount",
        
        # Wind variations
        "wind": "http://vocab.nerc.ac.uk/standard_name/wind_speed",
        "wind_speed": "http://vocab.nerc.ac.uk/standard_name/wind_speed",
        "wind speed": "http://vocab.nerc.ac.uk/standard_name/wind_speed",
        "windy": "http://vocab.nerc.ac.uk/standard_name/wind_speed",
        "breeze": "http://vocab.nerc.ac.uk/standard_name/wind_speed",
        "gust": "http://vocab.nerc.ac.uk/standard_name/wind_speed",
        "gusts": "http://vocab.nerc.ac.uk/standard_name/wind_speed",
        
        # Pressure variations
        "pressure": "http://vocab.nerc.ac.uk/standard_name/air_pressure",
        "air_pressure": "http://vocab.nerc.ac.uk/standard_name/air_pressure",
        "air pressure": "http://vocab.nerc.ac.uk/standard_name/air_pressure",
        "atmospheric pressure": "http://vocab.nerc.ac.uk/standard_name/air_pressure",
        "barometric": "http://vocab.nerc.ac.uk/standard_name/air_pressure",
        "barometric pressure": "http://vocab.nerc.ac.uk/standard_name/air_pressure",
        
        # Solar/Radiation variations
        "solar": "http://vocab.nerc.ac.uk/standard_name/surface_downwelling_shortwave_flux_in_air",
        "radiation": "http://vocab.nerc.ac.uk/standard_name/surface_downwelling_shortwave_flux_in_air",
        "solar radiation": "http://vocab.nerc.ac.uk/standard_name/surface_downwelling_shortwave_flux_in_air",
        "sunlight": "http://vocab.nerc.ac.uk/standard_name/surface_downwelling_shortwave_flux_in_air",
        "sun": "http://vocab.nerc.ac.uk/standard_name/surface_downwelling_shortwave_flux_in_air",
        "sunshine": "http://vocab.nerc.ac.uk/standard_name/surface_downwelling_shortwave_flux_in_air",
        "shortwave": "http://vocab.nerc.ac.uk/standard_name/surface_downwelling_shortwave_flux_in_air",
    }
    
    def __init__(self):
        self._available_properties: List[Tuple[str, int]] = []  # [(uri, count)]
        self._cache_lock = threading.Lock()
        self._cached = False
    
    def prefetch_properties(self):
        """Prefetch available properties from endpoint (run at startup)."""
        query = f"""PREFIX sosa: <http://www.w3.org/ns/sosa/>
SELECT ?property (COUNT(*) AS ?count)
FROM <{GRAPH}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:observedProperty ?property .
}}
GROUP BY ?property
ORDER BY DESC(?count)
LIMIT 100"""
        
        try:
            result = run_sparql(query, validate=False)
            properties = []
            for row in result.get("results", {}).get("bindings", []):
                uri = row["property"]["value"]
                count = int(row["count"]["value"])
                properties.append((uri, count))
            
            with self._cache_lock:
                self._available_properties = properties
                self._cached = True
            
            print(f"Cached {len(properties)} properties from endpoint")
        except Exception as e:
            print(f"Failed to prefetch properties: {e}")
    
    def resolve(self, property_hint: str) -> Tuple[Optional[str], Optional[str], Optional[List[str]]]:
        """
        Resolve a property hint to a URI.
        
        Args:
            property_hint: User's property description
            
        Returns:
            Tuple of (resolved_uri, confidence_note, candidate_list)
            - If resolved: (uri, "exact match" or "assumed X", None)
            - If ambiguous: (None, None, [list of candidate URIs])
            - If not found: (None, "not found", None)
        """
        # Lazy prefetch if not done yet
        if not self._cached:
            print("[PROPERTY_RESOLVER] Prefetching properties on first use...")
            self.prefetch_properties()
        
        if not property_hint:
            return (None, None, None)
        
        hint_lower = property_hint.lower().strip()
        
        # Check if it's already a URI
        if hint_lower.startswith("http://") or hint_lower.startswith("https://"):
            return (property_hint, "exact URI provided", None)
        
        # Check domain dictionary (exact match)
        if hint_lower in self.DOMAIN_DICTIONARY:
            uri = self.DOMAIN_DICTIONARY[hint_lower]
            # Verify it exists in the dataset
            if self._verify_property_exists(uri):
                return (uri, f"matched '{hint_lower}' to standard name", None)
            else:
                # Fallback to search
                pass
        
        # Fuzzy matching for typos (if not exact match)
        fuzzy_match = self._fuzzy_match_dictionary(hint_lower)
        if fuzzy_match:
            uri = self.DOMAIN_DICTIONARY[fuzzy_match]
            if self._verify_property_exists(uri):
                return (uri, f"fuzzy matched '{hint_lower}' to '{fuzzy_match}'", None)
        
        # Search in cached properties by substring
        candidates = self._search_properties(hint_lower)
        
        if len(candidates) == 0:
            return (None, "property not found in dataset", None)
        elif len(candidates) == 1:
            return (candidates[0], f"found property matching '{hint_lower}'", None)
        else:
            # Multiple candidates - ask user to choose
            return (None, None, candidates[:10])  # Limit to top 10
    
    def _verify_property_exists(self, uri: str) -> bool:
        """Check if a property URI exists in cached properties."""
        with self._cache_lock:
            for prop_uri, _ in self._available_properties:
                if prop_uri == uri:
                    return True
        return False
    
    def _fuzzy_match_dictionary(self, query: str) -> Optional[str]:
        """
        Find closest match in dictionary using Levenshtein-like distance.
        Handles common typos (1-2 character differences).
        """
        if len(query) < 3:
            return None
        
        best_match = None
        best_distance = float('inf')
        
        for key in self.DOMAIN_DICTIONARY.keys():
            distance = self._levenshtein_distance(query, key)
            # Allow 1-2 character difference based on length
            max_distance = 1 if len(query) <= 5 else 2
            
            if distance <= max_distance and distance < best_distance:
                best_distance = distance
                best_match = key
        
        return best_match
    
    @staticmethod
    def _levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return PropertyResolver._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost of insertions, deletions, or substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _search_properties(self, keyword: str) -> List[str]:
        """Search for properties containing keyword."""
        keyword_lower = keyword.lower()
        matches = []
        
        with self._cache_lock:
            for uri, count in self._available_properties:
                uri_lower = uri.lower()
                # Extract the last part of the URI (the standard_name)
                parts = uri.split('/')
                if parts:
                    name = parts[-1].lower()
                    if keyword_lower in name or keyword_lower.replace('_', ' ') in name.replace('_', ' '):
                        matches.append(uri)
        
        return matches
    
    def get_property_display_name(self, uri: str) -> str:
        """Extract a human-readable name from property URI."""
        if not uri:
            return "unknown"
        
        # Extract last part of URI
        parts = uri.split('/')
        if parts:
            name = parts[-1]
            # Convert underscores to spaces and title case
            return name.replace('_', ' ').title()
        return uri
    
    def get_available_properties(self, limit: int = 20) -> List[Tuple[str, str, int]]:
        """
        Get list of available properties with display names.
        
        Returns:
            List of (uri, display_name, count) tuples
        """
        with self._cache_lock:
            return [
                (uri, self.get_property_display_name(uri), count)
                for uri, count in self._available_properties[:limit]
            ]


# Global property resolver
property_resolver = PropertyResolver()


# ============================================================================
# LOCATION RESOLVER
# ============================================================================

class LocationResolver:
    """Resolve location names to coordinates and feature URIs."""
    
    # Major European cities with their coordinates (lat, lon)
    # This dataset primarily covers European region from 1950-1951
    CITY_COORDINATES = {
        # Germany
        "berlin": (52.52, 13.40),
        "munich": (48.14, 11.58),
        "hamburg": (53.55, 10.00),
        "cologne": (50.94, 6.96),
        "frankfurt": (50.11, 8.68),
        
        # France
        "paris": (48.86, 2.35),
        "marseille": (43.30, 5.37),
        "lyon": (45.76, 4.84),
        "toulouse": (43.60, 1.44),
        
        # UK
        "london": (51.51, -0.13),
        "manchester": (53.48, -2.24),
        "birmingham": (52.48, -1.90),
        "edinburgh": (55.95, -3.19),
        
        # Italy
        "rome": (41.90, 12.50),
        "milan": (45.46, 9.19),
        "naples": (40.85, 14.27),
        "turin": (45.07, 7.69),
        "florence": (43.77, 11.26),
        
        # Spain
        "madrid": (40.42, -3.70),
        "barcelona": (41.39, 2.17),
        "valencia": (39.47, -0.38),
        "seville": (37.39, -5.98),
        
        # Netherlands
        "amsterdam": (52.37, 4.89),
        "rotterdam": (51.92, 4.48),
        "the hague": (52.08, 4.31),
        
        # Belgium
        "brussels": (50.85, 4.35),
        "antwerp": (51.22, 4.40),
        
        # Other major European cities
        "vienna": (48.21, 16.37),
        "zurich": (47.37, 8.54),
        "geneva": (46.20, 6.14),
        "prague": (50.08, 14.44),
        "warsaw": (52.23, 21.01),
        "budapest": (47.50, 19.04),
        "athens": (37.98, 23.73),
        "lisbon": (38.72, -9.14),
        "copenhagen": (55.68, 12.57),
        "oslo": (59.91, 10.75),
        "stockholm": (59.33, 18.07),
        "helsinki": (60.17, 24.94),
        "dublin": (53.35, -6.26),
    }
    
    @staticmethod
    def get_coordinates(location_name: str) -> Optional[tuple]:
        """
        Get coordinates for a location name.
        
        Args:
            location_name: City or location name
            
        Returns:
            (lat, lon) tuple or None if not found
        """
        location_lower = location_name.lower().strip()
        return LocationResolver.CITY_COORDINATES.get(location_lower)
    
    @staticmethod
    def find_nearest_feature(lat: float, lon: float, sparql_client_func) -> Optional[str]:
        """
        Find the nearest feature URI given coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            sparql_client_func: Function to execute SPARQL queries
            
        Returns:
            Feature URI of nearest station or None
        """
        from src.query.query_templates import GRAPH
        
        # Query to get all features with their geometries
        query = f"""PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
SELECT DISTINCT ?feature ?wkt
FROM <{GRAPH}>
WHERE {{
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?feature .
  OPTIONAL {{
    ?feature geo:hasGeometry ?geom .
    ?geom geo:asWKT ?wkt .
  }}
}}
LIMIT 1000"""
        
        try:
            result = sparql_client_func(query)
            features = result.get("results", {}).get("bindings", [])
            
            if not features:
                print(f"[LOCATION] No features found with geometries")
                return None
            
            # Calculate distances and find nearest
            nearest_feature = None
            min_distance = float('inf')
            
            for feature_row in features:
                feature_uri = feature_row.get("feature", {}).get("value")
                wkt = feature_row.get("wkt", {}).get("value", "")
                
                # Parse WKT to get coordinates
                # Format: POINT(lon lat) or similar
                if "POINT" in wkt.upper():
                    try:
                        coords_str = wkt.split("(")[1].split(")")[0]
                        parts = coords_str.strip().split()
                        feature_lon = float(parts[0])
                        feature_lat = float(parts[1])
                        
                        # Calculate Haversine distance
                        distance = LocationResolver._haversine_distance(
                            lat, lon, feature_lat, feature_lon
                        )
                        
                        if distance < min_distance:
                            min_distance = distance
                            nearest_feature = feature_uri
                    except Exception as e:
                        print(f"[LOCATION] Error parsing WKT '{wkt}': {e}")
                        continue
            
            if nearest_feature:
                print(f"[LOCATION] Found nearest feature: {nearest_feature} (distance: {min_distance:.2f} km)")
                return nearest_feature
            else:
                print(f"[LOCATION] No valid feature geometries found")
                return None
                
        except Exception as e:
            print(f"[LOCATION] Error finding nearest feature: {e}")
            return None
    
    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth.
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            Distance in kilometers
        """
        import math
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth radius in kilometers
        r = 6371
        
        return c * r


# Global location resolver
location_resolver = LocationResolver()
