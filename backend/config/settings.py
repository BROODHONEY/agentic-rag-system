"""Application configuration settings."""
from pydantic_settings import BaseSettings
from typing import Optional, Literal
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys - make it optional with default to avoid immediate error
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    
    # LLM Configuration
    default_model: str = os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
    temperature: float = 0.0
    max_tokens: int = 1024
    
    # Vector Store Configuration
    vector_store_type: Literal["chroma", "pinecone"] = os.getenv("VECTOR_STORE_TYPE", "chroma")
    
    # ChromaDB Configuration (local)
    chroma_persist_directory: str = "./data/vectorstore"
    chroma_collection_name: str = "documents"
    
    # Pinecone Configuration (cloud)
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "agentic-rag")
    
    # Embedding Configuration
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Retrieval Configuration
    top_k_results: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Don't error if .env doesn't exist
        env_file_optional = True


# Create settings instance
try:
    settings = Settings()
    
    # Create necessary directories
    os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
    os.makedirs(settings.chroma_persist_directory, exist_ok=True)
    os.makedirs("./data/raw", exist_ok=True)
    os.makedirs("./data/processed", exist_ok=True)
    
except Exception as e:
    print(f"Warning: Error loading settings: {e}")
    # Create a minimal settings object if loading fails
    settings = Settings()