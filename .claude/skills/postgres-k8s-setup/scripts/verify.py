#!/usr/bin/env python3
# PostgreSQL Verification Script

import subprocess
import json
import sys

def check_postgres_status():
    """Verify PostgreSQL pods are running and accessible"""
    try:
        # Get pods in postgresql namespace
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", "postgresql", "-o", "json"],
            capture_output=True, text=True, check=True
        )
        pods = json.loads(result.stdout)["items"]

        # Count running pods
        running = sum(1 for pod in pods if pod["status"]["phase"] == "Running")
        total = len(pods)

        if running == total and total > 0:
            print(f"✓ All {total} PostgreSQL pods running")

            # Test database connection
            try:
                # Use kubectl exec to test connection within the cluster
                conn_test = subprocess.run([
                    "kubectl", "exec", "-it", f"{pods[0]['metadata']['name']}", "-n", "postgresql",
                    "--", "pg_isready", "-h", "localhost", "-U", "postgres"
                ], capture_output=True, text=True, timeout=30)

                if conn_test.returncode == 0:
                    print("✓ PostgreSQL is accessible and accepting connections")
                    sys.exit(0)
                else:
                    print(f"✗ PostgreSQL connection test failed: {conn_test.stderr}")
                    sys.exit(1)
            except subprocess.TimeoutExpired:
                print("✗ PostgreSQL connection test timed out")
                sys.exit(1)
        else:
            print(f"✗ {running}/{total} PostgreSQL pods running")
            for pod in pods:
                name = pod["metadata"]["name"]
                status = pod["status"]["phase"]
                print(f"  - {name}: {status}")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to check PostgreSQL status: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error checking PostgreSQL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_postgres_status()