"""
Response format detector and dual format generator (layman vs technical).
"""

from typing import Dict, List, Any, Optional
from enum import Enum


class ResponseFormat(Enum):
    """Response format types."""
    LAYMAN = "layman"
    TECHNICAL = "technical"
    AUTO = "auto"


class ResponseFormatDetector:
    """Detect whether user wants layman or technical response."""
    
    # Keywords that suggest technical format
    TECHNICAL_KEYWORDS = [
        'statistical', 'statistics', 'std', 'deviation', 'variance',
        'confidence', 'interval', 'methodology', 'technical', 'analysis',
        'precise', 'exact', 'detailed', 'metric', 'metrics', 'measure',
        'distribution', 'correlation', 'regression', 'p-value', 'significance',
        'standard error', 'coefficient', 'r-squared', 'quantile',
        'scientific', 'academic', 'research', 'study'
    ]
    
    # Keywords that suggest layman format
    LAYMAN_KEYWORDS = [
        'simple', 'easy', 'explain', 'layman', 'basic', 'understand',
        'plain', 'summary', 'overview', 'eli5', 'like i\'m 5',
        'non-technical', 'beginner', 'normal', 'everyday'
    ]
    
    @classmethod
    def detect_format(cls, query: str) -> ResponseFormat:
        """
        Detect desired response format from user query.
        
        Args:
            query: User's query text
            
        Returns:
            ResponseFormat enum value
        """
        query_lower = query.lower()
        
        # Check for explicit format requests
        technical_score = sum(1 for kw in cls.TECHNICAL_KEYWORDS if kw in query_lower)
        layman_score = sum(1 for kw in cls.LAYMAN_KEYWORDS if kw in query_lower)
        
        # Only return technical if explicitly requested
        if technical_score > 0 and technical_score > layman_score:
            return ResponseFormat.TECHNICAL
        elif layman_score > 0:
            return ResponseFormat.LAYMAN
        
        # Default to layman format for all queries (clean, simple responses)
        return ResponseFormat.LAYMAN


class DualFormatResponder:
    """Generate responses in either layman or technical format."""
    
    @staticmethod
    def generate_both_formats(
        data: Dict[str, Any],
        template_type: str,
        property_name: Optional[str] = None,
        debug_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Generate both layman and technical responses.
        
        Args:
            data: Data dictionary with results
            template_type: Type of query template used
            property_name: Name of the property
            debug_info: Debug information to include in technical response
            
        Returns:
            Dict with 'layman' and 'technical' response strings
        """
        layman_response = DualFormatResponder.format_layman(data, template_type, property_name)
        technical_response = DualFormatResponder.format_technical(
            data, template_type, property_name, debug_info
        )
        
        return {
            'layman': layman_response,
            'technical': technical_response
        }
    
    @staticmethod
    def format_layman(
        data: Dict[str, Any],
        template_type: str,
        property_name: Optional[str] = None
    ) -> str:
        """
        Format response for layman audience.
        Uses simple language, emojis, clear headings, everyday comparisons.
        
        Args:
            data: Data dictionary with results
            template_type: Type of query template used
            property_name: Name of the property
            
        Returns:
            Formatted layman-friendly response
        """
        lines = []
        
        # Add friendly emoji header based on property
        emoji = DualFormatResponder._get_emoji_for_property(property_name)
        if property_name:
            lines.append(f"{emoji} {property_name.title()} Data")
        else:
            lines.append(f"📊 Climate Data Results")
        lines.append("")
        
        # Format based on template type
        if template_type == 'average_for_property_date_range':
            avg = data.get('average', 'N/A')
            unit = data.get('unit', '')
            count = data.get('count', 0)
            time_period = data.get('time_period', 'the period')
            
            lines.append(f"Quick Summary:")
            lines.append(f"The average {property_name or 'value'} during {time_period} was {avg}{unit}")
            lines.append(f"(Based on {count:,} measurements)")
            
            # Add context/comparison if applicable
            comparison = DualFormatResponder._get_layman_comparison(property_name, float(avg) if avg != 'N/A' else 0, unit)
            if comparison:
                lines.append("")
                lines.append(f"💡 In everyday terms: {comparison}")
        
        elif template_type == 'timeseries_statistics':
            mean = data.get('mean', 'N/A')
            min_val = data.get('min', 'N/A')
            max_val = data.get('max', 'N/A')
            unit = data.get('unit', '')
            
            lines.append("What the data shows:")
            lines.append(f"1. Typical value: {mean}{unit} (average)")
            lines.append(f"2. Lowest recorded: {min_val}{unit}")
            lines.append(f"3. Highest recorded: {max_val}{unit}")
            
            # Add range description
            try:
                range_val = float(max_val) - float(min_val)
                lines.append(f"4. Variation: {range_val:.2f}{unit} (difference between high and low)")
            except:
                pass
        
        elif template_type in ['daily_aggregates', 'monthly_aggregates']:
            period = "Daily" if template_type == 'daily_aggregates' else "Monthly"
            lines.append(f"{period} Breakdown:")
            lines.append(f"Here's how {property_name or 'values'} changed over time:")
            lines.append("")
            
            # Show values in friendly format
            for item in data.get('values', [])[:10]:
                date = item.get('date', 'N/A')
                mean = item.get('mean', 'N/A')
                unit = item.get('unit', '')
                lines.append(f"📅 {date}: {mean}{unit}")
        
        else:
            # Generic format
            lines.append("Results:")
            lines.append(f"Found {data.get('count', 0)} data points")
        
        # Add helpful footer
        lines.append("")
        lines.append("_Need more details? Ask me for technical analysis!_")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_technical(
        data: Dict[str, Any],
        template_type: str,
        property_name: Optional[str] = None,
        debug_info: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Format response for technical audience.
        Includes statistics, metrics, confidence intervals, methodology notes, and debug info.
        
        Args:
            data: Data dictionary with results
            template_type: Type of query template used
            property_name: Name of the property
            debug_info: Debug information (timings, errors, etc.)
            
        Returns:
            Formatted technical response
        """
        lines = []
        
        # Technical header
        lines.append(f"Statistical Analysis: {property_name or 'Climate Data'}")
        lines.append("")
        lines.append(f"Query Type: {template_type}")
        lines.append("")
        
        # Format based on template type
        if template_type == 'average_for_property_date_range':
            avg = data.get('average', 'N/A')
            unit = data.get('unit', '')
            count = data.get('count', 0)
            std = data.get('std', 'N/A')
            
            lines.append("Summary Statistics")
            lines.append(f"1. Mean: {avg} {unit}")
            lines.append(f"2. Sample Size (n): {count:,}")
            
            if std != 'N/A':
                lines.append(f"3. Standard Deviation (σ): {std} {unit}")
                try:
                    # Calculate confidence interval (95%)
                    import math
                    se = float(std) / math.sqrt(count)
                    ci_lower = float(avg) - 1.96 * se
                    ci_upper = float(avg) + 1.96 * se
                    lines.append(f"4. 95% CI: [{ci_lower:.2f}, {ci_upper:.2f}] {unit}")
                except:
                    pass
        
        elif template_type == 'timeseries_statistics':
            mean = data.get('mean', 'N/A')
            min_val = data.get('min', 'N/A')
            max_val = data.get('max', 'N/A')
            count = data.get('count', 0)
            std = data.get('std', 'N/A')
            unit = data.get('unit', '')
            
            lines.append("Descriptive Statistics")
            lines.append(f"1. Mean (μ): {mean} {unit}")
            lines.append(f"2. Minimum: {min_val} {unit}")
            lines.append(f"3. Maximum: {max_val} {unit}")
            
            if std != 'N/A':
                lines.append(f"4. Std Dev (σ): {std} {unit}")
            
            try:
                range_val = float(max_val) - float(min_val)
                lines.append(f"5. Range: {range_val:.2f} {unit}")
            except:
                pass
            
            lines.append(f"6. N: {count:,} observations")
        
        elif template_type in ['daily_aggregates', 'monthly_aggregates']:
            period = "Daily" if template_type == 'daily_aggregates' else "Monthly"
            lines.append(f"{period} Aggregated Metrics")
            lines.append("")
            lines.append(f"Temporal Resolution: {period}")
            lines.append(f"Aggregation Function: Mean, Min, Max")
            lines.append("")
            
            # Table format
            lines.append("| Date | Mean | Min | Max | Unit |")
            lines.append("|------|------|-----|-----|------|")
            
            for item in data.get('values', [])[:20]:
                date = item.get('date', 'N/A')
                mean = item.get('mean', 'N/A')
                min_v = item.get('min', 'N/A')
                max_v = item.get('max', 'N/A')
                unit = item.get('unit', '')
                lines.append(f"| {date} | {mean} | {min_v} | {max_v} | {unit} |")
        
        # Add methodology notes
        lines.append("")
        lines.append("Methodology Notes")
        lines.append("1. Data Source: Climate observation knowledge graph (1950-1951)")
        lines.append("2. Query Language: SPARQL")
        lines.append("3. Aggregation: Server-side computation")
        lines.append("4. Missing Data: Excluded from calculations")
        
        # Add debug information if provided
        if debug_info:
            lines.append("")
            lines.append("Debug Information")
            lines.append("─" * 40)
            
            # Timing information
            if 'validation_time' in debug_info:
                lines.append(f"⏱ Validation: {debug_info['validation_time']}s")
            if 'resolve_time' in debug_info:
                lines.append(f"⏱ Resolution: {debug_info['resolve_time']}s")
            if 'plan_time' in debug_info:
                lines.append(f"⏱ Planning: {debug_info['plan_time']}s")
            if 'build_query_time' in debug_info:
                lines.append(f"⏱ Query Build: {debug_info['build_query_time']}s")
            if 'execute_time' in debug_info:
                lines.append(f"⏱ Execution: {debug_info['execute_time']}s")
            if 'format_time' in debug_info:
                lines.append(f"⏱ Format: {debug_info['format_time']}s")
            if 'explain_time' in debug_info:
                lines.append(f"⏱ Explanation: {debug_info['explain_time']}s")
            
            # Result counts
            if 'row_count' in debug_info:
                lines.append(f"📊 Rows Retrieved: {debug_info['row_count']}")
            
            # Model info
            if 'llm_provider' in debug_info:
                lines.append(f"🤖 LLM Provider: {debug_info['llm_provider']}")
            if 'llm_model' in debug_info:
                lines.append(f"🤖 LLM Model: {debug_info['llm_model']}")
            
            # Errors or warnings
            if 'plan_error' in debug_info:
                lines.append(f"⚠️ Planning Error: {debug_info['plan_error']}")
            if 'execute_error' in debug_info:
                lines.append(f"⚠️ Execution Error: {debug_info['execute_error']}")
            
            # Memory state
            if 'memory_loaded' in debug_info:
                lines.append(f"💾 Session Memory: {'Loaded' if debug_info['memory_loaded'] else 'Not found'}")
            if 'memory_saved' in debug_info:
                lines.append(f"💾 Session Save: {'Success' if debug_info['memory_saved'] else 'Failed'}")
        
        return "\n".join(lines)
    
    @staticmethod
    def _get_emoji_for_property(property_name: Optional[str]) -> str:
        """Get relevant emoji for property type."""
        if not property_name:
            return "📊"
        
        prop_lower = property_name.lower()
        
        if 'temp' in prop_lower:
            return "🌡️"
        elif 'rain' in prop_lower or 'precip' in prop_lower:
            return "🌧️"
        elif 'humid' in prop_lower:
            return "💧"
        elif 'wind' in prop_lower:
            return "💨"
        elif 'pressure' in prop_lower:
            return "⏱️"
        elif 'solar' in prop_lower or 'sun' in prop_lower:
            return "☀️"
        else:
            return "📊"
    
    @staticmethod
    def _get_layman_comparison(property_name: Optional[str], value: float, unit: str) -> Optional[str]:
        """Generate layman-friendly comparison."""
        if not property_name:
            return None
        
        prop_lower = property_name.lower()
        
        # Temperature comparisons
        if 'temp' in prop_lower:
            if 'celsius' in unit.lower() or '°c' in unit.lower():
                if value < 0:
                    return "That's below freezing! ❄️"
                elif value < 10:
                    return "Pretty cold, like a chilly winter day"
                elif value < 20:
                    return "Cool and comfortable, like spring weather"
                elif value < 30:
                    return "Warm and pleasant, perfect outdoor temperature"
                else:
                    return "Hot! That's a summer heat wave 🔥"
        
        # Precipitation
        elif 'rain' in prop_lower or 'precip' in prop_lower:
            if 'mm' in unit.lower():
                if value < 1:
                    return "Very light drizzle"
                elif value < 10:
                    return "Light rain"
                elif value < 50:
                    return "Moderate rainfall"
                else:
                    return "Heavy rain! 🌧️"
        
        return None
