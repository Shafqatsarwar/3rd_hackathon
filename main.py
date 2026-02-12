"""
LearnFlow Root Entry Point (Proxy)
Allows running the backend from the project root.
"""
import sys
import sys
import os
from pathlib import Path
import importlib.util

# Paths
root_path = Path(__file__).parent.absolute()
backend_path = root_path / "src" / "backend"
backend_main = backend_path / "main.py"

# Import backend/main.py explicitly to avoid shadowing
if not backend_main.exists():
    print(f"Error: Could not find backend main file at {backend_main}")
    sys.exit(1)

# Use importlib to load the module under a different name
spec = importlib.util.spec_from_file_location("backend_main", str(backend_main))
backend_module = importlib.util.module_from_spec(spec)
sys.modules["backend_main"] = backend_module

try:
    spec.loader.exec_module(backend_module)
    app = backend_module.app
except Exception as e:
    print(f"Error loading backend: {e}")
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    # Note: We point uvicorn to THIS root file, which now has 'app' defined
    uvicorn.run(app, host="0.0.0.0", port=port)
