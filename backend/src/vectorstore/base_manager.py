"""Base vector store manager interface."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseVectorStoreManager(ABC):
    """Abstract base class for vector store managers."""
    
    @abstractmethod
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Add documents to the vector store."""
        pass
    
    @abstractmethod
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        pass
    
    @abstractmethod
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection."""
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """Reset the vector store (delete all documents)."""
        pass
    
    @abstractmethod
    def get_all_documents(self) -> Dict[str, Any]:
        """Get all documents with their chunks and embeddings."""
        pass
    
    @abstractmethod
    def delete_by_source(self, source: str) -> int:
        """Delete all documents with a specific source."""
        pass
