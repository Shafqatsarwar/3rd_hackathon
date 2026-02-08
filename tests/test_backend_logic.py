
import sys
import os
import asyncio
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from backend.main import chat, ChatRequest


# Force unbuffered output
sys.stdout.reconfigure(encoding='utf-8')

async def run_tests():
    print("Running Backend Logic Tests...", flush=True)
    
    # Test 1: Compound Query
    req1 = ChatRequest(message="What is a list and a dictionary?")
    resp1 = await chat(req1)
    print(f"Test 1 (Compound): Agent={resp1.agent}", flush=True)
    if resp1.agent == "concepts-agent" and "List" in resp1.response and "Dictionary" in resp1.response:
        print("  PASS: Correctly identified multiple concepts.", flush=True)
    else:
        print(f"  FAIL: Expected concepts-agent with list/dict defs. Got: {resp1.response}", flush=True)

    # Test 2: Generic Help
    req2 = ChatRequest(message="I need help learning python")
    resp2 = await chat(req2)
    print(f"Test 2 (Generic): Agent={resp2.agent}", flush=True)
    if resp2.agent == "concepts-agent":
        print("  PASS: Routed to Concepts Agent.", flush=True)
    else:
        print(f"  FAIL: Expected concepts-agent. Got: {resp2.agent}", flush=True)

    # Test 3: Debug Query
    req3 = ChatRequest(message="My code has an error")
    resp3 = await chat(req3)
    print(f"Test 3 (Debug): Agent={resp3.agent}", flush=True)
    if resp3.agent == "debug-agent":
        print("  PASS: Routed to Debug Agent.", flush=True)
    else:
        print(f"  FAIL: Expected debug-agent. Got: {resp3.agent}", flush=True)

if __name__ == "__main__":
    asyncio.run(run_tests())
