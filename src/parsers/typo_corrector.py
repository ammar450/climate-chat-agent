"""
Typo correction for common climate-related terms.
"""

from typing import Dict, Tuple, Optional


class TypoCorrector:
    """Corrects common typos in climate-related queries."""
    
    # Common climate typos dictionary
    TYPO_MAP: Dict[str, str] = {
        # Temperature
        "temprature": "temperature",
        "temperture": "temperature",
        "tempature": "temperature",
        "temperatur": "temperature",
        "temerature": "temperature",
        
        # Precipitation
        "precipitaion": "precipitation",
        "percipitation": "precipitation",
        "precipiation": "precipitation",
        "precipation": "precipitation",
        "preciptation": "precipitation",
        "precipitaton": "precipitation",
        
        # Rainfall
        "rainfal": "rainfall",
        "rainfalll": "rainfall",
        "ranfall": "rainfall",
        
        # Humidity
        "humidty": "humidity",
        "humididy": "humidity",
        "humidy": "humidity",
        "humdity": "humidity",
        
        # Pressure
        "presure": "pressure",
        "pressur": "pressure",
        "preasure": "pressure",
        
        # Weather
        "wheather": "weather",
        "wether": "weather",
        "wheater": "weather",
        
        # Climate
        "climat": "climate",
        "clmate": "climate",
        
        # Data
        "dat": "data",
        "dta": "data",
        
        # Average
        "averge": "average",
        "avrage": "average",
        "avarage": "average",
        
        # Monthly
        "montly": "monthly",
        "monthy": "monthly",
        
        # Daily
        "daly": "daily",
        "dayly": "daily",
    }
    
    @classmethod
    def correct(cls, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Correct typos in text and return corrected text with corrections made.
        
        Args:
            text: Input text that may contain typos
            
        Returns:
            Tuple of (corrected_text, corrections_dict)
            where corrections_dict maps typo -> correct_word
        """
        # Quick check - if no potential typos in text, return immediately
        text_lower = text.lower()
        has_potential_typo = any(typo in text_lower for typo in ['temp', 'precip', 'humid', 'rain', 'aver'])
        if not has_potential_typo:
            return text, {}
        
        corrections_made = {}
        words = text.split()
        corrected_words = []
        
        for word in words:
            word_clean = word.lower().strip('.,!?;:')
            
            # Check if word is a typo
            if word_clean in cls.TYPO_MAP:
                correct_word = cls.TYPO_MAP[word_clean]
                corrections_made[word_clean] = correct_word
                
                # Preserve case
                if word[0].isupper():
                    corrected_word = correct_word.capitalize()
                else:
                    corrected_word = correct_word
                
                # Restore punctuation
                for char in word:
                    if char in '.,!?;:':
                        corrected_word += char
                        break
                
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)
        
        corrected_text = ' '.join(corrected_words)
        return corrected_text, corrections_made
    
    @classmethod
    def format_correction_message(cls, corrections: Dict[str, str]) -> Optional[str]:
        """
        Format a friendly correction message.
        
        Args:
            corrections: Dictionary of typo -> correct word
            
        Returns:
            Formatted message or None if no corrections
        """
        if not corrections:
            return None
        
        if len(corrections) == 1:
            typo, correct = list(corrections.items())[0]
            return f"💡 I assumed you meant **{correct}** (you wrote '{typo}')"
        else:
            items = [f"'{typo}' → **{correct}**" for typo, correct in corrections.items()]
            return f"💡 I corrected some typos: {', '.join(items)}"
    
    @classmethod
    def check_and_correct(cls, text: str) -> Tuple[str, Optional[str]]:
        """
        Check text for typos, correct them, and return corrected text with message.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (corrected_text, correction_message)
        """
        corrected_text, corrections = cls.correct(text)
        message = cls.format_correction_message(corrections)
        
        return corrected_text, message
