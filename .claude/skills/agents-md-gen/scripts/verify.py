import os

def verify():
    """Verify scripts exist."""
    scripts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
    if os.path.exists(scripts_dir):
        print("✓ agents-md-gen: Scripts directory exists")
        return True
    print("✗ agents-md-gen: Missing scripts directory")
    return False

if __name__ == "__main__":
    verify()
