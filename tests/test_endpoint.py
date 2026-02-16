"""Test the /chat endpoint"""
import requests
import json

url = "http://localhost:8000/chat"
data = {
    "message": "What properties are available?",
    "session_id": "test123"
}

print("Testing /chat endpoint...")
print(f"Request: {json.dumps(data, indent=2)}")
print()

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
