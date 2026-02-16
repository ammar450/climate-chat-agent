"""
Error handler with helpful messages and query suggestions.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime


class QuerySuggestionEngine:
    """Generate helpful suggestions for invalid or problematic queries."""
    
    # Available data years
    MIN_YEAR = 1950
    MAX_YEAR = 1951
    
    # Common query templates
    EXAMPLE_QUERIES = [
        "What was the temperature in 1950?",
        "Show me 1951 precipitation patterns",
        "Compare 1950 vs 1951 temperature",
        "What variables are available?",
        "Show me daily averages for January 1950",
        "What was the rainfall in 1951?",
    ]
    
    @classmethod
    def handle_year_out_of_range(cls, requested_year: int, property_name: Optional[str] = None) -> Dict[str, str]:
        """
        Generate helpful error message and suggestions for year out of range.
        
        Args:
            requested_year: Year that user requested
            property_name: Optional property (e.g., "temperature")
            
        Returns:
            Dict with 'error', 'explanation', and 'suggestions'
        """
        # Determine closest available year
        if requested_year < cls.MIN_YEAR:
            closest_year = cls.MIN_YEAR
            comparison = "earlier than"
        else:
            closest_year = cls.MAX_YEAR
            comparison = "later than"
        
        property_part = f" {property_name}" if property_name else ""
        
        error_msg = f"I notice you asked about {requested_year}"
        explanation = f"I only have climate data for 1950 and 1951. Your requested year ({requested_year}) is {comparison} my available data."
        
        # Generate suggestions
        suggestions = []
        
        if property_name:
            suggestions.append(f"Would you like to see{property_part} data for {closest_year} instead?")
            suggestions.append(f"I can show you{property_part} for the entire 1950-1951 period")
            suggestions.append(f"Try: 'What was the{property_part} in {closest_year}?'")
        else:
            suggestions.append(f"Would you like to see data for {closest_year} instead?")
            suggestions.append(f"I can compare 1950 vs 1951 for you")
            suggestions.append(f"Try: 'Show me climate data from {closest_year}'")
        
        return {
            'error': error_msg,
            'explanation': explanation,
            'suggestions': suggestions
        }
    
    @classmethod
    def handle_no_data_found(cls, context: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate helpful message when no data is found.
        
        Args:
            context: Dict with 'property', 'location', 'time_range', etc.
            
        Returns:
            Dict with 'error', 'explanation', and 'suggestions'
        """
        error_msg = "I couldn't find any data matching your criteria"
        
        explanation_parts = []
        if context.get('property'):
            explanation_parts.append(f"Property: {context['property']}")
        if context.get('location'):
            explanation_parts.append(f"Location: {context['location']}")
        if context.get('time_range'):
            explanation_parts.append(f"Time: {context['time_range']}")
        
        if explanation_parts:
            explanation = "Search criteria:\n" + "\n".join([f"{i+1}. {part}" for i, part in enumerate(explanation_parts)])
        else:
            explanation = "No specific criteria were set"
        
        suggestions = [
            "Try listing available variables: 'What variables are available?'",
            "Try a broader time range: 'Show me 1950 data'",
            "Check available locations: 'List all stations'"
        ]
        
        return {
            'error': error_msg,
            'explanation': explanation,
            'suggestions': suggestions
        }
    
    @classmethod
    def handle_typo_detected(cls, typos: Dict[str, str]) -> str:
        """
        Generate friendly message about typo corrections.
        
        Args:
            typos: Dict mapping typo -> corrected word
            
        Returns:
            Formatted correction message
        """
        if not typos:
            return ""
        
        if len(typos) == 1:
            typo, correct = list(typos.items())[0]
            return f"💡 I assumed you meant {correct} (you wrote '{typo}')"
        else:
            items = [f"'{typo}' → {correct}" for typo, correct in typos.items()]
            return f"💡 I corrected some typos: {', '.join(items)}"
    
    @classmethod
    def suggest_alternative_queries(cls, failed_query_type: str) -> List[str]:
        """
        Suggest alternative queries based on what failed.
        
        Args:
            failed_query_type: Type of query that failed
            
        Returns:
            List of suggested queries
        """
        suggestions = {
            'no_property': [
                "What variables are available?",
                "Show me available climate properties",
                "List all observation types"
            ],
            'no_location': [
                "List all stations",
                "What locations are available?",
                "Show me observation locations"
            ],
            'invalid_date': [
                "What was the temperature in 1950?",
                "Show me 1951 data",
                "Compare 1950 and 1951"
            ],
            'general': cls.EXAMPLE_QUERIES
        }
        
        return suggestions.get(failed_query_type, suggestions['general'])
    
    @classmethod
    def format_error_response(cls, error_type: str, details: Dict[str, Any]) -> str:
        """
        Format a complete error response with suggestions.
        
        Args:
            error_type: Type of error ('year_out_of_range', 'no_data', etc.)
            details: Error-specific details
            
        Returns:
            Formatted error message with suggestions
        """
        if error_type == 'year_out_of_range':
            error_info = cls.handle_year_out_of_range(
                details.get('year'),
                details.get('property')
            )
        elif error_type == 'no_data':
            error_info = cls.handle_no_data_found(details)
        else:
            return "I encountered an error processing your request. Please try rephrasing your question."
        
        # Build formatted response
        lines = [
            error_info['error'],
            "",
            error_info['explanation'],
            "",
            "Here are some suggestions:"
        ]
        
        for i, suggestion in enumerate(error_info['suggestions'], 1):
            lines.append(f"{i}. {suggestion}")
        
        return "\n".join(lines)
    
    @classmethod
    def get_contextual_help(cls, user_query: str) -> Optional[str]:
        """
        Provide contextual help based on user query patterns.
        
        Args:
            user_query: User's query text
            
        Returns:
            Help message or None
        """
        query_lower = user_query.lower()
        
        # Check for common issues
        if any(word in query_lower for word in ['recent', 'latest', 'current', 'today', '2020', '2021', '2022', '2023', '2024', '2025']):
            return (
                "💡 Note: I only have historical climate data for 1950 and 1951. "
                "I cannot provide recent or current data.\n\n"
                "Try asking about 1950 or 1951 instead!"
            )
        
        if 'help' in query_lower or 'how' in query_lower:
            return (
                "I can help you with:\n"
                "1. Climate data from 1950-1951\n"
                "2. Temperature, precipitation, humidity, and more\n"
                "3. Daily, monthly, or yearly averages\n"
                "4. Comparisons between time periods\n\n"
                "Try asking:\n"
                f"- {cls.EXAMPLE_QUERIES[0]}\n"
                f"- {cls.EXAMPLE_QUERIES[1]}\n"
                f"- {cls.EXAMPLE_QUERIES[4]}"
            )
        
        return None
