#!/usr/bin/env python3
"""Helper script to switch between vector storage types."""
import os
import sys
from pathlib import Path


def update_env_file(storage_type: str):
    """Update .env.local with the specified storage type."""
    env_file = Path(__file__).parent / ".env.local"
    
    if not env_file.exists():
        print(f"Error: {env_file} not found")
        return False
    
    # Read current content
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update VECTOR_STORE_TYPE line
    updated = False
    for i, line in enumerate(lines):
        if line.startswith('VECTOR_STORE_TYPE='):
            lines[i] = f'VECTOR_STORE_TYPE={storage_type}\n'
            updated = True
            break
    
    # If not found, add it
    if not updated:
        lines.append(f'\nVECTOR_STORE_TYPE={storage_type}\n')
    
    # Write back
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    return True


def main():
    """Main function."""
    if len(sys.argv) != 2 or sys.argv[1] not in ['chroma', 'pinecone']:
        print("Usage: python switch_storage.py [chroma|pinecone]")
        print("\nExamples:")
        print("  python switch_storage.py chroma    # Switch to local ChromaDB")
        print("  python switch_storage.py pinecone  # Switch to cloud Pinecone")
        sys.exit(1)
    
    storage_type = sys.argv[1]
    
    print(f"Switching to {storage_type.upper()} storage...")
    
    if update_env_file(storage_type):
        print(f"✓ Successfully switched to {storage_type.upper()}")
        print("\nNext steps:")
        
        if storage_type == 'pinecone':
            print("1. Make sure PINECONE_API_KEY is set in .env.local")
            print("2. Install dependencies: pip install pinecone-client langchain-pinecone")
            print("3. Restart the backend server")
        else:
            print("1. Optionally update CHROMA_PERSIST_DIRECTORY to a permanent location")
            print("2. Restart the backend server")
        
        print("\nRestart command:")
        print("  python -m uvicorn api.main:app --reload")
    else:
        print("✗ Failed to update configuration")
        sys.exit(1)


if __name__ == "__main__":
    main()
