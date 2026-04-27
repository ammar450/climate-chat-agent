"""
Time range parser for natural language date expressions.
Enhanced with strict 1950-1951 validation and helpful error messages.
"""

import re
from datetime import datetime
from typing import Optional, Tuple, Dict


class DateValidationError(Exception):
    """Raised when date is outside available data range."""
    def __init__(self, message: str, suggested_query: Optional[str] = None):
        super().__init__(message)
        self.suggested_query = suggested_query


class TimeParser:
    # Data availability: 1950-2024
    DATA_START = "1950-01-01T00:00:00"
    DATA_END = "2025-01-01T00:00:00"
    MIN_YEAR = 1950
    MAX_YEAR = 2024
    """Parse natural language time expressions with strict validation."""
    
    MONTH_NAMES = {
        "january": 1, "jan": 1,
        "february": 2, "feb": 2,
        "march": 3, "mar": 3,
        "april": 4, "apr": 4,
        "may": 5,
        "june": 6, "jun": 6,
        "july": 7, "jul": 7,
        "august": 8, "aug": 8,
        "september": 9, "sep": 9, "sept": 9,
        "october": 10, "oct": 10,
        "november": 11, "nov": 11,
        "december": 12, "dec": 12
    }
    
    @classmethod
    def validate_year(cls, year: int) -> Dict[str, any]:
        """
        Validate if year is within 1950-1951 range.
        
        Returns:
            Dict with 'valid' (bool), 'message' (str), and 'suggestion' (str)
        """
        if year < cls.MIN_YEAR:
            return {
                'valid': False,
                'message': f"I notice you asked about {year}, but I only have climate data from 1950 to 2024.",
                'suggestion': f"Try asking about 1950 instead. For example: 'What was the temperature in 1950?'"
            }
        elif year > cls.MAX_YEAR:
            return {
                'valid': False,
                'message': f"I notice you asked about {year}, but I only have climate data from 1950 to 2024.",
                'suggestion': f"Try asking about 2024 instead. For example: 'Show me 2024 precipitation patterns'"
            }
        return {'valid': True, 'message': '', 'suggestion': ''}
    
    @classmethod
    def parse_specific_date(cls, text: str, strict: bool = True) -> Optional[Tuple[str, str, Optional[str]]]:
        """
        Parse a specific date in YYYY-MM-DD format.
        Returns the date range and a message if date was adjusted.
        
        Args:
            text: Input text to parse (should contain YYYY-MM-DD)
            strict: If True, find nearest available date if exact date doesn't exist
        
        Returns:
            Tuple of (start_datetime, end_datetime, availability_message) or None
            availability_message is set if we used a different date than requested
        """
        if not text:
            return None
        
        # Pattern: YYYY-MM-DD
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
        if not match:
            return None
        
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        
        requested_date_str = f"{year:04d}-{month:02d}-{day:02d}"
        
        # First, validate the date format (month 1-12, day 1-31)
        if month < 1 or month > 12:
            error_msg = f"Invalid date format: {requested_date_str}. Month must be between 01 and 12. I have data from 1950-01-01 to 2024-12-31."
            if strict:
                raise DateValidationError(error_msg)
            return None
        
        if day < 1 or day > 31:
            error_msg = f"Invalid date format: {requested_date_str}. Day must be between 01 and 31. I have data from 1950-01-01 to 2024-12-31."
            if strict:
                raise DateValidationError(error_msg)
            return None
        
        # Try to create a valid datetime to catch invalid combinations (like Feb 30)
        try:
            test_date = datetime(year, month, day)
        except ValueError as e:
            error_msg = f"Invalid date: {requested_date_str}. {str(e).capitalize()}. I have data from 1950-01-01 to 2024-12-31."
            if strict:
                raise DateValidationError(error_msg)
            return None
        
        # Validate date is within 1950-2024
        if year < cls.MIN_YEAR or year > cls.MAX_YEAR:
            if strict:
                # Find nearest available date
                if year < cls.MIN_YEAR:
                    # Use earliest available date
                    nearest_year = cls.MIN_YEAR
                    nearest_date_str = f"{nearest_year}-01-01"
                    message = f"Data for {requested_date_str} is not available. Showing data for {nearest_date_str} instead (earliest available date)."
                else:
                    # Use latest available date
                    nearest_year = cls.MAX_YEAR
                    nearest_date_str = f"{nearest_year}-12-31"
                    message = f"Data for {requested_date_str} is not available. Showing data for {nearest_date_str} instead (latest available date)."
                
                # Parse the nearest date
                parts = nearest_date_str.split('-')
                nearest_year = int(parts[0])
                nearest_month = int(parts[1])
                nearest_day = int(parts[2])
                
                start, end = cls.parse_day(nearest_year, nearest_month, nearest_day)
                return (start, end, message)
            else:
                return None
        
        # Date is within range and valid, return it
        start, end = cls.parse_day(year, month, day)
        return (start, end, None)  # No message needed, exact date exists
    
    @classmethod
    def parse(cls, text: str, strict: bool = True) -> Optional[Tuple[str, str]]:
        """
        Parse time range from natural language text.
        
        Args:
            text: Input text to parse
            strict: If True, raise error for dates outside 1950-1951
        
        Returns:
            Tuple of (start_datetime, end_datetime) in ISO format, or None
            
        Raises:
            DateValidationError: If strict=True and date is outside 1950-1951
        """
        if not text:
            return None
        
        text_lower = text.lower()
        
        # Pattern: "between YYYY and YYYY"
        match = re.search(r'between\s+(\d{4})\s+and\s+(\d{4})', text_lower)
        if match:
            start_year = int(match.group(1))
            end_year = int(match.group(2))
            
            if strict and (start_year < cls.MIN_YEAR or start_year > cls.MAX_YEAR or 
                          end_year < cls.MIN_YEAR or end_year > cls.MAX_YEAR):
                validation = cls.validate_year(start_year if start_year < cls.MIN_YEAR or start_year > cls.MAX_YEAR else end_year)
                raise DateValidationError(
                    validation['message'],
                    suggested_query=validation['suggestion']
                )
            
            return (f"{start_year}-01-01T00:00:00", f"{end_year + 1}-01-01T00:00:00")
        
        # Pattern: "from YYYY to YYYY"
        match = re.search(r'from\s+(\d{4})\s+to\s+(\d{4})', text_lower)
        if match:
            start_year = int(match.group(1))
            end_year = int(match.group(2))
            
            if strict and (start_year < cls.MIN_YEAR or start_year > cls.MAX_YEAR or 
                          end_year < cls.MIN_YEAR or end_year > cls.MAX_YEAR):
                validation = cls.validate_year(start_year if start_year < cls.MIN_YEAR or start_year > cls.MAX_YEAR else end_year)
                raise DateValidationError(
                    validation['message'],
                    suggested_query=validation['suggestion']
                )
            
            return (f"{start_year}-01-01T00:00:00", f"{end_year + 1}-01-01T00:00:00")
        
        # Pattern: "Month YYYY" or "YYYY Month"
        for month_name, month_num in cls.MONTH_NAMES.items():
            # Month YYYY
            pattern = rf'\b{month_name}\s+(\d{{4}})\b'
            match = re.search(pattern, text_lower)
            if match:
                year = int(match.group(1))
                
                if strict:
                    validation = cls.validate_year(year)
                    if not validation['valid']:
                        raise DateValidationError(
                            validation['message'],
                            suggested_query=validation['suggestion']
                        )
                
                return cls._month_year_to_range(year, month_num)
            
            # YYYY Month
            pattern = rf'\b(\d{{4}})\s+{month_name}\b'
            match = re.search(pattern, text_lower)
            if match:
                year = int(match.group(1))
                
                if strict:
                    validation = cls.validate_year(year)
                    if not validation['valid']:
                        raise DateValidationError(
                            validation['message'],
                            suggested_query=validation['suggestion']
                        )
                
                return cls._month_year_to_range(year, month_num)
        
        # Pattern: "in YYYY"
        match = re.search(r'\bin\s+(\d{4})\b', text_lower)
        if match:
            year = int(match.group(1))
            
            if strict:
                validation = cls.validate_year(year)
                if not validation['valid']:
                    raise DateValidationError(
                        validation['message'],
                        suggested_query=validation['suggestion']
                    )
            
            return (f"{year}-01-01T00:00:00", f"{year + 1}-01-01T00:00:00")
        
        # Pattern: standalone "YYYY"
        match = re.search(r'\b(\d{4})\b', text)
        if match:
            year = int(match.group(1))
            # Only if it looks like a reasonable year (1800-2100)
            if 1800 <= year <= 2100:
                if strict:
                    validation = cls.validate_year(year)
                    if not validation['valid']:
                        raise DateValidationError(
                            validation['message'],
                            suggested_query=validation['suggestion']
                        )
                
                return (f"{year}-01-01T00:00:00", f"{year + 1}-01-01T00:00:00")
        
        return None
    
    @classmethod
    def _month_year_to_range(cls, year: int, month: int) -> Tuple[str, str]:
        """Convert year and month to date range with exclusive end.
        
        Returns:
            (start, end) where start is first day of month at 00:00:00,
            end is first day of next month at 00:00:00 (exclusive).
        """
        start = datetime(year, month, 1)
        # Calculate first day of next month (exclusive end)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)
        
        return (start.strftime("%Y-%m-%dT%H:%M:%S"), end.strftime("%Y-%m-%dT%H:%M:%S"))
    
    @classmethod
    def is_within_available_data(cls, start: str, end: str) -> bool:
        """Check if requested time range is within available data (1950-1951)."""
        try:
            start_dt = datetime.fromisoformat(start.replace("Z", ""))
            end_dt = datetime.fromisoformat(end.replace("Z", ""))
            data_start_dt = datetime.fromisoformat(cls.DATA_START)
            data_end_dt = datetime.fromisoformat(cls.DATA_END)
            
            return start_dt >= data_start_dt and end_dt <= data_end_dt
        except:
            return True  # If can't parse, assume it's OK
    
    @classmethod
    def clip_to_available_data(cls, start: str, end: str) -> Tuple[str, str]:
        """Clip time range to available data period (1950-1951)."""
        try:
            start_dt = datetime.fromisoformat(start.replace("Z", ""))
            end_dt = datetime.fromisoformat(end.replace("Z", ""))
            data_start_dt = datetime.fromisoformat(cls.DATA_START)
            data_end_dt = datetime.fromisoformat(cls.DATA_END)
            
            # Clip to available range
            if start_dt < data_start_dt:
                start_dt = data_start_dt
            if end_dt > data_end_dt:
                end_dt = data_end_dt
            
            return (start_dt.strftime("%Y-%m-%dT%H:%M:%S"), end_dt.strftime("%Y-%m-%dT%H:%M:%S"))
        except:
            return start, end  # If can't parse, return as-is
    
    @classmethod
    def parse_day(cls, year: int, month: int, day: int) -> Tuple[str, str]:
        """Parse a specific day to range with exclusive end.
        
        Returns:
            (start, end) where start is YYYY-MM-DD 00:00:00,
            end is next day at 00:00:00 (exclusive).
        """
        from datetime import timedelta
        start = datetime(year, month, day)
        end = start + timedelta(days=1)
        return (start.strftime("%Y-%m-%dT%H:%M:%S"), end.strftime("%Y-%m-%dT%H:%M:%S"))
    
    @classmethod
    def extract_year_update(cls, text: str) -> Optional[int]:
        """
        Extract ANY year mentioned in text, including:
        - "set year to 1950"
        - "climate data for 1949"
        - "weather in 1960"
        - "show me 1951"
        - "data from 1950"
        - "what about 1952"
        
        Returns:
            Year as int if found, else None
        """
        text_lower = text.lower()
        
        # Comprehensive patterns for any year mention (4-digit years only)
        patterns = [
            r'(?:for|from|in|during|about|year|use|set|show|data for|climate for|weather in|now show|what about)\s+(\d{4})',
            r'(\d{4})\s+(?:data|climate|weather|observations)',
            r'year\s+(\d{4})',
            r'\b(1\d{3}|20\d{2})\b'  # Any year 1000-2099 as standalone
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                year = int(match.group(1))
                # Only return if it looks like a valid year (1900-2100)
                if 1900 <= year <= 2100:
                    return year
        
        return None
    
    @classmethod
    def extract_month_update(cls, text: str, current_year: Optional[int] = None) -> Optional[Tuple[str, str]]:
        """
        Extract month from follow-up like "what about February".
        
        Args:
            text: User message
            current_year: Previously selected year to use
            
        Returns:
            Time range tuple or None
        """
        if not current_year:
            return None
        
        text_lower = text.lower()
        
        for month_name, month_num in cls.MONTH_NAMES.items():
            if month_name in text_lower:
                return cls._month_year_to_range(current_year, month_num)
        
        return None
    
    @classmethod
    def validate_date_format(cls, text: str) -> bool:
        """
        Check if text contains a date-like pattern that should be validated.
        
        Returns:
            True if text contains a date pattern, False otherwise
        """
        # Check for patterns that look like dates
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY or DD/MM/YYYY
            r'\d{1,2}/\d{1,2}/\d{2,4}',  # M/D/YY or M/D/YYYY
        ]
        
        for pattern in date_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    @classmethod
    def format_range(cls, start: str, end: str) -> str:
        """Format time range for display."""
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            
            # Same year
            if start_dt.year == end_dt.year:
                # Same month
                if start_dt.month == end_dt.month:
                    return start_dt.strftime("%B %Y")
                else:
                    return f"{start_dt.strftime('%B')} - {end_dt.strftime('%B %Y')}"
            else:
                # Different years
                if start_dt.month == 1 and start_dt.day == 1 and end_dt.month == 1 and end_dt.day == 1:
                    # Full year(s)
                    if end_dt.year - start_dt.year == 1:
                        return str(start_dt.year)
                    else:
                        return f"{start_dt.year} - {end_dt.year - 1}"
                else:
                    return f"{start_dt.strftime('%b %Y')} - {end_dt.strftime('%b %Y')}"
        except:
            return f"{start} to {end}"
