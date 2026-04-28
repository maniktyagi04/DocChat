import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

load_dotenv()

app = FastAPI(
    title="RAG Application",
    description="A document Q&A system powered by RAG",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# --------------- Configuration ---------------
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 3
MODEL_NAME = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# --------------- state ---------------
UPLOAD_DIR = Path("/tmp/uploads") if os.environ.get("VERCEL") else Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

vector_store = None  # will hold the FAISS index after upload


# --------------- helpers ---------------

def load_document(file_path: str):
    """
    Load a PDF or text file and return LangChain Documents.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        List of LangChain Document objects
        
    Raises:
        ValueError: If file type is not supported
    """
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Only .pdf and .txt files are supported.")
    return loader.load()


def build_vector_store(documents):
    """
    Split documents into chunks and build a FAISS vector store.
    
    Args:
        documents: List of LangChain Document objects
        
    Returns:
        FAISS vector store with embedded document chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.from_documents(chunks, embeddings)


def get_qa_chain(store):
    """
    Create a RetrievalQA chain from the vector store.
    
    Args:
        store: FAISS vector store containing document embeddings
        
    Returns:
        RetrievalQA chain configured with Groq LLM
    """
    llm = ChatGroq(model=MODEL_NAME, temperature=0)
    chain_type = "stuff"
    retriever = store.as_retriever(search_kwargs={"k": RETRIEVAL_K})
    return_source_documents = True
    return RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type=chain_type, 
        return_source_documents=return_source_documents, 
        retriever=retriever
    )

# --------------- routes ---------------

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main application HTML page."""
    return HTMLResponse(Path("static/index.html").read_text())


@app.get("/favicon.ico")
async def favicon():
    """Handle favicon requests to prevent 404 errors."""
    return {"message": "No favicon"}


class QueryRequest(BaseModel):
    question: str


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and index a document for Q&A.
    
    Args:
        file: PDF or TXT file to process
        
    Returns:
        Success message with document metadata
        
    Raises:
        HTTPException: If file is invalid or processing fails
    """
    global vector_store
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    ext = Path(file.filename).suffix.lower()
    if ext not in [".pdf", ".txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only .pdf and .txt allowed.")
    safe_name = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_name
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    try:
        documents = load_document(str(file_path))
        vector_store = build_vector_store(documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    return {"message": f"'{safe_name}' uploaded and indexed successfully.", "pages": len(documents)}


@app.post("/query")
async def query_document(req: QueryRequest):
    """
    Query the uploaded document with a question.
    
    Args:
        req: QueryRequest containing the user's question
        
    Returns:
        Answer from the LLM with source document citations
        
    Raises:
        HTTPException: If no document has been uploaded
    """
    if vector_store is None:
        raise HTTPException(status_code=400, detail="No document uploaded yet. Please upload a document first.")
    chain = get_qa_chain(vector_store)
    result = chain.invoke({"query": req.question})
    sources = []
    for doc in result.get("source_documents", []):
        sources.append({
            "content": doc.page_content[:300],
            "metadata": doc.metadata
        })
    return {"answer": result["result"], "sources": sources}
