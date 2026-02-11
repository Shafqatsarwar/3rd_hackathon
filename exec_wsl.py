import subprocess
import sys

def run_wsl_script(script_path):
    print(f"Executing: wsl bash {script_path}")
    try:
        # Use a list to avoid shell parsing of arguments
        result = subprocess.run(["wsl", "bash", script_path], check=True, text=True)
        print("Successfully executed script")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exec_wsl.py <script_path>")
        sys.exit(1)
    
    run_wsl_script(sys.argv[1])
