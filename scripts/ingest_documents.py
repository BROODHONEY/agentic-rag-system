"""Script to ingest documents into the vector store."""
import argparse
from pathlib import Path
from src.processing.loaders import DocumentLoader
from src.processing.chunkers import DocumentChunker
from src.vectorstore.chroma_manager import get_chroma_manager
from src.utils.logger import logger


def ingest_document(file_path: str) -> None:
    """Ingest a single document."""
    try:
        logger.info(f"Loading document: {file_path}")
        
        # Load document
        documents = DocumentLoader.load_document(file_path)
        logger.info(f"Loaded {len(documents)} pages/sections")
        
        # Chunk documents
        logger.info("Chunking documents...")
        chunks = DocumentChunker.recursive_chunk(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        # Add to vector store
        logger.info("Adding to vector store...")
        chroma = get_chroma_manager()
        doc_ids = chroma.add_documents(
            documents=[chunk.page_content for chunk in chunks],
            metadatas=[chunk.metadata for chunk in chunks],
        )
        
        logger.info(f"✅ Successfully ingested {len(doc_ids)} chunks")
        logger.info(f"Total documents in collection: {chroma.get_collection_count()}")
        
    except Exception as e:
        logger.error(f"❌ Error ingesting document: {e}")
        raise


def ingest_directory(directory_path: str) -> None:
    """Ingest all documents in a directory."""
    try:
        logger.info(f"Loading documents from directory: {directory_path}")
        
        # Load all documents
        documents = DocumentLoader.load_directory(directory_path)
        
        if not documents:
            logger.warning("No documents found in directory!")
            return
        
        logger.info(f"Loaded {len(documents)} total pages/sections")
        
        # Chunk documents
        logger.info("Chunking documents...")
        chunks = DocumentChunker.recursive_chunk(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        # Add to vector store in batches
        batch_size = 100
        chroma = get_chroma_manager()
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            logger.info(f"Adding batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
            
            chroma.add_documents(
                documents=[chunk.page_content for chunk in batch],
                metadatas=[chunk.metadata for chunk in batch],
            )
        
        logger.info(f"✅ Successfully ingested all documents")
        logger.info(f"Total documents in collection: {chroma.get_collection_count()}")
        
    except Exception as e:
        logger.error(f"❌ Error ingesting directory: {e}")
        raise


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Ingest documents into vector store")
    parser.add_argument("path", type=str, help="Path to document file or directory")
    
    args = parser.parse_args()
    path = Path(args.path)
    
    if not path.exists():
        logger.error(f"❌ Path does not exist: {path}")
        return
    
    if path.is_file():
        ingest_document(str(path))
    elif path.is_dir():
        ingest_directory(str(path))
    else:
        logger.error(f"❌ Invalid path: {path}")


if __name__ == "__main__":
    main()