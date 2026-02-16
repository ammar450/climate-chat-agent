"""Test SAIA LLM provider integration."""
import os
os.environ["LLM_BACKEND"] = "saia"  # Force SAIA backend

from llm_provider import get_llm, chat

print("=" * 60)
print("Testing SAIA LLM Provider")
print("=" * 60)

# Test 1: Get LLM instance
print("\n[TEST 1] Getting LLM instance...")
try:
    llm = get_llm()
    print("✅ LLM instance created successfully")
except Exception as e:
    print(f"❌ Failed to create LLM instance: {e}")
    exit(1)

# Test 2: Simple chat
print("\n[TEST 2] Testing simple chat...")
try:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say 'Hello from SAIA!' and nothing else."}
    ]
    response = chat(messages)
    print(f"✅ Response: {response}")
except Exception as e:
    print(f"❌ Chat failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 3: JSON generation (like planning)
print("\n[TEST 3] Testing JSON generation...")
try:
    messages = [
        {"role": "system", "content": "You must respond with valid JSON only."},
        {"role": "user", "content": 'Generate JSON: {"status": "ok", "message": "SAIA working"}'}
    ]
    response = chat(messages)
    print(f"✅ Response: {response}")
    
    import json
    data = json.loads(response.strip().replace("```json", "").replace("```", ""))
    print(f"✅ Parsed JSON: {data}")
except Exception as e:
    print(f"❌ JSON generation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("SAIA Integration Test Complete!")
print("=" * 60)
