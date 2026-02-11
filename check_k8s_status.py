import subprocess
import sys

def get_status():
    log_file = "k8s_status_log.txt"
    with open(log_file, "w") as f:
        f.write("--- KUBERNETES STATUS START ---\n")
        print("--- KUBERNETES STATUS START ---", flush=True)
        try:
            # Check all pods
            process = subprocess.Popen(["wsl", "kubectl", "get", "pods", "-A"], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=30)
            
            f.write(stdout)
            f.write(stderr)
            print(stdout, flush=True)
            print(stderr, flush=True)
            
            # Check namespaces
            process_ns = subprocess.Popen(["wsl", "kubectl", "get", "ns"], 
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout_ns, stderr_ns = process_ns.communicate(timeout=30)
            f.write("\n--- NAMESPACES ---\n")
            f.write(stdout_ns)
            print("\n--- NAMESPACES ---", flush=True)
            print(stdout_ns, flush=True)
            
        except Exception as e:
            f.write(f"Error: {e}\n")
            print(f"Error: {e}", flush=True)
        f.write("--- KUBERNETES STATUS END ---\n")
        print("--- KUBERNETES STATUS END ---", flush=True)

if __name__ == "__main__":
    get_status()
