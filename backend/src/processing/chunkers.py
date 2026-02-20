"""Text chunking strategies."""
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config.settings import settings
from src.utils.logger import logger
from src.utils.exceptions import DocumentProcessingError


class DocumentChunker:
    """Handles document chunking."""
    
    @staticmethod
    def recursive_chunk(
        documents: List[Document],
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ) -> List[Document]:
        """Chunk documents using recursive character splitting."""
        try:
            chunk_size = chunk_size or settings.chunk_size
            chunk_overlap = chunk_overlap or settings.chunk_overlap
            
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\n\n", "\n", ". ", " ", ""],
                length_function=len,
            )
            
            chunks = splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
            
            # Add chunk metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata['chunk_id'] = i
                chunk.metadata['chunk_size'] = len(chunk.page_content)
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error in chunking: {e}")
            raise DocumentProcessingError(f"Chunking failed: {e}")