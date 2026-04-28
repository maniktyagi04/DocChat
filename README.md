# RAG Application

A simple **Retrieval-Augmented Generation (RAG)** app built with **LangChain**, **FastAPI**, and plain **HTML/JS**.

Upload a PDF or text document, then ask questions — the app retrieves relevant chunks and uses an LLM to answer.

## 🚀 Live Deployment

**Frontend:** https://doc-chat-pearl.vercel.app/  
**Backend API:** https://docchat-backend-4pwm.onrender.com  
**Health Check:** https://docchat-backend-4pwm.onrender.com/health

---

## Architecture

```
┌──────────┐       ┌──────────────┐       ┌────────────┐
│  Browser  │──────▶│   FastAPI     │──────▶│  LangChain │
│  (HTML)   │◀──────│   Backend     │◀──────│  + FAISS   │
└──────────┘       └──────────────┘       └────────────┘
                          │                       │
                     Upload doc              OpenAI API
                     /query                 (embeddings + chat)
```

### How RAG Works (simplified)

1. **Upload** — The document is split into small overlapping chunks.
2. **Embed** — Each chunk is converted to a vector using OpenAI Embeddings.
3. **Store** — Vectors are stored in an in-memory FAISS index.
4. **Query** — The user's question is embedded, the top-k similar chunks are retrieved, and passed as context to the LLM which generates an answer.

---

## Setup

### Prerequisites
- Python 3.8 or higher
- Groq API key (get one at https://console.groq.com/)

### 1. Clone / copy the project

```
RAG/
├── main.py              # FastAPI backend
├── static/
│   └── index.html       # Frontend
├── requirements.txt
├── .env.example
└── README.md
```

### 2. Create a virtual environment

```bash
cd RAG
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Groq API key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 5. Run the app

```bash
uvicorn main:app --reload
```

**Local development:** Open **http://127.0.0.1:8000** in your browser.

**Live deployment:** Visit **https://doc-chat-pearl.vercel.app/**

---

## Usage

1. Click **Upload** and select a `.pdf` or `.txt` file.
2. Type a question in the text box and click **Ask**.
3. The answer and source chunks will appear below.

---

## Key Concepts for Students

| Concept | Where in code |
|---|---|
| Document loading | `load_document()` — uses LangChain's `PyPDFLoader` / `TextLoader` |
| Text chunking | `build_vector_store()` — `RecursiveCharacterTextSplitter` |
| Embeddings | `OpenAIEmbeddings()` converts text → vectors |
| Vector store | `FAISS.from_documents()` — similarity search index |
| Retrieval chain | `RetrievalQA.from_chain_type()` — retrieves context + generates answer |
| API endpoint | FastAPI `@app.post("/query")` |

---

## Notes

- This uses **in-memory** FAISS — data is lost on restart.
- Uses Groq's `llama-3.3-70b-versatile` model for fast inference.
- HuggingFace embeddings run locally (no API key needed).
- For production, add authentication, persistent storage, and rate limiting.

## API Endpoints

- `GET /` - Main application interface
- `POST /upload` - Upload and index a document
- `POST /query` - Query the indexed document
- `GET /health` - Health check endpoint
