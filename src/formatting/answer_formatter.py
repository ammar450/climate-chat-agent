"""
Answer formatter for clean result presentation.
"""

from typing import List, Dict, Any, Optional
from src.parsers.time_parser import TimeParser


class AnswerFormatter:
    """Format SPARQL results into friendly answers."""
    
    @staticmethod
    def format_list_properties(rows: List[Dict[str, Any]], limit: int = 10) -> str:
        """Format list of properties."""
        if not rows:
            return "No properties found in the dataset."
        
        from src.parsers.property_resolver import property_resolver
        
        lines = [f"Found {len(rows)} climate variables. Here are the top {min(limit, len(rows))}:"]
        lines.append("")
        
        for i, row in enumerate(rows[:limit], 1):
            prop_uri = row.get("property", {}).get("value", "")
            count = row.get("count", {}).get("value", "0")
            display_name = property_resolver.get_property_display_name(prop_uri)
            
            # Format count with commas
            try:
                count_int = int(count)
                count_str = f"{count_int:,}"
            except:
                count_str = count
            
            lines.append(f"{i}. {display_name} ({count_str} observations)")
        
        if len(rows) > limit:
            lines.append(f"\n... and {len(rows) - limit} more variables.")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_list_features(rows: List[Dict[str, Any]], limit: int = 10) -> str:
        """Format list of features/locations."""
        if not rows:
            return "No locations found in the dataset."
        
        lines = [f"Found {len(rows)} observation locations. Here are the top {min(limit, len(rows))}:"]
        lines.append("")
        
        for i, row in enumerate(rows[:limit], 1):
            feature_uri = row.get("feature", {}).get("value", "")
            count = row.get("count", {}).get("value", "0")
            # Extract location ID from URI
            location_id = feature_uri.split('/')[-1] if '/' in feature_uri else feature_uri
            
            # Format count with commas
            try:
                count_int = int(count)
                count_str = f"{count_int:,}"
            except:
                count_str = count
            
            lines.append(f"{i}. {location_id} ({count_str} observations)")
        
        if len(rows) > limit:
            lines.append(f"\n... and {len(rows) - limit} more locations.")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_average(rows: List[Dict[str, Any]], property_name: str = "value") -> str:
        """Format average result."""
        if not rows or not rows[0].get("average"):
            return "No data found for the specified criteria."
        
        row = rows[0]
        avg_val = float(row["average"]["value"])
        count = int(row.get("count", {}).get("value", 0))
        unit = row.get("unit", {}).get("value", "")
        
        # Extract unit name
        unit_name = unit.split('/')[-1] if unit else ""
        unit_str = f" {unit_name}" if unit_name else ""
        
        return f"The average {property_name} is {avg_val:.2f}{unit_str} (based on {count:,} observations)."
    
    @staticmethod
    def format_extremes(rows: List[Dict[str, Any]], order: str = "DESC", property_name: str = "value", limit: int = 5) -> str:
        """Format extreme values (highest/lowest)."""
        if not rows:
            return "No data found for the specified criteria."
        
        extreme_type = "highest" if order.upper() == "DESC" else "lowest"
        lines = [f"Here are the {extreme_type} {property_name} values:"]
        lines.append("")
        
        for i, row in enumerate(rows[:limit], 1):
            value = float(row.get("value", {}).get("value", 0))
            time = row.get("time", {}).get("value", "")
            feature = row.get("feature", {}).get("value", "")
            unit = row.get("unit", {}).get("value", "")
            
            # Format time
            time_str = time.split('T')[0] if 'T' in time else time
            # Extract location
            location = feature.split('/')[-1] if '/' in feature else feature
            # Unit
            unit_name = unit.split('/')[-1] if unit else ""
            unit_str = f" {unit_name}" if unit_name else ""
            
            lines.append(f"{i}. {value:.2f}{unit_str} on {time_str} at {location}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_timeseries_summary(rows: List[Dict[str, Any]], property_name: str = "value") -> str:
        """Format timeseries data summary."""
        if not rows:
            return "No time series data found for the specified criteria."
        
        count = len(rows)
        
        # Extract values and times
        values = []
        times = []
        unit = None
        
        for row in rows:
            val = row.get("value", {}).get("value")
            time = row.get("time", {}).get("value")
            if val:
                values.append(float(val))
            if time:
                times.append(time)
            if not unit and row.get("unit"):
                unit = row.get("unit", {}).get("value", "")
        
        if not values:
            return f"Found {count} observations but couldn't extract values."
        
        # Calculate statistics
        min_val = min(values)
        max_val = max(values)
        avg_val = sum(values) / len(values)
        
        # Format dates
        first_date = times[0].split('T')[0] if times else "unknown"
        last_date = times[-1].split('T')[0] if times else "unknown"
        
        # Unit
        unit_name = unit.split('/')[-1] if unit else ""
        unit_str = f" {unit_name}" if unit_name else ""
        
        lines = [
            f"Time series summary for {property_name}:",
            f"Period: {first_date} to {last_date}",
            f"Data points: {count:,}",
            f"Range: {min_val:.2f} - {max_val:.2f}{unit_str}",
            f"Average: {avg_val:.2f}{unit_str}"
        ]
        
        return "\n".join(lines)
    
    @staticmethod
    def format_sample_observations(rows: List[Dict[str, Any]], limit: int = 5) -> str:
        """Format sample observations."""
        if not rows:
            return "No observations found."
        
        lines = [f"Here are {min(limit, len(rows))} sample observations:"]
        lines.append("")
        
        for i, row in enumerate(rows[:limit], 1):
            time = row.get("time", {}).get("value", "")
            value = row.get("value", {}).get("value", "")
            prop = row.get("property", {}).get("value", "")
            unit = row.get("unit", {}).get("value", "")
            
            # Format components
            time_str = time.split('T')[0] if 'T' in time else time
            from src.parsers.property_resolver import property_resolver
            prop_name = property_resolver.get_property_display_name(prop)
            unit_name = unit.split('/')[-1] if unit else ""
            unit_str = f" {unit_name}" if unit_name else ""
            
            lines.append(f"{i}. {time_str}: {value}{unit_str} ({prop_name})")
        
        if len(rows) > limit:
            lines.append(f"\n... and {len(rows) - limit:,} more observations.")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_count(rows: List[Dict[str, Any]]) -> str:
        """Format count result."""
        if not rows or not rows[0].get("count"):
            return "No observations found."
        
        count = int(rows[0]["count"]["value"])
        return f"The dataset contains {count:,} observations matching your criteria."
    
    @staticmethod
    def format_daily_aggregates(rows: List[Dict[str, Any]], property_name: str = "value", 
                                scope_label: str = "") -> str:
        """Format daily aggregate results with scope clarification."""
        if not rows:
            return "No daily aggregate data found for the specified criteria."
        
        scope_text = f" ({scope_label})" if scope_label else ""
        lines = [f"Here are {len(rows)} daily means{scope_text}:"]
        lines.append("")
        
        for i, row in enumerate(rows[:31], 1):  # Show up to 31 days
            date = row.get("date", {}).get("value", "N/A")
            mean = row.get("mean", {}).get("value", "N/A")
            unit = row.get("unit", {}).get("value", "")
            unit_name = unit.split('/')[-1] if unit else ""
            unit_str = f" {unit_name}" if unit_name else ""
            
            try:
                mean_val = float(mean)
                lines.append(f"{i}. {date}: {mean_val:.2f}{unit_str}")
            except:
                lines.append(f"{i}. {date}: {mean}{unit_str}")
        
        if len(rows) > 31:
            lines.append(f"\\n... and {len(rows) - 31} more daily values.")
        
        lines.append("")
        lines.append("💡 *If you want ONE overall mean for the entire period, ask me to compute the monthly or overall mean.*")
        return "\\n".join(lines)
    
    @staticmethod
    def format_monthly_aggregates(rows: List[Dict[str, Any]], property_name: str = "value",
                                  scope_label: str = "") -> str:
        """Format monthly aggregate results with scope clarification."""
        if not rows:
            return "No monthly aggregate data found for the specified criteria."
        
        scope_text = f" ({scope_label})" if scope_label else ""
        lines = [f"Here are {len(rows)} monthly means{scope_text}:"]
        lines.append("")
        
        for i, row in enumerate(rows, 1):
            month = row.get("month", {}).get("value", "N/A")
            mean = row.get("mean", {}).get("value", "N/A")
            unit = row.get("unit", {}).get("value", "")
            unit_name = unit.split('/')[-1] if unit else ""
            unit_str = f" {unit_name}" if unit_name else ""
            
            try:
                mean_val = float(mean)
                lines.append(f"{i}. {month}: {mean_val:.2f}{unit_str}")
            except:
                lines.append(f"{i}. {month}: {mean}{unit_str}")
        
        return "\\n".join(lines)
    
    @staticmethod
    def add_context_line(property_uri: Optional[str], feature_uri: Optional[str], 
                        time_range: Optional[tuple], confidence: Optional[str] = None) -> str:
        """
        Generate context line showing what was used.
        
        Returns:
            String like "I used: Relative Humidity at location_123 during January 1950."
        """
        from src.parsers.property_resolver import property_resolver
        
        parts = []
        
        if property_uri:
            prop_name = property_resolver.get_property_display_name(property_uri)
            parts.append(prop_name)
        
        if feature_uri:
            location = feature_uri.split('/')[-1] if '/' in feature_uri else feature_uri
            parts.append(f"at {location}")
        
        if time_range:
            time_str = TimeParser.format_range(time_range[0], time_range[1])
            parts.append(f"during {time_str}")
        
        context = " ".join(parts) if parts else "the available data"
        
        result = f"📍 I used: {context}"
        
        if confidence:
            result += f"\\n💡 Note: {confidence}"
        
        return result
