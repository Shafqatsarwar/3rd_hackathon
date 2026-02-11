import os
from pathlib import Path
import sys

def check_skills():
    with open("manual_verify_output.txt", "w") as f:
        f.write("Checking skills...\n")
        skills_dir = Path(".claude/skills")
        if not skills_dir.exists():
            f.write(f"Skills directory not found: {skills_dir}\n")
            return

        for skill in skills_dir.iterdir():
            if skill.is_dir():
                skill_md = skill / "SKILL.md"
                if not skill_md.exists():
                    f.write(f"[FAIL] {skill.name}: Missing SKILL.md\n")
                else:
                    f.write(f"[OK] {skill.name}: SKILL.md found\n")

                scripts_dir = skill / "scripts"
                if not scripts_dir.exists():
                    f.write(f"[FAIL] {skill.name}: Missing scripts/ directory\n")
                else:
                    # check for verify script
                    has_verify = any("verify" in s.name for s in scripts_dir.iterdir())
                    if not has_verify:
                        f.write(f"  [WARN] {skill.name}: No verify script found\n")

if __name__ == "__main__":
    check_skills()
