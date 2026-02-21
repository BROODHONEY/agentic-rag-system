"""Pinecone vector store manager for cloud storage."""
from typing import List, Dict, Any, Optional
import uuid
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import settings
from src.utils.logger import logger
from src.utils.exceptions import VectorStoreError
from src.vectorstore.base_manager import BaseVectorStoreManager

try:
    from pinecone import Pinecone, ServerlessSpec
    from langchain_pinecone import PineconeVectorStore
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    logger.warning("Pinecone not installed. Install with: pip install pinecone-client langchain-pinecone")


class PineconeManager(BaseVectorStoreManager):
    """Manages Pinecone vector store operations (cloud-based)."""
    
    def __init__(
        self,
        index_name: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """Initialize Pinecone manager."""
        if not PINECONE_AVAILABLE:
            raise VectorStoreError("Pinecone is not installed. Install with: pip install pinecone-client langchain-pinecone")
        
        self.index_name = index_name or settings.pinecone_index_name
        self.api_key = api_key or settings.pinecone_api_key
        
        if not self.api_key:
            raise VectorStoreError("Pinecone API key not provided")
        
        try:
            # Initialize embedding model
            logger.info("Loading embedding model...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.embedding_model
            )
            logger.info(f"Loaded embedding model: {settings.embedding_model}")
            
            # Initialize Pinecone client
            self.pc = Pinecone(api_key=self.api_key)
            
            # Create index if it doesn't exist
            if self.index_name not in self.pc.list_indexes().names():
                logger.info(f"Creating Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=384,  # all-MiniLM-L6-v2 dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
            
            # Initialize vector store
            self.index = self.pc.Index(self.index_name)
            self.vectorstore = PineconeVectorStore(
                index=self.index,
                embedding=self.embeddings,
                text_key="text",
            )
            
            logger.info(f"Initialized Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            raise VectorStoreError(f"Pinecone initialization failed: {e}")
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Add documents to the vector store."""
        try:
            from langchain.schema import Document
            
            # Generate IDs if not provided
            if ids is None:
                ids = [str(uuid.uuid4()) for _ in documents]
            
            docs = []
            for i, text in enumerate(documents):
                metadata = metadatas[i] if metadatas else {}
                metadata['id'] = ids[i]  # Store ID in metadata
                docs.append(Document(page_content=text, metadata=metadata))
            
            self.vectorstore.add_documents(documents=docs, ids=ids)
            
            logger.info(f"Added {len(ids)} documents to Pinecone")
            return ids
            
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
            stats = self.index.describe_index_stats()
            return stats.total_vector_count
        except Exception as e:
            logger.error(f"Error getting collection count: {e}")
            return 0
    
    def get_all_documents(self) -> Dict[str, Any]:
        """Get all documents with their chunks and embeddings."""
        try:
            # Pinecone doesn't support fetching all vectors easily
            # We'll use a workaround by querying with a dummy vector
            stats = self.index.describe_index_stats()
            total_count = stats.total_vector_count
            
            if total_count == 0:
                return {
                    'documents': [],
                    'total_documents': 0,
                    'total_chunks': 0,
                }
            
            # Fetch vectors in batches using list operation
            all_vectors = []
            for ids_batch in self._get_all_ids():
                fetch_response = self.index.fetch(ids=ids_batch)
                all_vectors.extend(fetch_response.vectors.values())
            
            # Group by source
            documents_by_source = {}
            
            for vector in all_vectors:
                metadata = vector.metadata
                content = metadata.get('text', '')
                source = metadata.get('source', 'Unknown')
                
                if source not in documents_by_source:
                    documents_by_source[source] = {
                        'source': source,
                        'chunks': [],
                        'total_chunks': 0,
                    }
                
                chunk_info = {
                    'id': vector.id,
                    'content': content,
                    'metadata': metadata,
                    'embedding_dim': len(vector.values) if vector.values else 0,
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
    
    def _get_all_ids(self):
        """Helper to get all vector IDs in batches."""
        # This is a simplified version - in production you'd want pagination
        try:
            # Query with a dummy vector to get IDs
            dummy_query = [0.0] * 384
            results = self.index.query(
                vector=dummy_query,
                top_k=10000,
                include_metadata=True
            )
            return [[match.id for match in results.matches]]
        except:
            return []
    
    def delete_by_source(self, source: str) -> int:
        """Delete all documents with a specific source."""
        try:
            # Delete by metadata filter
            self.index.delete(filter={"source": source})
            logger.info(f"Deleted documents with source: {source}")
            return 1  # Pinecone doesn't return count
            
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            raise VectorStoreError(f"Failed to delete documents: {e}")
    
    def reset(self) -> None:
        """Reset the vector store (delete all documents)."""
        try:
            # Delete all vectors
            self.index.delete(delete_all=True)
            logger.info("Pinecone index reset successfully")
        except Exception as e:
            logger.error(f"Error resetting Pinecone: {e}")
            raise VectorStoreError(f"Failed to reset Pinecone: {e}")
