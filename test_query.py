"""Test the complete RAG system."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.agent import create_agentic_rag

def main():
    print("\n" + "="*60)
    print("🤖 Agentic RAG System Test")
    print("="*60)
    
    # Initialize the system
    print("\n📦 Initializing system...")
    rag = create_agentic_rag()
    print("✅ System initialized!")
    
    # Test queries
    test_questions = [
        "What is machine learning?",
        "What is RAG?",
        "Tell me about vector databases",
        "What are Large Language Models?"
    ]
    
    print("\n" + "="*60)
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}/{len(test_questions)}")
        print(f"Question: {question}")
        print("-" * 60)
        
        try:
            result = rag.query(question, conversation_id="test-session")
            
            print(f"\n💡 Answer:")
            print(f"{result['answer']}")
            print(f"\n📊 Metadata: {result['metadata']}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        print("\n" + "="*60)
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()