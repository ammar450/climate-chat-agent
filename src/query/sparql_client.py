"""
SPARQL client with enhanced safety controls and validation.
Backend is the ONLY component allowed to call the SPARQL endpoint.
"""

import os
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment variables
# Primary knowledge source: EOBS — always queried first
ENDPOINT = os.getenv("SPARQL_ENDPOINT", "https://obs.knowledgehub.nfdi4earth.de/sparql/")
GRAPH = os.getenv("GRAPH_IRI", "climateobservations/eobs-v31")
QUERY_TIMEOUT = int(os.getenv("SPARQL_TIMEOUT", "300"))  # seconds
MAX_LIMIT = int(os.getenv("MAX_LIMIT", "500"))
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "200"))

# Dangerous SPARQL keywords that should not be allowed
DANGEROUS_KEYWORDS = [
    "INSERT", "DELETE", "LOAD", "CLEAR", "CREATE", 
    "DROP", "MOVE", "COPY", "ADD", "UPDATE"
]


class SPARQLSecurityError(Exception):
    """Raised when a query violates security policies."""
    pass


def is_safe_query(query: str) -> bool:
    """
    Check if a SPARQL query is safe (read-only SELECT only).
    
    Args:
        query: SPARQL query string
        
    Returns:
        True if safe, False otherwise
        
    Raises:
        SPARQLSecurityError: If query violates security policies
    """
    query_upper = query.upper().strip()
    
    # Must contain SELECT (but doesn't have to be first due to PREFIX declarations)
    if "SELECT" not in query_upper:
        raise SPARQLSecurityError("Query must contain SELECT")
    
    # Check for dangerous keywords
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in query_upper:
            raise SPARQLSecurityError(f"Query contains forbidden keyword: {keyword}")
    
    return True


def enforce_limit(query: str, max_limit: int = None) -> str:
    """
    Enforce a maximum LIMIT on a SPARQL query.
    If no LIMIT present, add DEFAULT_LIMIT.
    If LIMIT > MAX_LIMIT, clamp to MAX_LIMIT.
    
    Args:
        query: SPARQL query string
        max_limit: Maximum allowed LIMIT (uses MAX_LIMIT from config if None)
        
    Returns:
        Query with enforced LIMIT
    """
    if max_limit is None:
        max_limit = MAX_LIMIT
    
    # Check if query has aggregate functions (COUNT, AVG, SUM, etc.)
    has_aggregate = bool(re.search(r'\b(COUNT|AVG|SUM|MIN|MAX)\s*\(', query, re.IGNORECASE))
    
    if has_aggregate:
        # Don't enforce LIMIT on aggregate queries
        return query
    
    # Check if LIMIT already exists - only adjust the LAST (outermost) LIMIT
    limit_matches = list(re.finditer(r'LIMIT\s+(\d+)', query, re.IGNORECASE))
    
    if limit_matches:
        # Only clamp the last LIMIT (outermost query level)
        last_match = limit_matches[-1]
        current_limit = int(last_match.group(1))
        if current_limit > max_limit:
            # Replace only the last occurrence
            prefix = query[:last_match.start()]
            suffix = query[last_match.end():]
            query = prefix + f'LIMIT {max_limit}' + suffix
            print(f"[SECURITY] Outer LIMIT reduced from {current_limit} to {max_limit}")
    else:
        # No LIMIT found, add default
        query = query.rstrip() + f"\nLIMIT {DEFAULT_LIMIT}"
        print(f"[SECURITY] Added default LIMIT {DEFAULT_LIMIT}")
    
    return query


def ensure_from_clause(query: str, graph_uri: str = GRAPH) -> str:
    """
    Ensure the query has a FROM clause for the named graph.
    
    Args:
        query: SPARQL query string
        graph_uri: Graph URI to use
        
    Returns:
        Query with FROM clause
    """
    if f"FROM <{graph_uri}>" in query or "FROM <" in query:
        return query
    
    # Insert FROM after SELECT line
    lines = query.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if re.match(r'^\s*SELECT\s+', line, re.IGNORECASE):
            new_lines.append(f'FROM <{graph_uri}>')
    
    return '\n'.join(new_lines)


def run_sparql(query: str, validate: bool = True) -> Dict[str, Any]:
    """
    Execute a SPARQL query against the endpoint with enhanced safety checks.
    
    Security measures:
    - Only SELECT queries allowed
    - Enforces FROM <graph> clause
    - Enforces LIMIT <= MAX_LIMIT, defaults to DEFAULT_LIMIT
    - Request timeout protection
    - Error handling and logging
    
    Args:
        query: SPARQL query string
        validate: Whether to apply safety checks (default True)
        
    Returns:
        Query results as dictionary
        
    Raises:
        SPARQLSecurityError: If query violates security policies
        Exception: If query execution fails
    """
    if validate:
        try:
            # Security validation
            is_safe_query(query)
            query = ensure_from_clause(query)
            query = enforce_limit(query)
        except SPARQLSecurityError as e:
            print(f"[SECURITY ERROR] {str(e)}")
            print(f"[SECURITY ERROR] Query was: {query[:200]}...")
            raise
    
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(QUERY_TIMEOUT)
    
    try:
        print(f"[SPARQL] Executing query against {ENDPOINT}")
        result = sparql.query().convert()
        return result
    except Exception as e:
        error_msg = f"SPARQL query failed: {str(e)}"
        print(f"[ERROR] {error_msg}")
        raise Exception(error_msg)


def test_endpoint() -> bool:
    """
    Test if the SPARQL endpoint is reachable.
    
    Returns:
        True if endpoint is working, False otherwise
    """
    test_query = f"""
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    SELECT (COUNT(*) AS ?count)
    FROM <{GRAPH}>
    WHERE {{
      ?obs a sosa:Observation .
    }}
    LIMIT 1
    """
    
    try:
        result = run_sparql(test_query, validate=False)
        return True
    except:
        return False
