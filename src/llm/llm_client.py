"""
Unified LLM client supporting multiple providers (Ollama, SAIA).
Provides a single interface for chat completions across different LLM backends.
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

# Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai | ollama
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
DEFAULT_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1000"))
REQUEST_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "30"))


class LLMError(Exception):
    """Raised when LLM request fails."""
    pass


def chat(
    messages: List[Dict[str, str]], 
    provider: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
) -> str:
    """
    Send chat completion request to configured LLM provider.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
                 Example: [{"role": "system", "content": "..."}, 
                          {"role": "user", "content": "..."}]
        provider: Override provider ('openai' | 'ollama'), uses LLM_PROVIDER if None
        model: Override model name, uses default for provider if None
        temperature: Sampling temperature (0.0-1.0), uses DEFAULT_TEMPERATURE if None
        max_tokens: Max tokens to generate, uses DEFAULT_MAX_TOKENS if None
        
    Returns:
        String response from LLM
        
    Raises:
        LLMError: If request fails or provider is invalid
    """
    provider = provider or LLM_PROVIDER
    temperature = temperature if temperature is not None else DEFAULT_TEMPERATURE
    max_tokens = max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS
    
    if provider == "openai":
        return _chat_openai(messages, model, temperature, max_tokens)
    elif provider == "ollama":
        return _chat_ollama(messages, model, temperature, max_tokens)
    else:
        raise LLMError(f"Unknown LLM provider: {provider}. Use 'openai' or 'ollama'")


def _chat_openai(
    messages: List[Dict[str, str]],
    model: Optional[str],
    temperature: float,
    max_tokens: int
) -> str:
    """
    Call OpenAI API.
    """
    if not OPENAI_API_KEY:
        raise LLMError("OPENAI_API_KEY not configured in environment")
    
    model = model or OPENAI_MODEL
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        print(f"[OPENAI] Calling {OPENAI_URL} with model {model}")
        response = requests.post(
            OPENAI_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Extract content from OpenAI response
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            return content.strip()
        else:
            raise LLMError(f"Unexpected OpenAI response format: {data}")
            
    except requests.Timeout:
        raise LLMError(f"OpenAI request timed out after {REQUEST_TIMEOUT} seconds")
    except requests.RequestException as e:
        raise LLMError(f"OpenAI request failed: {str(e)}")
    except Exception as e:
        raise LLMError(f"OpenAI processing error: {str(e)}")


def _chat_ollama(
    messages: List[Dict[str, str]],
    model: Optional[str],
    temperature: float,
    max_tokens: int
) -> str:
    """
    Call Ollama API.
    """
    model = model or OLLAMA_MODEL
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }
    
    try:
        print(f"[OLLAMA] Calling {OLLAMA_URL} with model {model}")
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        
        # Check for model not found error
        if response.status_code == 404:
            raise LLMError(f"Model '{model}' not found in Ollama. Run: ollama pull {model}")
        
        response.raise_for_status()
        
        data = response.json()
        
        # Extract content from Ollama response
        if "message" in data and "content" in data["message"]:
            content = data["message"]["content"]
            return content.strip()
        else:
            raise LLMError(f"Unexpected Ollama response format: {data}")
            
    except requests.Timeout:
        raise LLMError(f"Ollama request timed out after {REQUEST_TIMEOUT} seconds")
    except requests.RequestException as e:
        raise LLMError(f"Ollama request failed: {str(e)}")
    except Exception as e:
        raise LLMError(f"Ollama processing error: {str(e)}")


def test_connection(provider: Optional[str] = None) -> bool:
    """
    Test if LLM provider is reachable.
    
    Args:
        provider: Provider to test ('ollama' | 'saia'), uses LLM_PROVIDER if None
        
    Returns:
        True if provider is working, False otherwise
    """
    provider = provider or LLM_PROVIDER
    
    try:
        if provider == "openai":
            # Test OpenAI with a minimal request
            if not OPENAI_API_KEY:
                return False
            test_messages = [{"role": "user", "content": "test"}]
            chat(test_messages, provider="openai", max_tokens=5)
            return True
        elif provider == "ollama":
            # Test Ollama
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        else:
            return False
    except Exception as e:
        print(f"[LLM] Connection test failed for {provider}: {e}")
        return False
