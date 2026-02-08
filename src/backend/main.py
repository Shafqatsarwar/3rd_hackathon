"""
LearnFlow Backend API
AI-Powered Python Tutoring Platform
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="LearnFlow API",
    description="AI-Powered Python Tutoring Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    context: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    agent: str

class HealthResponse(BaseModel):
    status: str
    version: str
    services: dict


# Mock Knowledge Base
KNOWLEDGE_BASE = {
    "python": "Python is a high-level, interpreted programming language known for its easy readability and vast ecosystem of libraries.",
    "list": "A list in Python is a mutable, ordered sequence of elements. You can create one using square brackets: `my_list = [1, 2, 3]`.",
    "tuple": "A tuple is an immutable, ordered sequence. Once created, it cannot be changed. Usage: `my_tuple = (1, 2)`.",
    "dictionary": "A dictionary is a collection of key-value pairs. It's mutable and unordered (pre-3.7). Usage: `my_dict = {'key': 'value'}`.",
    "dict": "A dictionary (dict) is a collection of key-value pairs. Usage: `data = {'name': 'Alice', 'age': 30}`.",
    "set": "A set is an unordered collection of unique elements. Usage: `my_set = {1, 2, 3}`.",
    "function": "A function is a block of code which only runs when it is called. You define it using the `def` keyword.",
    "loop": "Loops allow you to repeat code. Python has `for` loops (for iterating over sequences) and `while` loops.",
    "pandas": "Pandas is a powerful library for data manipulation and analysis. It provides the DataFrame structure for tabular data.",
    "numpy": "NumPy is the fundamental package for scientific computing in Python, providing support for large, multi-dimensional arrays and matrices.",
    "tabular": "Tabular data is data that is structured into rows and columns, like a spreadsheet. In Python, the **Pandas** library is the standard tool for working with tabular data using DataFrames.",
    "dataframe": "A DataFrame is a 2-dimensional labeled data structure with columns of potentially different types, similar to a spreadsheet. It is the primary object in Pandas.",
    "matplotlib": "Matplotlib is a plotting library for creating static, animated, and interactive visualizations in Python.",
    "variable": "A variable is a container for storing data values. In Python, you don't need to declare its type explicitly.",
    "class": "A class is a blueprint for creating objects. It defines a set of attributes and methods that characterize any object of the class.",
    "object": "An object is an instance of a class. It has state (attributes) and behavior (methods).",
    "pip": "pip is the package installer for Python. You can use it to install libraries from the Python Package Index (PyPI).",
    "venv": "venv is a module to create lightweight 'virtual environments' with their own site directories, isolated from system site-directories.",
}

# Routes
@app.get("/")
async def root():
    return {"message": "LearnFlow API - AI Python Tutor", "version": "1.0.0"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        services={
            "api": "running",
            "openai": "configured" if os.getenv("OPENAI_API_KEY") else "not configured",
            "database": "configured" if os.getenv("DATABASE_URL") else "not configured"
        }
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the AI tutor.
    Routes to appropriate agent based on query.
    """
    message = request.message.lower()
    
    # Simple routing logic (Triage Agent simulation)
    # Knowledge Base Lookup
    matches = []
    # Check for specific definitions in KNOWLEDGE_BASE
    for key, answer in KNOWLEDGE_BASE.items():
        # strict word boundary check could be better, but simple inclusion is okay for mock
        if key in message:
            matches.append(f"- **{key.title()}**: {answer}")
    
    if matches:
        agent = "concepts-agent"
        intro = "I found multiple concepts in your query:" if len(matches) > 1 else "Here is the definition you asked for:"
        response = f"[Concepts Agent] {intro}\n\n" + "\n".join(matches)
        return ChatResponse(response=response, agent=agent)

    # Enhanced routing logic
    if any(phrase in message for phrase in ["explain", "what is", "how does", "what about", "tell me", "show me", "help me", "learn", "data structure"]):
        agent = "concepts-agent"
        response = f"[Concepts Agent] Great question! Here's an explanation about Python concepts related to your query: '{request.message}'.\n\n(Note: Connect an LLM backend to get real answers!)"
    elif any(word in message for word in ["data", "tabular", "pandas", "numpy", "list", "dictionary", "tuple"]):
        agent = "concepts-agent"
        response = f"[Concepts Agent] It looks like you're asking about data structures or libraries. For '{request.message}', you should explore Pandas for tabular data or built-in lists/dictionaries."
    elif any(phrase in message for phrase in ["error", "bug", "wrong", "stuck", "fail", "broken", "fix"]):
        agent = "debug-agent"
        response = f"[Debug Agent] I see you're having trouble. Let me help you debug: '{request.message}'"
    elif any(word in message for word in ["practice", "exercise", "challenge", "quiz", "test"]):
        agent = "exercise-agent"
        response = f"[Exercise Agent] Here's a practice exercise for you based on: '{request.message}'"
    elif any(word in message for word in ["progress", "score", "how am i", "stats"]):
        agent = "progress-agent"
        response = f"[Progress Agent] Here's your learning progress summary."
    else:
        agent = "triage-agent"
        response = f"[Triage Agent] I'm not sure which agent handles that. Try asking to 'explain' a concept, 'fix' a bug, or 'practice' a skill."
    
    return ChatResponse(response=response, agent=agent)

@app.get("/api/chat", response_model=ChatResponse)
async def chat_get(message: str):
    """
    Chat with the AI tutor via GET request.
    Allows testing via browser: /api/chat?message=help
    """
    # Reuse the logic from the POST endpoint
    request = ChatRequest(message=message)
    return await chat(request)

@app.get("/api/agents")
async def list_agents():
    """List all available AI tutoring agents."""
    return {
        "agents": [
            {"name": "triage-agent", "purpose": "Routes queries to specialists"},
            {"name": "concepts-agent", "purpose": "Explains Python concepts"},
            {"name": "debug-agent", "purpose": "Helps fix errors"},
            {"name": "exercise-agent", "purpose": "Generates practice challenges"},
            {"name": "progress-agent", "purpose": "Tracks learning progress"},
            {"name": "code-review-agent", "purpose": "Reviews code quality"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
