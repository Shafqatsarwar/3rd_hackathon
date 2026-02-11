import subprocess
import json
import os

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

report = {
    "minikube_status": run_cmd("minikube status"),
    "kubectl_nodes": run_cmd("kubectl get nodes"),
    "kubectl_pods": run_cmd("kubectl get pods -A")
}

with open("infra_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("Report generated: infra_report.json")
