# Model Selection Feature

## Overview
Users can now select which LLM model to use for query planning and answer generation directly from the frontend interface.

## Available Models

### Ollama (Local)
- **Llama 3.2** - Default local model
- **Llama 3.1** - Alternative local model
- **Mistral** - Lightweight local model

### SAIA (Cloud)
- **GPT-4** - Most capable model (requires SAIA_API_KEY)
- **GPT-3.5 Turbo** - Faster model (requires SAIA_API_KEY)

## How It Works

### Frontend
1. **Model Selector Dropdown** in the header
   - Loads available models from `/models` endpoint
   - Saves selection to localStorage
   - Persists across page reloads

2. **Model Format**: `provider:model_name`
   - Example: `ollama:llama3.2`
   - Example: `saia:gpt-4`

### Backend

#### New Endpoint: `/models`
Returns list of available models with their display names and providers.

```json
{
  "models": [
    {
      "id": "ollama:llama3.2",
      "name": "Llama 3.2 (Local)",
      "provider": "ollama"
    },
    {
      "id": "saia:gpt-4",
      "name": "GPT-4 (SAIA)",
      "provider": "saia"
    }
  ],
  "default": "ollama:llama3.2"
}
```

#### Updated Chat Endpoint
- Accepts `model` parameter in ChatRequest
- Parses format: `provider:model_name`
- Passes to agent's `plan_query()` and `explain_results()`

#### Agent Updates
- `plan_query()` - accepts `model` parameter
- `plan_query_with_llm()` - accepts `model` parameter
- `explain_results()` - accepts `model` parameter
- All methods parse model string and pass `provider` and `model_name` to `llm_client.chat()`

## Usage

1. **Open the chat interface** at http://localhost:8000/static/index.html
2. **Select a model** from the dropdown in the header
3. **Ask questions** - the selected model will be used for:
   - Query planning (if RAG is enabled)
   - Answer generation

## Configuration

### Environment Variables
```bash
# Default provider and model (if user doesn't select)
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2

# SAIA configuration (optional)
SAIA_API_KEY=your_api_key_here
SAIA_MODEL=gpt-4
```

### Adding New Models

#### Backend (`main.py` - `/models` endpoint):
```python
models.append({
    "id": "ollama:codellama",
    "name": "Code Llama (Local)",
    "provider": "ollama"
})
```

#### Frontend:
Models are loaded automatically from the API.

## Benefits

1. **Flexibility** - Users choose the right model for their needs
2. **Cost Control** - Use local models for simple queries, cloud models for complex ones
3. **Performance** - Select faster models when speed matters
4. **Privacy** - Keep sensitive queries on local models

## Technical Details

### Model Parameter Flow
```
Frontend Dropdown Selection
    ↓
localStorage (persists choice)
    ↓
POST /chat { model: "ollama:llama3.2" }
    ↓
ChatRequest.model
    ↓
agent.plan_query(model=...)
agent.explain_results(model=...)
    ↓
Parse: provider="ollama", model_name="llama3.2"
    ↓
llm_client.chat(provider=..., model=...)
    ↓
_chat_ollama() or _chat_saia()
```

### Error Handling
- If model not specified, uses default from .env
- If model API fails, falls back to context-only response
- If model selector fails to load, shows error message

## Testing

1. **Test model switching**:
   ```javascript
   // In browser console
   localStorage.setItem('selectedModel', 'ollama:mistral');
   location.reload();
   ```

2. **Test different models**:
   - Ask same question with different models
   - Compare response quality and speed

3. **Test fallback**:
   - Select non-existent model
   - Verify system falls back to default
