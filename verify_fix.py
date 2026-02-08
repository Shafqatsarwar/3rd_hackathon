import requests
import sys

def log(msg):
    with open("verify_output.txt", "a") as f:
        f.write(msg + "\n")

def test_backend():
    log("Testing Backend...")
    base_url = "http://localhost:8000"
    
    # 1. Test Health
    try:
        resp = requests.get(f"{base_url}/health", timeout=5)
        if resp.status_code == 200:
            log("[PASS] Health check passed")
        else:
            log(f"[FAIL] Health check failed: {resp.status_code}")
    except Exception as e:
        log(f"[FAIL] Backend not reachable: {e}")
        return

    # 2. Test GET Endpoint (User Request)
    try:
        resp = requests.get(f"{base_url}/api/chat", params={"message": "what is python"}, timeout=10)
        if resp.status_code == 200:
            log(f"[PASS] GET /api/chat works. Response: {resp.json().get('response')[:50]}...")
        else:
            log(f"[FAIL] GET /api/chat failed: {resp.status_code} {resp.text}")
    except Exception as e:
        log(f"[FAIL] GET /api/chat exception: {e}")

    # 3. Test POST Compound Query (User Request)
    try:
        payload = {"message": "explain list and dictionary"}
        resp = requests.post(f"{base_url}/api/chat", json=payload, timeout=10)
        response_text = resp.json().get('response', '').lower()
        if "list" in response_text and "dictionary" in response_text:
            log("[PASS] POST /api/chat compound query works (found 'list' and 'dictionary').")
        else:
            log(f"[FAIL] POST /api/chat compound query missing content. Response: {response_text[:100]}...")
    except Exception as e:
        log(f"[FAIL] POST /api/chat exception: {e}")

if __name__ == "__main__":
    test_backend()

if __name__ == "__main__":
    test_backend()
