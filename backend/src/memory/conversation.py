"""Conversation memory management."""
from typing import List, Dict, Any, Optional
from collections import defaultdict
from datetime import datetime
from src.utils.logger import logger


class ConversationMemory:
    """Manages conversation history and context."""
    
    def __init__(self, max_history: int = 10):
        """Initialize conversation memory."""
        self.max_history = max_history
        self.conversations: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        logger.info(f"Initialized conversation memory (max_history={max_history})")
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a message to conversation history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }
        
        self.conversations[conversation_id].append(message)
        
        # Trim history if needed
        if len(self.conversations[conversation_id]) > self.max_history * 2:
            self.conversations[conversation_id] = self.conversations[conversation_id][-(self.max_history * 2):]
        
        logger.debug(f"Added {role} message to conversation {conversation_id}")
    
    def get_history(
        self,
        conversation_id: str,
        n_messages: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Get conversation history."""
        history = self.conversations.get(conversation_id, [])
        
        if n_messages:
            return history[-n_messages:]
        
        return history
    
    def clear_history(self, conversation_id: str) -> None:
        """Clear conversation history."""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Cleared history for conversation {conversation_id}")