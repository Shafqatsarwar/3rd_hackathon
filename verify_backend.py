import requests
import json

try:
    url = "http://localhost:8000/api/chat"
    payload = {"message": "explain list dictionary tuple set"}
    print(f"Sending request to {url} with payload: {payload}")
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response Content:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
