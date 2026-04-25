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

app = FastAPI(title="RAG Application")

app.mount("/static", StaticFiles(directory="static"), name="static")


# --------------- state ---------------
UPLOAD_DIR = Path("/tmp/uploads") if os.environ.get("VERCEL") else Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

vector_store = None  # will hold the FAISS index after upload


# --------------- helpers ---------------

def load_document(file_path: str):
    """Load a PDF or text file and return LangChain Documents."""
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Only .pdf and .txt files are supported.")
    return loader.load()


def build_vector_store(documents):
    """Split documents into chunks and build a FAISS vector store."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(chunks, embeddings)


def get_qa_chain(store):
    """Create a RetrievalQA chain from the vector store."""
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    chain_type = "stuff"
    retriever = store.as_retriever(search_kwargs={"k": 3})
    return_source_documents = True
    return RetrievalQA.from_chain_type(llm=llm, chain_type=chain_type, return_source_documents=return_source_documents, retriever=retriever)

