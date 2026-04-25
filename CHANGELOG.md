# Changelog

All notable changes to **DocChat** are documented here.

## [1.0.0] — 2026-04-25

### Added
- FastAPI backend with `/upload` and `/query` REST endpoints
- LangChain RAG pipeline using HuggingFace `all-MiniLM-L6-v2` embeddings
- FAISS vector store for semantic document retrieval
- Groq LLaMA 3.3-70b-versatile LLM integration
- Support for `.pdf` and `.txt` document ingestion
- Source citation in every query response (page number + excerpt)
- React 18 + Tailwind CSS frontend (CDN, no build step)
- ChatGPT-style chat bubble interface with typing indicator
- Drag-and-drop PDF upload zone with live file-state feedback
- Smooth chatbot reveal animation after successful upload
- Professional SVG arrow annotation guiding users to upload
- Fully responsive, single-page design inspired by ChatPDF
- `uploads/` directory auto-created on server start
