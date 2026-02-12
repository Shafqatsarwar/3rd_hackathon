import subprocess
import os
import sys

def run_and_log(cmd, log_file):
    with open(log_file, "a") as f:
        f.write(f"\n--- Running: {cmd} ---\n")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            f.write(result.stdout)
            if result.stderr:
                f.write(f"\nSTDERR:\n{result.stderr}")
            f.write(f"\nReturn code: {result.returncode}\n")
        except Exception as e:
            f.write(f"\nERROR: {str(e)}\n")

if __name__ == "__main__":
    log = "proxy_log.txt"
    if os.path.exists(log):
        os.remove(log)
    
    # Core health checks
    run_and_log("dir", log)
    run_and_log("wsl minikube status", log)
    run_and_log("wsl kubectl get nodes", log)
    run_and_log("wsl kubectl get pods -A", log)
