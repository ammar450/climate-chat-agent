"""
SAIA Integration Setup Guide
=============================

⚠️ SECURITY FIRST
-----------------
1. REVOKE the OpenAI key that was exposed immediately
2. SAIA requires its own API key from Academic Cloud (https://chat-ai.academiccloud.de/)
3. OpenAI keys DO NOT work with SAIA endpoints
4. NEVER commit API keys to git or share them in chat

SAIA Configuration Steps
-------------------------

1. Get SAIA API Key from Academic Cloud:
   - Go to https://chat-ai.academiccloud.de/
   - Sign up / log in to Academic Cloud
   - Navigate to API Keys section
   - Generate a new API key for SAIA

2. Configure .env file:
   
   LLM_BACKEND=saia
   SAIA_BASE_URL=https://chat-ai.academiccloud.de/v1
   SAIA_API_KEY=your-actual-saia-key-here
   SAIA_MODEL=codestral-22b

3. Test SAIA connection (bash):
   
   export SAIA_API_KEY="your-saia-key"
   export SAIA_BASE_URL="https://chat-ai.academiccloud.de/v1"
   export SAIA_MODEL="codestral-22b"
   
   curl -sS "$SAIA_BASE_URL/chat/completions" \
     -H "Authorization: Bearer $SAIA_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "'"$SAIA_MODEL"'",
       "messages": [
         {"role":"system","content":"You are a helpful assistant."},
         {"role":"user","content":"Say OK and nothing else."}
       ],
       "temperature": 0
     }'

4. Test SAIA connection (PowerShell):
   
   $env:SAIA_API_KEY="your-saia-key"
   $env:SAIA_BASE_URL="https://chat-ai.academiccloud.de/v1"
   $env:SAIA_MODEL="codestral-22b"
   
   $body = @{
       model = $env:SAIA_MODEL
       messages = @(
           @{role="system"; content="You are a helpful assistant."}
           @{role="user"; content="Say OK and nothing else."}
       )
       temperature = 0
   } | ConvertTo-Json -Depth 3
   
   Invoke-RestMethod -Uri "$env:SAIA_BASE_URL/chat/completions" `
     -Method Post `
     -Headers @{"Authorization"="Bearer $env:SAIA_API_KEY"} `
     -ContentType "application/json" `
     -Body $body

Expected Response:
------------------
✅ Success (200):
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "OK"
      }
    }
  ]
}

❌ 401 Unauthorized:
- Key is not a valid SAIA key (get one from Academic Cloud)
- Key is expired or revoked
- Using OpenAI key instead of SAIA key

❌ 404 Not Found:
- Wrong base URL or model name
- Check SAIA_BASE_URL and SAIA_MODEL

Switching Backends
------------------

Switch to SAIA:
  python switch_backend.py saia

Switch to Ollama (local):
  python switch_backend.py ollama

Then restart server:
  uvicorn main:app --reload

Testing the Integration
------------------------

1. Test health endpoint:
   curl http://localhost:8000/health

2. Test with simple query:
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"What variables are available?","session_id":"test"}'

3. Check logs for:
   [LLM PROVIDER] Backend: SAIA (OpenAI-compatible)
   [LLM PROVIDER] Model: codestral-22b
   [LLM PROVIDER] Base URL: https://chat-ai.academiccloud.de/v1

Troubleshooting
---------------

Error: 401 Unauthorized
→ Your SAIA_API_KEY is not valid for Academic Cloud
→ Get a proper SAIA key from https://chat-ai.academiccloud.de/

Error: "langchain-openai required"
→ pip install langchain-openai

Error: Ollama works but SAIA doesn't
→ Check SAIA_API_KEY is from Academic Cloud, not OpenAI
→ Verify SAIA_BASE_URL is correct
→ Test with curl command above first

LangGraph Integration
---------------------

The LangGraph workflow automatically uses the configured backend.
No changes needed to graph_agent.py - just set LLM_BACKEND in .env.

Backend is loaded once at module initialization:
- graph_agent.py imports llm_provider
- llm_provider reads LLM_BACKEND from .env
- Returns either ChatOllama or ChatOpenAI instance
- All nodes use the same LLM instance

Security Best Practices
-----------------------

✅ DO:
- Store keys in .env file (never commit to git)
- Add .env to .gitignore
- Use environment variables in production
- Rotate keys regularly
- Use secrets manager in cloud deployments

❌ DON'T:
- Commit API keys to git
- Share keys in chat/screenshots
- Use OpenAI keys for SAIA
- Hardcode keys in source code
- Expose keys in error messages

Questions?
----------

If still getting 401:
1. Verify you have a SAIA API key (not OpenAI)
2. Test with curl command first
3. Check .env file has correct SAIA_API_KEY
4. Restart server after changing .env

If integration doesn't work:
1. Check llm_provider.py logs on startup
2. Run: python -c "from llm_provider import get_llm; get_llm()"
3. Share error message (WITHOUT the API key)
