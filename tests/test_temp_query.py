"""Test the /chat endpoint with temperature query"""
import requests
import json

url = "http://localhost:8000/chat"
data = {
    "message": "Show me temperature data from 2020",
    "session_id": "test123"
}

print("Testing /chat endpoint with temperature query...")
print(f"Request: {json.dumps(data, indent=2)}")
print()

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Answer: {result.get('answer', 'No answer')[:200]}...")
    print(f"Template: {result.get('used_template')}")
    print(f"Rows: {len(result.get('rows', []))} rows returned")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
