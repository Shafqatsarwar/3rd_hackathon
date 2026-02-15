import subprocess
import json
import os
from pathlib import Path

SKILLS_ROOT = Path(r"D:\Panaverse\projects\3rd_hackathon\.claude\skills")
RESULTS_FILE = Path(r"D:\Panaverse\projects\3rd_hackathon\validation_results.json")

skills_to_test = [
    {"name": "spec-governance-check", "script": "scripts/validate_repo.py"},
    {"name": "mcp-code-execution", "script": "scripts/verify.py"},
    {"name": "kafka-k8s-setup", "script": "scripts/verify.py"},
    {"name": "postgres-k8s-setup", "script": "scripts/verify.py"},
    {"name": "fastapi-dapr-agent", "script": "scripts/verify_service.py", "args": ["triage-agent"]},
    {"name": "nextjs-k8s-deploy", "script": "scripts/verify_deployment.py", "args": ["learnflow-frontend"]},
    {"name": "phase3-deploy", "script": "scripts/verify_agents_deployment.py"},
    {"name": "agents-md-gen", "script": "scripts/verify.py"},
    {"name": "docusaurus-deploy", "script": "scripts/verify_site.py", "args": ["learnflow-docs"]}
]

results = []

print(f"Starting Validation Sweep for {len(skills_to_test)} skills...")

for skill in skills_to_test:
    name = skill["name"]
    script_rel_path = skill["script"]
    args = skill.get("args", [])
    
    skill_path = SKILLS_ROOT / name
    script_path = skill_path / script_rel_path
    
    print(f"Testing {name}...")
    
    if not script_path.exists():
        results.append({"skill": name, "status": "FAIL", "error": "Script not found"})
        continue
        
    try:
        cmd = ["python", str(script_path)] + args
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=str(skill_path.parent.parent.parent))
        
        status = "PASS" if process.returncode == 0 else "FAIL"
        results.append({
            "skill": name,
            "status": status,
            "stdout": process.stdout[:500],
            "stderr": process.stderr[:500],
            "returncode": process.returncode
        })
    except Exception as e:
        results.append({"skill": name, "status": "ERROR", "error": str(e)})

with open(RESULTS_FILE, "w") as f:
    json.dump(results, f, indent=2)

print(f"Sweep complete. Results written to {RESULTS_FILE}")
