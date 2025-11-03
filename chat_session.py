from typing import Dict, List, Optional
from datetime import datetime
import uuid

class ChatSession:
    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.messages = []
        self.context = {}
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add message to chat session"""
        message = {
            'role': role,  # 'user' or 'assistant'
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.messages.append(message)
        self.last_activity = datetime.now()
    
    def get_conversation_context(self) -> str:
        """Get formatted conversation context for AI prompts"""
        context_lines = []
        for msg in self.messages[-5:]:  # Last 5 messages for context
            role = "Human" if msg['role'] == 'user' else "Assistant"
            context_lines.append(f"{role}: {msg['content']}")
        return "\n".join(context_lines)
    
    def update_context(self, key: str, value):
        """Update session context"""
        self.context[key] = value
        self.last_activity = datetime.now()
    
    def get_context(self, key: str, default=None):
        """Get value from session context"""
        return self.context.get(key, default)

class ChatManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self) -> str:
        """Create new chat session"""
        session = ChatSession()
        self.sessions[session.session_id] = session
        return session.session_id
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get existing chat session"""
        return self.sessions.get(session_id)
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Remove sessions older than max_age_hours"""
        cutoff = datetime.now().timestamp() - (max_age_hours * 3600)
        
        expired_sessions = [
            sid for sid, session in self.sessions.items()
            if session.last_activity.timestamp() < cutoff
        ]
        
        for sid in expired_sessions:
            del self.sessions[sid]
        
        return len(expired_sessions)