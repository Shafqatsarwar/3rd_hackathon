import os

def verify():
    """Verify scripts exist."""
    scripts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
    if os.path.exists(scripts_dir):
        print("✓ spec-governance-check: Scripts directory exists")
        return True
    print("✗ spec-governance-check: Missing scripts directory")
    return False

if __name__ == "__main__":
    verify()
