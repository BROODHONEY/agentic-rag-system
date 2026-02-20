"""LLM wrapper for Groq API integration."""
from typing import Optional, List, Dict, Any
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from config.settings import settings
from src.utils.logger import logger
from src.utils.exceptions import LLMError


class GroqLLM:
    """Wrapper for Groq LLM with error handling."""
    
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        """Initialize Groq LLM."""
        self.model = model or settings.default_model
        self.temperature = temperature or settings.temperature
        self.max_tokens = max_tokens or settings.max_tokens
        
        try:
            self.llm = ChatGroq(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                groq_api_key=settings.groq_api_key,
            )
            logger.info(f"Initialized Groq LLM with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Groq LLM: {e}")
            raise LLMError(f"LLM initialization failed: {e}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a response from the LLM."""
        try:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            response = self.llm.invoke(messages)
            logger.debug(f"Generated response: {response.content[:100]}...")
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise LLMError(f"Generation failed: {e}")


# Singleton instance
_llm_instance: Optional[GroqLLM] = None

def get_llm() -> GroqLLM:
    """Get or create the global LLM instance."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = GroqLLM()
    return _llm_instance