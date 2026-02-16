"""
Session state management for conversation memory.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import threading

class SessionState:
    """Session state for tracking conversation context."""
    
    def __init__(self):
        self.selected_property_uri: Optional[str] = None
        self.selected_feature_uri: Optional[str] = None
        self.time_range: Optional[tuple] = None  # (start, end)
        self.last_template: Optional[str] = None
        self.last_results: Optional[list] = None
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()
    
    def update(self, **kwargs):
        """Update state fields."""
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "property_uri": self.selected_property_uri,
            "feature_uri": self.selected_feature_uri,
            "time_range": self.time_range,
            "last_template": self.last_template
        }


class SessionStore:
    """Thread-safe in-memory session store."""
    
    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}
        self._lock = threading.Lock()
    
    def get(self, session_id: str) -> SessionState:
        """Get or create session state."""
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = SessionState()
            return self._sessions[session_id]
    
    def reset(self, session_id: str):
        """Reset session state."""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
    
    def cleanup_old(self, max_age_hours: int = 24):
        """Remove sessions older than max_age_hours."""
        with self._lock:
            now = datetime.now()
            to_remove = []
            for sid, state in self._sessions.items():
                age = (now - state.updated_at).total_seconds() / 3600
                if age > max_age_hours:
                    to_remove.append(sid)
            for sid in to_remove:
                del self._sessions[sid]
    
    def count(self) -> int:
        """Get number of active sessions."""
        with self._lock:
            return len(self._sessions)


# Global session store
session_store = SessionStore()
