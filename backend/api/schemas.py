"""Pydantic schemas for API request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    question: str = Field(..., description="User's question", min_length=1)
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is machine learning?",
                "conversation_id": "session-123"
            }
        }


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    answer: str = Field(..., description="Generated answer")
    question: str = Field(..., description="Original question")
    conversation_id: Optional[str] = Field(None, description="Conversation ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Machine learning is a subset of AI that focuses on...",
                "question": "What is machine learning?",
                "conversation_id": "session-123",
                "metadata": {
                    "model": "mixtral-8x7b-32768",
                    "tools_used": 1
                }
            }
        }


class IngestResponse(BaseModel):
    """Response model for document ingestion."""
    status: str = Field(..., description="Ingestion status")
    message: str = Field(..., description="Status message")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Ingestion metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Successfully ingested document.pdf",
                "metadata": {
                    "filename": "document.pdf",
                    "num_chunks": 42,
                    "num_documents": 10
                }
            }
        }


class StatsResponse(BaseModel):
    """Response model for system statistics."""
    vector_store: Dict[str, Any]
    agent: Dict[str, Any]


class MessageResponse(BaseModel):
    """Generic message response."""
    status: str
    message: str