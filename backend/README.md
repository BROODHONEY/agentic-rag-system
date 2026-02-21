# 🔧 Bibliotheca AI - Backend

FastAPI backend for the Bibliotheca AI document intelligence system.

## 📋 Overview

The backend provides a RESTful API for document ingestion, semantic search, and conversational AI powered by Groq LLMs and vector databases.

## 🏗️ Architecture

### Core Components

- **Agent System** (`src/core/`): Agentic RAG orchestrator using LangChain
- **Vector Store** (`src/vectorstore/`): Unified interface for ChromaDB and Pinecone
- **Document Processing** (`src/processing/`): Loaders and chunkers for various formats
- **Tools** (`src/tools/`): Semantic search and other agent capabilities
- **Memory** (`src/memory/`): Conversation history management

### API Endpoints

- `POST /api/v1/query` - Query the RAG system
- `POST /api/v1/ingest` - Upload and process documents
- `GET /api/v1/stats` - System statistics
- `GET /api/v1/documents` - List all documents with chunks
- `DELETE /api/v1/documents/{source}` - Delete specific document
- `POST /api/v1/reset` - Clear all documents
- `GET /api/v1/search` - Direct vector search
- `GET /health` - Health check

## 🚀 Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env` to `.env.local` and configure:

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# LLM Configuration
DEFAULT_MODEL=llama-3.3-70b-versatile
TEMPERATURE=0
MAX_TOKENS=1024

# Vector Store (choose one)
VECTOR_STORE_TYPE=chroma  # or "pinecone"

# ChromaDB (Local)
CHROMA_PERSIST_DIRECTORY=./data/vectorstore
CHROMA_COLLECTION_NAME=documents

# Pinecone (Cloud) - Optional
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=bibliotheca-ai

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Retrieval
TOP_K_RESULTS=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 4. Start Server

**Option 1: Using PowerShell Script**
```bash
.\start.ps1
```

**Option 2: Direct Command**
```bash
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Using Python**
```bash
python api/main.py
```

## 📦 Dependencies

### Core
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `python-dotenv` - Environment management

### LLM & Agent
- `langchain` - Agent orchestration
- `langchain-groq` - Groq integration
- `langchain-community` - Community integrations

### Vector Stores
- `chromadb` - Local vector database
- `pinecone-client` - Cloud vector database
- `langchain-pinecone` - Pinecone integration

### Embeddings & Processing
- `sentence-transformers` - Text embeddings
- `pypdf` - PDF processing
- `python-docx` - DOCX processing
- `unstructured` - Document parsing

## 🗄️ Vector Store Options

### ChromaDB (Local)

**Pros:**
- Free and open source
- Fast for development
- No external dependencies
- Works offline

**Cons:**
- Limited to local storage
- Not suitable for distributed systems

**Configuration:**
```bash
VECTOR_STORE_TYPE=chroma
CHROMA_PERSIST_DIRECTORY=./data/vectorstore
```

### Pinecone (Cloud)

**Pros:**
- Scalable cloud infrastructure
- Managed service
- High availability
- Accessible from anywhere

**Cons:**
- Requires API key
- Free tier limited to 100K vectors
- Requires internet connection

**Setup:**
1. Sign up at https://app.pinecone.io/
2. Get your API key
3. Configure:
```bash
VECTOR_STORE_TYPE=pinecone
PINECONE_API_KEY=your_key_here
PINECONE_INDEX_NAME=bibliotheca-ai
```

### Switching Between Stores

Use the helper script:
```bash
# Switch to Pinecone
python switch_storage.py pinecone

# Switch to ChromaDB
python switch_storage.py chroma
```

## 🔧 Configuration Details

### LLM Models (Groq)

Available models:
- `llama-3.3-70b-versatile` (Recommended)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

### Embedding Models

Default: `sentence-transformers/all-MiniLM-L6-v2`
- Dimension: 384
- Fast and efficient
- Good for general use

Alternatives:
- `sentence-transformers/all-mpnet-base-v2` (768 dim, more accurate)
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (multilingual)

### Chunking Strategy

- **Chunk Size**: 1000 characters (configurable)
- **Overlap**: 200 characters (configurable)
- **Method**: Recursive character splitting
- Preserves sentence boundaries when possible

## 📊 API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test query
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'
```

### Interactive Testing

Use the provided test scripts:
```bash
python test/interactive_test.py
python test/test_query.py
```

## 📁 Directory Structure

```
backend/
├── api/                    # API layer
│   ├── main.py            # FastAPI app
│   ├── routes.py          # API endpoints
│   └── schemas.py         # Pydantic models
├── config/                # Configuration
│   ├── settings.py        # Settings management
│   └── prompts.yaml       # Agent prompts
├── src/                   # Core application
│   ├── core/              # Agent and LLM
│   │   ├── agent.py       # Agentic RAG
│   │   └── llm.py         # Groq LLM wrapper
│   ├── memory/            # Conversation memory
│   │   └── conversation.py
│   ├── processing/        # Document processing
│   │   ├── loaders.py     # Document loaders
│   │   └── chunkers.py    # Text chunking
│   ├── tools/             # Agent tools
│   │   └── semantic_search.py
│   ├── vectorstore/       # Vector databases
│   │   ├── base_manager.py
│   │   ├── chroma_manager.py
│   │   └── pinecone_manager.py
│   └── utils/             # Utilities
│       ├── logger.py
│       └── exceptions.py
├── data/                  # Data storage
│   ├── raw/              # Uploaded files
│   ├── processed/        # Processed data
│   └── vectorstore/      # ChromaDB storage
├── logs/                 # Application logs
├── scripts/              # Utility scripts
│   └── ingest_documents.py
├── test/                 # Test files
├── .env                  # Environment template
├── .env.local           # Local configuration (gitignored)
├── requirements.txt     # Python dependencies
├── start.ps1           # Startup script
└── README.md           # This file
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
python -m uvicorn api.main:app --reload --port 8001
```

### ChromaDB Permission Error
```bash
# Change persist directory to user folder
CHROMA_PERSIST_DIRECTORY=C:/Users/YourName/Documents/bibliotheca-data
```

### Groq API Rate Limit
- Free tier: 30 requests/minute
- Upgrade at https://console.groq.com

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📝 Logging

Logs are stored in `logs/app.log`

Configure log level:
```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

## 🔒 Security Notes

- Never commit `.env.local` with API keys
- Use environment variables in production
- Enable CORS restrictions for production
- Implement rate limiting for public APIs
- Validate and sanitize file uploads

## 📈 Performance Tips

1. **Use Pinecone for production** - Better scalability
2. **Adjust chunk size** - Smaller chunks = more precise, larger = more context
3. **Tune Top-K** - Higher values = more context, slower responses
4. **Cache embeddings** - Reuse embeddings when possible
5. **Monitor memory** - Large documents can consume significant RAM

## 🔄 Updates

To update dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## 📧 Support

For backend-specific issues, check:
1. Logs in `logs/app.log`
2. API documentation at `/docs`
3. Health endpoint at `/health`

---

**Part of Bibliotheca AI - Intelligent Document Library**
