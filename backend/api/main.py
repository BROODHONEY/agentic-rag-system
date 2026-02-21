"""FastAPI application for Agentic RAG system."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import router
from config.settings import settings
from src.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    logger.info("=" * 60)
    logger.info("🚀 Starting Agentic RAG API Server")
    logger.info("=" * 60)
    logger.info(f"Model: {settings.default_model}")
    logger.info(f"Vector Store: {settings.chroma_persist_directory}")
    logger.info(f"API Port: {settings.api_port}")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("=" * 60)
    logger.info("🛑 Shutting down Agentic RAG API Server")
    logger.info("=" * 60)


# Create FastAPI app
app = FastAPI(
    title="Agentic RAG API",
    description="API for Agentic Retrieval-Augmented Generation system powered by Groq and ChromaDB",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["Agentic RAG"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Agentic RAG API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "query": "/api/v1/query",
            "ingest": "/api/v1/ingest",
            "stats": "/api/v1/stats",
            "search": "/api/v1/search",
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    try:
        from src.vectorstore.chroma_manager import get_vector_store
        from config.settings import settings
        
        vectorstore = get_vector_store()
        doc_count = vectorstore.get_collection_count()
        
        return {
            "status": "healthy",
            "model": settings.default_model,
            "vector_store": settings.vector_store_type,
            "documents": doc_count,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


def main():
    """Run the FastAPI application."""
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,  # Set to False in production
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()