# DocChat — REST API Reference

**Frontend URL:** `https://doc-chat-pearl.vercel.app/`  
**Backend API Base URL:** `https://docchat-backend-4pwm.onrender.com`

---

## `GET /`

Serves the frontend single-page application.

**Response:** `200 OK` — HTML page

---

## `POST /upload`

Upload and index a PDF or TXT document. The document is split into chunks, embedded with `sentence-transformers/all-MiniLM-L6-v2`, and stored in a FAISS in-memory vector store.

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | ✅ | `.pdf` or `.txt` file to index |

**Success Response — `200 OK`:**
```json
{
  "message": "'filename.pdf' uploaded and indexed successfully.",
  "pages": 21
}
```

**Error Responses:**

| Status | Reason |
|--------|--------|
| `400` | No file provided |
| `400` | Unsupported file type |
| `500` | Error during document processing |

---

## `POST /query`

Ask a natural-language question against the currently indexed document.

**Request:** `application/json`

```json
{ "question": "What is this document about?" }
```

**Success Response — `200 OK`:**
```json
{
  "answer": "This document discusses game theory...",
  "sources": [
    {
      "content": "First 300 chars of retrieved chunk...",
      "metadata": { "source": "uploads/file.pdf", "page": 0 }
    }
  ]
}
```

**Error Responses:**

| Status | Reason |
|--------|--------|
| `400` | No document uploaded yet |

---

## Notes

- Only **one document** is active at a time. Uploading a new file replaces the previous index.
- Sources return the top **3 most relevant chunks** by cosine similarity.
- The LLM used is **Groq LLaMA 3.3-70b-versatile** (`temperature=0`).
