"""Document loaders for various file formats."""
from typing import List
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from langchain.schema import Document
from src.utils.logger import logger
from src.utils.exceptions import DocumentProcessingError


class DocumentLoader:
    """Unified document loader for multiple file formats."""
    
    SUPPORTED_EXTENSIONS = {
        '.pdf': PyPDFLoader,
        '.docx': Docx2txtLoader,
        '.txt': TextLoader,
    }
    
    @classmethod
    def load_document(cls, file_path: str) -> List[Document]:
        """Load a document from file."""
        try:
            path = Path(file_path)
            
            if not path.exists():
                raise DocumentProcessingError(f"File not found: {file_path}")
            
            extension = path.suffix.lower()
            
            if extension not in cls.SUPPORTED_EXTENSIONS:
                raise DocumentProcessingError(
                    f"Unsupported file type: {extension}"
                )
            
            # Get appropriate loader
            loader_class = cls.SUPPORTED_EXTENSIONS[extension]
            loader = loader_class(str(path))
            
            # Load documents
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} pages from {file_path}")
            
            # Add metadata
            for doc in documents:
                doc.metadata['source'] = str(path)
                doc.metadata['file_type'] = extension
            
            return documents
            
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {e}")
            raise DocumentProcessingError(f"Failed to load document: {e}")
    
    @classmethod
    def load_directory(cls, directory_path: str) -> List[Document]:
        """Load all supported documents from a directory."""
        try:
            directory = Path(directory_path)
            
            if not directory.exists():
                raise DocumentProcessingError(f"Directory not found: {directory_path}")
            
            all_documents = []
            
            for file_path in directory.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in cls.SUPPORTED_EXTENSIONS:
                    try:
                        documents = cls.load_document(str(file_path))
                        all_documents.extend(documents)
                    except Exception as e:
                        logger.warning(f"Skipping {file_path}: {e}")
                        continue
            
            logger.info(f"Loaded {len(all_documents)} total documents from {directory_path}")
            return all_documents
            
        except Exception as e:
            logger.error(f"Error loading directory {directory_path}: {e}")
            raise DocumentProcessingError(f"Failed to load directory: {e}")