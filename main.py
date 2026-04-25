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


