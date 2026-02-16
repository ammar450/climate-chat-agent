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
