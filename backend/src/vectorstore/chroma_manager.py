"""ChromaDB vector store manager."""
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import settings
from src.utils.logger import logger
from src.utils.exceptions import VectorStoreError
from src.vectorstore.base_manager import BaseVectorStoreManager


class ChromaManager(BaseVectorStoreManager):
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
    
    def get_all_documents(self) -> Dict[str, Any]:
        """Get all documents with their chunks and embeddings."""
        try:
            collection = self.client.get_collection(name=self.collection_name)
            
            # Get all documents from collection
            all_data = collection.get(include=['documents', 'metadatas', 'embeddings'])
            
            # Group by source file
            documents_by_source = {}
            
            for i, (doc_id, content, metadata, embedding) in enumerate(zip(
                all_data['ids'],
                all_data['documents'],
                all_data['metadatas'],
                all_data['embeddings'] if all_data['embeddings'] else [None] * len(all_data['ids'])
            )):
                source = metadata.get('source', 'Unknown')
                
                if source not in documents_by_source:
                    documents_by_source[source] = {
                        'source': source,
                        'chunks': [],
                        'total_chunks': 0,
                    }
                
                chunk_info = {
                    'id': doc_id,
                    'content': content,
                    'metadata': metadata,
                    'embedding_dim': len(embedding) if embedding else 0,
                    'content_length': len(content),
                }
                
                documents_by_source[source]['chunks'].append(chunk_info)
                documents_by_source[source]['total_chunks'] += 1
            
            return {
                'documents': list(documents_by_source.values()),
                'total_documents': len(documents_by_source),
                'total_chunks': sum(d['total_chunks'] for d in documents_by_source.values()),
            }
            
        except Exception as e:
            logger.error(f"Error getting documents: {e}")
            raise VectorStoreError(f"Failed to get documents: {e}")
    
    def delete_by_source(self, source: str) -> int:
        """Delete all documents with a specific source."""
        try:
            collection = self.client.get_collection(name=self.collection_name)
            
            # Get all document IDs with matching source
            all_data = collection.get(
                where={"source": source},
                include=['metadatas']
            )
            
            if not all_data['ids']:
                return 0
            
            # Delete all chunks from this document
            collection.delete(ids=all_data['ids'])
            
            logger.info(f"Deleted {len(all_data['ids'])} chunks from document: {source}")
            return len(all_data['ids'])
            
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            raise VectorStoreError(f"Failed to delete documents: {e}")


# Singleton instance
_chroma_instance: Optional[ChromaManager] = None

def get_chroma_manager() -> ChromaManager:
    """Get or create the global ChromaDB manager instance."""
    global _chroma_instance
    if _chroma_instance is None:
        _chroma_instance = ChromaManager()
    return _chroma_instance


def get_vector_store():
    """Get the configured vector store (ChromaDB or Pinecone)."""
    from config.settings import settings
    
    if settings.vector_store_type == "pinecone":
        from src.vectorstore.pinecone_manager import PineconeManager
        return PineconeManager()
    else:
        return get_chroma_manager()