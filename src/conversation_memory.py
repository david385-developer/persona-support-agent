"""
Conversation Memory Module

Tracks multi-turn conversation state per session.
Like maintaining session state in a web app.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ConversationState:
    """State for one conversation session."""
    session_id: str
    history: list = field(default_factory=list)
    detected_persona: Optional[str] = None
    persona_confidence: float = 0.0
    sources_used: list = field(default_factory=list)
    is_escalated: bool = False


class ConversationMemory:
    """Manages conversation state across sessions."""

    def __init__(self):
        self.sessions: dict[str, ConversationState] = {}

    def get_or_create(self, session_id: str) -> ConversationState:
        """Get existing session or create new one."""
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationState(session_id=session_id)
        return self.sessions[session_id]

    def add_user_message(self, session_id: str, message: str):
        """Record a user message."""
        state = self.get_or_create(session_id)
        state.history.append({"role": "user", "content": message})

    def add_assistant_message(
        self, session_id: str, message: str, sources: list = None
    ):
        """Record an assistant response."""
        state = self.get_or_create(session_id)
        state.history.append({"role": "assistant", "content": message})
        if sources:
            state.sources_used.extend(sources)

    def update_persona(self, session_id: str, persona: str, confidence: float):
        """Update detected persona for the session."""
        state = self.get_or_create(session_id)
        if confidence > state.persona_confidence or state.detected_persona is None:
            state.detected_persona = persona
            state.persona_confidence = confidence

    def get_history(self, session_id: str) -> list:
        """Get all messages in this session."""
        return self.get_or_create(session_id).history

    def get_turn_count(self, session_id: str) -> int:
        """Count how many user messages in this session."""
        state = self.get_or_create(session_id)
        return sum(1 for h in state.history if h["role"] == "user")

    def mark_escalated(self, session_id: str):
        """Mark session as escalated."""
        self.get_or_create(session_id).is_escalated = True