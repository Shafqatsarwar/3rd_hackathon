#!/usr/bin/env python3
"""
Verify FastAPI + Dapr service deployment
Returns minimal output for token efficiency
"""
import subprocess
import json
import sys

def get_pod_status(service_name: str, namespace: str = "learnflow"):
    """Check pod status for the service"""
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace, "-l", f"app={service_name}", "-o", "json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None, f"kubectl error: {result.stderr}"
    
    pods = json.loads(result.stdout)["items"]
    if not pods:
        return None, "No pods found"
    
    return pods, None

def check_dapr_sidecar(pod):
    """Check if Dapr sidecar is running"""
    containers = pod.get("status", {}).get("containerStatuses", [])
    for container in containers:
        if "daprd" in container.get("name", ""):
            return container.get("ready", False)
    return False

def main():
    service_name = sys.argv[1] if len(sys.argv) > 1 else "my-service"
    namespace = sys.argv[2] if len(sys.argv) > 2 else "learnflow"
    
    pods, error = get_pod_status(service_name, namespace)
    
    if error:
        print(f"✗ Service verification failed: {error}")
        sys.exit(1)
    
    total = len(pods)
    running = 0
    dapr_ready = 0
    
    for pod in pods:
        phase = pod.get("status", {}).get("phase", "Unknown")
        if phase == "Running":
            running += 1
            if check_dapr_sidecar(pod):
                dapr_ready += 1
    
    if running == total and dapr_ready == total:
        print(f"✓ {service_name}: {running}/{total} pods running, Dapr sidecars healthy")
        sys.exit(0)
    elif running == total:
        print(f"⚠ {service_name}: {running}/{total} pods running, {dapr_ready}/{total} Dapr sidecars ready")
        sys.exit(1)
    else:
        print(f"✗ {service_name}: {running}/{total} pods running")
        sys.exit(1)

if __name__ == "__main__":
    main()
