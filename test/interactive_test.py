"""Interactive RAG system testing."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.agent import create_agentic_rag
import uuid

def main():
    print("\n" + "="*60)
    print("🤖 Interactive Agentic RAG System")
    print("="*60)
    print("\nCommands:")
    print("  - Type your question to query the system")
    print("  - Type 'quit' or 'exit' to stop")
    print("  - Type 'stats' to see vector store stats")
    print("="*60 + "\n")
    
    # Initialize system
    print("Loading system...")
    rag = create_agentic_rag()
    conversation_id = str(uuid.uuid4())
    
    from src.vectorstore.chroma_manager import get_chroma_manager
    chroma = get_chroma_manager()
    
    print(f"✅ Ready! ({chroma.get_collection_count()} documents loaded)\n")
    
    while True:
        try:
            question = input("You: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit']:
                print("\n👋 Goodbye!")
                break
            
            if question.lower() == 'stats':
                count = chroma.get_collection_count()
                print(f"\n📊 Vector Store Stats:")
                print(f"   Documents: {count}")
                print(f"   Collection: {chroma.collection_name}\n")
                continue
            
            # Query the system
            print("\n🤔 Thinking...\n")
            result = rag.query(question, conversation_id=conversation_id)
            
            print(f"Agent: {result['answer']}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()