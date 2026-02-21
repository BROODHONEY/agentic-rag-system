# 📚 Bibliotheca AI

> An intelligent document library powered by Agentic RAG (Retrieval-Augmented Generation)

Bibliotheca AI is a sophisticated document management and question-answering system that combines the power of vector databases, large language models, and an elegant library-themed interface. Upload your documents and have intelligent conversations with your knowledge base.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Node](https://img.shields.io/badge/node-18+-green.svg)

## ✨ Features

### 🤖 Intelligent Agent System
- **Agentic RAG Architecture**: Autonomous agent that decides when to search your knowledge base
- **Semantic Search**: Vector-based similarity search using embeddings
- **Conversation Memory**: Maintains context across multiple queries
- **Tool-Based Reasoning**: ReAct pattern for transparent decision-making

### 📖 Document Management
- **Multi-Format Support**: PDF, DOCX, TXT files
- **Smart Chunking**: Intelligent document splitting with overlap
- **Embedding Visualization**: View all documents, chunks, and embeddings
- **Individual Document Control**: Delete specific documents or clear entire database

### 🎨 Library-Themed Interface
- **Parchment & Leather Design**: Beautiful vintage aesthetic
- **Real-Time Updates**: Auto-refresh after document uploads
- **System Monitoring**: Live stats showing database type, model, and configuration
- **Responsive Layout**: Works on desktop and tablet devices

### ☁️ Flexible Storage
- **Local Storage**: ChromaDB for development and testing
- **Cloud Storage**: Pinecone integration for production deployments
- **Easy Switching**: Toggle between storage types via configuration

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                      │
│  Library-themed UI • Document Upload • Chat Interface       │
└─────────────────────┬───────────────────────────────────────┘
                      │ REST API
┌─────────────────────▼───────────────────────────────────────┐
│                   Backend (FastAPI)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Agentic    │  │   Document   │  │    Vector    │     │
│  │   RAG Agent  │──│  Processing  │──│    Store     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐   ┌────▼────┐   ┌───▼────┐
   │  Groq   │   │ ChromaDB│   │Pinecone│
   │   LLM   │   │ (Local) │   │(Cloud) │
   └─────────┘   └─────────┘   └────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API Key ([Get one free](https://console.groq.com))
- (Optional) Pinecone API Key for cloud storage

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bibliotheca-ai.git
   cd bibliotheca-ai
   ```

2. **Set up Backend**
   ```bash
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows
   # source .venv/bin/activate    # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   # Copy and edit .env.local
   cp .env .env.local
   # Add your Groq API key
   ```

4. **Set up Frontend**
   ```bash
   cd ../frontend
   npm install
   ```

5. **Start the Application**
   
   Terminal 1 (Backend):
   ```bash
   cd backend
   .\start.ps1  # or: python -m uvicorn api.main:app --reload
   ```
   
   Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm run dev
   ```

6. **Open your browser**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

## 📖 Usage

### Upload Documents
1. Click the upload area or drag & drop files
2. Supported formats: PDF, DOCX, TXT
3. Documents are automatically chunked and embedded

### Ask Questions
1. Type your question in the chat interface
2. The agent will search your knowledge base
3. Receive contextual answers with sources

### Manage Documents
1. View all uploaded documents in the sidebar
2. Expand to see individual chunks and embeddings
3. Delete specific documents or clear all

### Monitor System
- View database type (ChromaDB/Pinecone)
- Check embedding model and configuration
- Monitor document count and agent settings

## ⚙️ Configuration

### Vector Storage Options

**Local Storage (ChromaDB)**
```bash
VECTOR_STORE_TYPE=chroma
CHROMA_PERSIST_DIRECTORY=./data/vectorstore
```

**Cloud Storage (Pinecone)**
```bash
VECTOR_STORE_TYPE=pinecone
PINECONE_API_KEY=your_api_key_here
PINECONE_INDEX_NAME=bibliotheca-ai
```

### LLM Configuration
```bash
DEFAULT_MODEL=llama-3.3-70b-versatile
TEMPERATURE=0
MAX_TOKENS=1024
TOP_K_RESULTS=5
```

See `backend/README.md` and `frontend/README.md` for detailed configuration options.

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **LangChain**: LLM orchestration and agent framework
- **Groq**: Ultra-fast LLM inference
- **ChromaDB**: Local vector database
- **Pinecone**: Cloud vector database
- **Sentence Transformers**: Text embeddings

### Frontend
- **Next.js 16**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Lucide Icons**: Beautiful icon library
- **React Markdown**: Markdown rendering

## 📁 Project Structure

```
bibliotheca-ai/
├── backend/              # FastAPI backend
│   ├── api/             # API routes and schemas
│   ├── config/          # Configuration and prompts
│   ├── src/             # Core application logic
│   │   ├── core/        # Agent and LLM
│   │   ├── memory/      # Conversation memory
│   │   ├── processing/  # Document loaders and chunkers
│   │   ├── tools/       # Agent tools
│   │   ├── vectorstore/ # Vector database managers
│   │   └── utils/       # Utilities and logging
│   └── data/            # Data storage
├── frontend/            # Next.js frontend
│   └── src/
│       ├── app/         # Next.js app router
│       ├── components/  # React components
│       ├── lib/         # API client
│       └── types/       # TypeScript types
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for blazing-fast LLM inference
- [LangChain](https://langchain.com) for the agent framework
- [ChromaDB](https://www.trychroma.com/) for local vector storage
- [Pinecone](https://www.pinecone.io/) for cloud vector storage
- [Vercel](https://vercel.com) for Next.js and deployment platform

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Agentic RAG architecture**
