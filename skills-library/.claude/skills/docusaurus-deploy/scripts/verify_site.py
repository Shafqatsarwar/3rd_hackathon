#!/usr/bin/env python3
# Docusaurus Site Verification Script

import subprocess
import json
import sys
import time

def check_docusaurus_status(site_name, namespace="default"):
    """Verify Docusaurus site is running and accessible"""
    try:
        # Get pods in the namespace
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", namespace, "-l", f"app={site_name}", "-o", "json"],
            capture_output=True, text=True, check=True
        )
        pods = json.loads(result.stdout)["items"]

        # Count running pods
        running = sum(1 for pod in pods if pod["status"]["phase"] == "Running")
        total = len(pods)

        if running == total and total > 0:
            print(f"✓ All {total} Docusaurus pods running")

            # Get service information
            service_result = subprocess.run(
                ["kubectl", "get", "service", f"{site_name}-service", "-n", namespace, "-o", "json"],
                capture_output=True, text=True
            )

            if service_result.returncode == 0:
                service = json.loads(service_result.stdout)
                print(f"✓ Service {site_name}-service is available")

                # Try to get the ingress URL
                ingress_result = subprocess.run(
                    ["kubectl", "get", "ingress", f"{site_name}-ingress", "-n", namespace, "-o", "json"],
                    capture_output=True, text=True
                )

                if ingress_result.returncode == 0:
                    ingress = json.loads(ingress_result.stdout)
                    if ingress.get("status", {}).get("loadBalancer", {}).get("ingress"):
                        urls = ingress["status"]["loadBalancer"]["ingress"]
                        print(f"✓ Site accessible at: {urls[0].get('hostname', urls[0].get('ip', 'unknown'))}")
                    else:
                        print(f"✓ Ingress {site_name}-ingress is configured")

                sys.exit(0)
            else:
                print(f"✗ Service {site_name}-service not available")
                sys.exit(1)
        else:
            print(f"✗ {running}/{total} Docusaurus pods running")
            for pod in pods:
                name = pod["metadata"]["name"]
                status = pod["status"]["phase"]
                print(f"  - {name}: {status}")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to check Docusaurus status: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error checking Docusaurus: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_site.py <site-name> [namespace]")
        sys.exit(1)

    site_name = sys.argv[1]
    namespace = sys.argv[2] if len(sys.argv) > 2 else "default"

    check_docusaurus_status(site_name, namespace)

if __name__ == "__main__":
    main()