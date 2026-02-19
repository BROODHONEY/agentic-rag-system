"""ChromaDB vector store manager."""
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import settings
from src.utils.logger import logger
from src.utils.exceptions import VectorStoreError


class ChromaManager:
    """Manages ChromaDB vector store operations."""
    
    def __init__(
        self,
        collection_name: Optional[str] = None,
        persist_directory: Optional[str] = None,
    ):
        """Initialize ChromaDB manager."""
        self.collection_name = collection_name or settings.chroma_collection_name
        self.persist_directory = persist_directory or settings.chroma_persist_directory
        
        try:
            # Initialize embedding model
            logger.info("Loading embedding model...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.embedding_model
            )
            logger.info(f"Loaded embedding model: {settings.embedding_model}")
            
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                )
            )
            
            # Initialize or get collection
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
                client=self.client,
            )
            
            logger.info(f"Initialized ChromaDB collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise VectorStoreError(f"ChromaDB initialization failed: {e}")
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Add documents to the vector store."""
        try:
            from langchain.schema import Document
            
            docs = []
            for i, text in enumerate(documents):
                metadata = metadatas[i] if metadatas else {}
                docs.append(Document(page_content=text, metadata=metadata))
            
            doc_ids = self.vectorstore.add_documents(documents=docs, ids=ids)
            
            logger.info(f"Added {len(doc_ids)} documents to vector store")
            return doc_ids
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise VectorStoreError(f"Failed to add documents: {e}")
    
    def similarity_search(
        self,
        query: str,
        k: int = None,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        try:
            k = k or settings.top_k_results
            
            results = self.vectorstore.similarity_search(
                query=query,
                k=k,
                filter=filter,
            )
            
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                })
            
            logger.info(f"Found {len(formatted_results)} similar documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise VectorStoreError(f"Similarity search failed: {e}")
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection."""
        try:
            collection = self.client.get_collection(name=self.collection_name)
            count = collection.count()
            return count
        except Exception as e:
            logger.error(f"Error getting collection count: {e}")
            return 0
    
    def reset(self) -> None:
        """Reset the vector store (delete all documents)."""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.__init__(self.collection_name, self.persist_directory)
            logger.info("Vector store reset successfully")
        except Exception as e:
            logger.error(f"Error resetting vector store: {e}")
            raise VectorStoreError(f"Failed to reset vector store: {e}")


# Singleton instance
_chroma_instance: Optional[ChromaManager] = None

def get_chroma_manager() -> ChromaManager:
    """Get or create the global ChromaDB manager instance."""
    global _chroma_instance
    if _chroma_instance is None:
        _chroma_instance = ChromaManager()
    return _chroma_instance