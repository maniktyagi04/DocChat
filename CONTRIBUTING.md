# Contributing to DocChat

Thank you for your interest in contributing! Here's how to get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/<your-username>/DocChat.git`
3. Create a feature branch: `git checkout -b feat/your-feature-name`
4. Make your changes
5. Test thoroughly (see below)
6. Submit a pull request

## Development Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # add your GROQ_API_KEY
uvicorn main:app --reload
```

**For local development:** Open http://localhost:8000 in your browser.

**Live deployment:** Visit https://doc-chat-pearl.vercel.app/

## Code Guidelines

- **Backend**: Follow PEP 8. Add docstrings to all new functions.
- **Frontend**: Keep changes inside `static/index.html`. No build step required.
- **Commits**: Use conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`).

## Testing

Before submitting a PR, manually verify:

1. Upload a `.pdf` file → should return a success message.
2. Ask a question → should return an answer with source citations.
3. Upload a `.txt` file → same flow should work.
4. Upload an invalid file type → should display an error message.

## Issues

Please use the GitHub issue templates provided for bug reports and feature requests.
