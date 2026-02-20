"""Custom exceptions for the Agentic RAG system."""

class AgenticRAGException(Exception):
    """Base exception for all Agentic RAG errors."""
    pass

class LLMError(AgenticRAGException):
    """Error related to LLM operations."""
    pass

class VectorStoreError(AgenticRAGException):
    """Error related to vector store operations."""
    pass

class DocumentProcessingError(AgenticRAGException):
    """Error related to document processing."""
    pass

class RetrievalError(AgenticRAGException):
    """Error related to document retrieval."""
    pass

class ToolExecutionError(AgenticRAGException):
    """Error related to tool execution."""
    pass