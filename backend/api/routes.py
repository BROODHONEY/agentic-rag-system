"""API routes for Agentic RAG system."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from typing import Dict, Optional
import uuid
import tempfile
import os

from api.schemas import (
    QueryRequest, 
    QueryResponse, 
    IngestResponse, 
    StatsResponse,
    MessageResponse
)
from src.core.agent import create_agentic_rag
from src.processing.loaders import DocumentLoader
from src.processing.chunkers import DocumentChunker
from src.vectorstore.chroma_manager import get_vector_store
from src.utils.logger import logger


router = APIRouter()

# Initialize Agentic RAG system (singleton)
try:
    rag_system = create_agentic_rag()
    logger.info("RAG system initialized for API")
except Exception as e:
    logger.error(f"Failed to initialize RAG system: {e}")
    rag_system = None


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Query the Agentic RAG system.
    
    - **question**: The question to ask
    - **conversation_id**: Optional conversation ID for maintaining context
    
    Returns the answer with metadata.
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        logger.info(f"Received query: {request.question}")
        
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Process query
        result = rag_system.query(
            question=request.question,
            conversation_id=conversation_id,
        )
        
        return QueryResponse(
            answer=result["answer"],
            question=request.question,
            conversation_id=conversation_id,
            metadata=result["metadata"],
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingest a document into the knowledge base.
    
    - **file**: Document file (PDF, DOCX, TXT)
    
    Returns ingestion status and metadata.
    """
    try:
        logger.info(f"Ingesting document: {file.filename}")
        
        # Validate file extension
        allowed_extensions = ['.pdf', '.docx', '.txt']
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Allowed: {allowed_extensions}"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Load document
            documents = DocumentLoader.load_document(tmp_file_path)
            logger.info(f"Loaded {len(documents)} pages/sections")
            
            # Chunk documents
            chunks = DocumentChunker.recursive_chunk(documents)
            logger.info(f"Created {len(chunks)} chunks")
            
            # Add to vector store
            vectorstore = get_vector_store()
            doc_ids = vectorstore.add_documents(
                documents=[chunk.page_content for chunk in chunks],
                metadatas=[chunk.metadata for chunk in chunks],
            )
            
            logger.info(f"Successfully ingested {len(doc_ids)} chunks")
            
            return IngestResponse(
                status="success",
                message=f"Successfully ingested {file.filename}",
                metadata={
                    "filename": file.filename,
                    "num_chunks": len(chunks),
                    "num_documents": len(documents),
                    "total_in_db": vectorstore.get_collection_count()
                }
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get system statistics.
    
    Returns information about the vector store and agent.
    """
    try:
        from config.settings import settings
        
        vectorstore = get_vector_store()
        doc_count = vectorstore.get_collection_count()
        
        # Determine vector store type and details
        vector_store_type = settings.vector_store_type
        if vector_store_type == "pinecone":
            store_location = "Cloud (Pinecone)"
            collection_name = getattr(vectorstore, 'index_name', settings.pinecone_index_name)
        else:
            store_location = getattr(vectorstore, 'persist_directory', './data/vectorstore')
            collection_name = getattr(vectorstore, 'collection_name', settings.chroma_collection_name)
        
        stats = StatsResponse(
            vector_store={
                "type": vector_store_type.upper(),
                "collection": collection_name,
                "document_count": doc_count,
                "persist_directory": store_location,
                "embedding_model": settings.embedding_model,
            },
            agent={
                "tools": rag_system.get_tool_names() if rag_system else [],
                "model": rag_system.llm.model if rag_system else "N/A",
                "memory_enabled": rag_system.use_memory if rag_system else False,
                "temperature": settings.temperature,
                "max_tokens": settings.max_tokens,
                "top_k": settings.top_k_results,
            }
        )
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversation/{conversation_id}", response_model=MessageResponse)
async def clear_conversation(conversation_id: str):
    """
    Clear conversation history.
    
    - **conversation_id**: The conversation ID to clear
    
    Returns status message.
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        rag_system.clear_memory(conversation_id)
        
        return MessageResponse(
            status="success",
            message=f"Cleared conversation {conversation_id}"
        )
        
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset", response_model=MessageResponse)
async def reset_vector_store():
    """
    Reset the vector store (delete all documents).
    
    ⚠️ WARNING: This will delete all documents from the vector database!
    
    Returns status message.
    """
    try:
        vectorstore = get_vector_store()
        vectorstore.reset()
        
        return MessageResponse(
            status="success",
            message="Vector store reset successfully"
        )
        
    except Exception as e:
        logger.error(f"Error resetting vector store: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{source:path}", response_model=MessageResponse)
async def delete_document(source: str):
    """
    Delete a specific document and all its chunks from the vector store.
    
    - **source**: The source path/filename of the document to delete
    
    Returns status message.
    """
    try:
        vectorstore = get_vector_store()
        
        # Delete by source
        deleted_count = vectorstore.delete_by_source(source)
        
        if deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No documents found with source: {source}"
            )
        
        logger.info(f"Deleted {deleted_count} chunks from document: {source}")
        
        return MessageResponse(
            status="success",
            message=f"Deleted document '{source}' ({deleted_count} chunks)"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=Dict)
async def search_documents(query: str, k: int = 5):
    """
    Search the vector store directly (without agent).
    
    - **query**: Search query
    - **k**: Number of results to return (default: 5)
    
    Returns raw search results.
    """
    try:
        vectorstore = get_vector_store()
        results = vectorstore.similarity_search(query, k=k)
        
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error in search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents", response_model=Dict)
async def get_all_documents():
    """
    Get all documents with their chunks and embeddings info.
    
    Returns all documents grouped by source file.
    """
    try:
        vectorstore = get_vector_store()
        
        # Get all documents
        result = vectorstore.get_all_documents()
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))