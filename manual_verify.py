import os
from pathlib import Path

def check_skills():
    print("Checking skills...", flush=True)
    skills_dir = Path(".claude/skills")
    if not skills_dir.exists():
        print(f"Skills directory not found: {skills_dir}")
        return

    for skill in skills_dir.iterdir():
        if skill.is_dir():
            skill_md = skill / "SKILL.md"
            if not skill_md.exists():
                print(f"[FAIL] {skill.name}: Missing SKILL.md")
            else:
                print(f"[OK] {skill.name}: SKILL.md found")
                # content = skill_md.read_text(encoding='utf-8')
                # if len(content.split()) > 200:
                #    print(f"  [WARN] {skill.name}: SKILL.md > 200 words")

            scripts_dir = skill / "scripts"
            if not scripts_dir.exists():
                print(f"[FAIL] {skill.name}: Missing scripts/ directory")
            else:
                has_deploy = any("deploy" in s.name for s in scripts_dir.iterdir())
                has_verify = any("verify" in s.name for s in scripts_dir.iterdir())
                if not has_verify:
                    print(f"  [WARN] {skill.name}: No verify script found")

if __name__ == "__main__":
    check_skills()
