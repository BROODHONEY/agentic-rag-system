"""Semantic search tool using vector similarity."""
from typing import Optional
from langchain.tools import Tool
from src.vectorstore.chroma_manager import get_vector_store
from src.utils.logger import logger
from src.utils.exceptions import ToolExecutionError


class SemanticSearchTool:
    """Tool for semantic search using vector similarity."""
    
    def __init__(self, top_k: Optional[int] = None):
        """Initialize semantic search tool."""
        self.top_k = top_k
        self.vectorstore = get_vector_store()
    
    def search(self, query: str) -> str:
        """Search the knowledge base using semantic similarity."""
        try:
            logger.info(f"Performing semantic search for: {query}")
            
            results = self.vectorstore.similarity_search(query=query, k=self.top_k)
            
            if not results:
                return "No relevant documents found in the knowledge base."
            
            # Format results
            formatted_results = []
            for i, result in enumerate(results, 1):
                content = result['content']
                metadata = result['metadata']
                source = metadata.get('source', 'Unknown')
                
                formatted_results.append(
                    f"Result {i}:\n"
                    f"Source: {source}\n"
                    f"Content: {content}\n"
                )
            
            output = "\n---\n".join(formatted_results)
            logger.info(f"Found {len(results)} relevant documents")
            
            return output
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            raise ToolExecutionError(f"Semantic search failed: {e}")
    
    def as_langchain_tool(self) -> Tool:
        """Convert to LangChain Tool format."""
        return Tool(
            name="semantic_search",
            func=self.search,
            description="""Search the knowledge base using semantic similarity.
            Use this tool when you need to find information related to concepts or topics.
            Input should be a natural language query.
            Returns the most relevant document chunks from the knowledge base."""
        )


def create_semantic_search_tool(top_k: Optional[int] = None) -> SemanticSearchTool:
    """Factory function to create a semantic search tool."""
    return SemanticSearchTool(top_k=top_k)