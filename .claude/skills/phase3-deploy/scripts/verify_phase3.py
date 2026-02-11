#!/usr/bin/env python3
"""Verify Phase 3 deployment - 6 AI agents with Dapr"""
import subprocess
import sys
import json

AGENTS = ["triage-agent", "concepts-agent", "debug-agent", 
          "exercise-agent", "progress-agent", "code-review-agent"]
NAMESPACE = "learnflow"

def run_cmd(cmd):
    """Run command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

def check_pods():
    """Check all agent pods are running"""
    print("🔍 Checking agent pods...")
    cmd = f"kubectl get pods -n {NAMESPACE} -o json"
    output, code = run_cmd(cmd)
    
    if code != 0:
        print(f"❌ Failed to get pods: {output}")
        return False
    
    pods = json.loads(output)
    running_agents = set()
    
    for pod in pods.get('items', []):
        name = pod['metadata']['name']
        status = pod['status']['phase']
        containers = pod['status'].get('containerStatuses', [])
        
        # Check if pod is for one of our agents
        for agent in AGENTS:
            if name.startswith(agent):
                if status == 'Running' and len(containers) == 2:  # app + dapr
                    all_ready = all(c.get('ready', False) for c in containers)
                    if all_ready:
                        running_agents.add(agent)
                        print(f"   ✅ {agent}: Running (2/2)")
                    else:
                        print(f"   ⚠️  {agent}: Running but not ready")
                else:
                    print(f"   ❌ {agent}: {status}")
    
    missing = set(AGENTS) - running_agents
    if missing:
        print(f"\n❌ Missing agents: {', '.join(missing)}")
        return False
    
    print(f"\n✅ All {len(AGENTS)} agents running with Dapr sidecars")
    return True

def check_services():
    """Check all services exist"""
    print("\n🔍 Checking services...")
    for agent in AGENTS:
        cmd = f"kubectl get svc {agent} -n {NAMESPACE} -o json 2>/dev/null"
        output, code = run_cmd(cmd)
        if code == 0:
            print(f"   ✅ {agent} service")
        else:
            print(f"   ❌ {agent} service missing")
            return False
    return True

def main():
    """Main verification"""
    print("=" * 60)
    print("Phase 3 Deployment Verification")
    print("=" * 60)
    
    checks = [
        ("Agent Pods", check_pods),
        ("Services", check_services),
    ]
    
    results = []
    for name, check_fn in checks:
        try:
            result = check_fn()
            results.append(result)
        except Exception as e:
            print(f"\n❌ {name} check failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ Phase 3 Deployment: SUCCESS")
        print("=" * 60)
        return 0
    else:
        print("❌ Phase 3 Deployment: FAILED")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
