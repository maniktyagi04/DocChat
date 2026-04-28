# Vercel Deployment Guide

## Quick Deploy to Vercel

### Important: You Need Two API Keys

1. **Groq API Key** (for the LLM): You already have this
2. **OpenAI API Key** (for embeddings): Get one at https://platform.openai.com/api-keys

The lightweight version uses OpenAI embeddings instead of heavy local models to fit within Vercel's limits.

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel**: Visit https://vercel.com/
2. **Sign in** with your GitHub account
3. **Import Project**: Click "Add New" → "Project"
4. **Select Repository**: Choose `maniktyagi04/DocChat`
5. **Configure Project**:
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: Leave empty
   - Output Directory: Leave empty
6. **Add Environment Variables** (BOTH REQUIRED):
   - Variable 1:
     - Key: `GROQ_API_KEY`
     - Value: Your Groq API key
   - Variable 2:
     - Key: `OPENAI_API_KEY`
     - Value: Your OpenAI API key (get from https://platform.openai.com/api-keys)
7. **Click Deploy**

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

When prompted, add the environment variable:
- `GROQ_API_KEY=your_groq_api_key_here`

## Important Notes

⚠️ **Vercel Limitations:**
- Vercel has a 250MB deployment size limit
- Some Python packages (like sentence-transformers) are very large
- The deployment might fail due to package size

## Alternative: Deploy Backend Separately

If Vercel deployment fails due to size limits, consider:

1. **Deploy Backend on Railway/Render** (supports larger Python apps)
2. **Deploy Frontend on Vercel** (just the HTML/JS)
3. **Update frontend to point to backend API**

## Troubleshooting

If deployment fails:
1. Check Vercel deployment logs
2. Verify all environment variables are set
3. Check package sizes in requirements.txt
4. Consider using lighter alternatives for embeddings

## Expected Deployment URL

After successful deployment, you'll get a URL like:
- `https://doc-chat-[random].vercel.app`

## Testing the Deployment

1. Visit your Vercel URL
2. Upload a PDF file
3. Ask questions about the document
4. Verify responses are working correctly
