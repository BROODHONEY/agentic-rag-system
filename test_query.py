"""Test the complete RAG system."""
from src.core.agent import create_agentic_rag

# Initialize the system
print("Initializing Agentic RAG system...")
rag = create_agentic_rag()

# Test query
question = "What is RAG?"
print(f"\nQuestion: {question}")
print("Thinking...\n")

result = rag.query(question)

print(f"Answer: {result['answer']}")
print(f"\nMetadata: {result['metadata']}")