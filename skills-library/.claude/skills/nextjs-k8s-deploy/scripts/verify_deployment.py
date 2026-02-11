#!/usr/bin/env python3
"""
Verify Next.js Kubernetes Deployment
Returns minimal output for token efficiency
"""
import subprocess
import json
import sys

def get_deployment_status(app_name: str, namespace: str = "learnflow"):
    """Check deployment status for the Next.js app."""
    result = subprocess.run(
        ["kubectl", "get", "deployment", app_name, "-n", namespace, "-o", "json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None, f"Deployment not found: {result.stderr[:100]}"
    
    return json.loads(result.stdout), None

def get_pod_status(app_name: str, namespace: str = "learnflow"):
    """Check pod status for the app."""
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace, "-l", f"app={app_name}", "-o", "json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None, f"Pods not found: {result.stderr[:100]}"
    
    return json.loads(result.stdout)["items"], None

def get_service_status(app_name: str, namespace: str = "learnflow"):
    """Check service status."""
    result = subprocess.run(
        ["kubectl", "get", "service", app_name, "-n", namespace, "-o", "json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None, f"Service not found: {result.stderr[:100]}"
    
    return json.loads(result.stdout), None

def check_health_endpoint(app_name: str, namespace: str = "learnflow"):
    """Check if health endpoint responds."""
    # Port-forward and check (simplified for verification)
    result = subprocess.run(
        ["kubectl", "exec", "-n", namespace, f"deploy/{app_name}", "--", 
         "wget", "-q", "-O", "-", "http://localhost:3000/api/health"],
        capture_output=True, text=True, timeout=10
    )
    return result.returncode == 0

def main():
    app_name = sys.argv[1] if len(sys.argv) > 1 else "learnflow-frontend"
    namespace = sys.argv[2] if len(sys.argv) > 2 else "learnflow"
    
    errors = []
    
    # Check deployment
    deployment, err = get_deployment_status(app_name, namespace)
    if err:
        errors.append(err)
    else:
        ready = deployment.get("status", {}).get("readyReplicas", 0)
        desired = deployment.get("spec", {}).get("replicas", 1)
        if ready < desired:
            errors.append(f"Deployment: {ready}/{desired} replicas ready")
    
    # Check pods
    pods, err = get_pod_status(app_name, namespace)
    if err:
        errors.append(err)
    else:
        running = sum(1 for p in pods if p.get("status", {}).get("phase") == "Running")
        total = len(pods)
        if running < total:
            errors.append(f"Pods: {running}/{total} running")
    
    # Check service
    service, err = get_service_status(app_name, namespace)
    if err:
        errors.append(err)
    
    # Output minimal result
    if errors:
        print(f"✗ {app_name}: {len(errors)} issues")
        for e in errors[:3]:  # Max 3 errors for token efficiency
            print(f"  - {e}")
        sys.exit(1)
    else:
        ready_count = deployment.get("status", {}).get("readyReplicas", 0)
        service_type = service.get("spec", {}).get("type", "ClusterIP")
        print(f"✓ {app_name}: {ready_count} replicas ready, Service: {service_type}")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"✗ Verification error: {str(e)[:100]}")
        sys.exit(1)
