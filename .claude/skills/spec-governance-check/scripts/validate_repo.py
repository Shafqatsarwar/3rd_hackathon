#!/usr/bin/env python3
"""
Governance Validation Script
Scans repo and validates against governance specs.
Returns minimal output for token efficiency.
"""
import os
import sys
import re
from pathlib import Path
from typing import List, Tuple

# Force unbuffered output
sys.stdout.reconfigure(encoding='utf-8')

def print_flush(msg):
    print(msg, flush=True)

def count_tokens(text: str) -> int:
    """Rough token count (words + punctuation)."""
    return len(text.split()) + len(re.findall(r'[^\w\s]', text))

def check_skill(skill_path: Path) -> Tuple[str, List[str]]:
    """Check a single skill for compliance."""
    issues = []
    skill_name = skill_path.name
    print(f"Checking skill: {skill_name}...", flush=True)
    
    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        issues.append("Missing SKILL.md")
    else:
        content = skill_md.read_text(encoding='utf-8', errors='ignore')
        tokens = count_tokens(content)
        if tokens > 200:
            issues.append(f"SKILL.md exceeds 200 tokens ({tokens})")
        
        # Check YAML frontmatter
        if not content.strip().startswith('---'):
            issues.append("Missing YAML frontmatter")
    
    # Check scripts/ exists
    scripts_dir = skill_path / "scripts"
    if not scripts_dir.exists():
        issues.append("Missing scripts/ directory")
    else:
        scripts = list(scripts_dir.glob("*"))
        if not scripts:
            issues.append("No scripts in scripts/")
        
        # Check for verify script
        has_verify = any(
            'verify' in s.name.lower() 
            for s in scripts
        )
        if not has_verify:
            issues.append("No verification script")
    
    return skill_name, issues

def check_specs(specs_dir: Path) -> Tuple[int, int, List[str]]:
    """Check that required specs exist."""
    required_specs = [
        "governance/system.spec.md",
        "governance/skills.spec.md",
        "governance/mcp.spec.md",
        "governance/architecture.spec.md",
        "governance/autonomy.spec.md",
        "governance/validation.spec.md",
    ]
    
    found = 0
    missing = []
    
    for spec in required_specs:
        spec_path = specs_dir / spec
        if spec_path.exists():
            found += 1
        else:
            missing.append(spec)
    
    return found, len(required_specs), missing

def calculate_score(skill_results: List[Tuple[str, List[str]]], 
                    specs_found: int, specs_total: int) -> int:
    """Calculate governance score (0-100)."""
    score = 0
    total_skills = len(skill_results)
    
    if total_skills == 0:
        return 0
    
    # Skills with SKILL.md (20 points)
    with_skill_md = sum(1 for _, issues in skill_results 
                        if "Missing SKILL.md" not in issues)
    score += int((with_skill_md / total_skills) * 20)
    
    # Skills with scripts/ (20 points)
    with_scripts = sum(1 for _, issues in skill_results 
                       if "Missing scripts/ directory" not in issues)
    score += int((with_scripts / total_skills) * 20)
    
    # Skills with verify (20 points)
    with_verify = sum(1 for _, issues in skill_results 
                      if "No verification script" not in issues)
    score += int((with_verify / total_skills) * 20)
    
    # Token compliance (15 points)
    token_compliant = sum(1 for _, issues in skill_results 
                          if not any("exceeds" in i for i in issues))
    score += int((token_compliant / total_skills) * 15)
    
    # No anti-patterns (15 points)
    clean = sum(1 for _, issues in skill_results if len(issues) == 0)
    score += int((clean / total_skills) * 15)
    
    # Specs complete (10 points)
    score += int((specs_found / specs_total) * 10)
    
    return min(score, 100)

def main():
    # Find project root
    # Try to find .claude/skills by walking up from CWD
    cwd = Path.cwd().resolve()
    root = cwd
    while not (root / ".claude" / "skills").exists():
        if root.parent == root:
            # Reached filesystem root without finding it
            # Fallback to script location logic
            root = Path(__file__).resolve().parent.parent.parent.parent
            break
        root = root.parent
    
    script_dir = root
    skills_dir = script_dir / ".claude" / "skills"
    specs_dir = script_dir / "specs"
    
    print(f"Project root detected at: {script_dir}", flush=True)

    if not skills_dir.exists():
        print(f"[ERROR] Skills directory not found at {skills_dir}", flush=True)
        sys.exit(1)
    
    # Check skills
    skill_results = []
    if skills_dir.exists():
        for skill_path in skills_dir.iterdir():
            if skill_path.is_dir():
                result = check_skill(skill_path)
                skill_results.append(result)
    
    # Check specs
    specs_found, specs_total, missing_specs = check_specs(specs_dir)
    
    # Calculate score
    score = calculate_score(skill_results, specs_found, specs_total)
    
    # Count compliant skills
    compliant = sum(1 for _, issues in skill_results if len(issues) == 0)
    total = len(skill_results)
    
    # Output minimal report (ASCII-safe for Windows)
    if score >= 90:
        print(f"[OK] Governance check passed")
        print(f"  Skills: {compliant}/{total} compliant")
        print(f"  Specs: {specs_found}/{specs_total} present")
        print(f"  Score: {score}/100")
        sys.exit(0)
    else:
        print(f"[FAIL] Governance check failed")
        print(f"  Skills: {compliant}/{total} compliant")
        
        # Show up to 5 issues
        issues_shown = 0
        print("  Issues:")
        for skill_name, issues in skill_results:
            if issues and issues_shown < 5:
                print(f"    - {skill_name}: {issues[0]}")
                issues_shown += 1
        
        if missing_specs:
            print(f"  Missing specs: {len(missing_specs)}")
        
        print(f"  Score: {score}/100")
        sys.exit(1)

if __name__ == "__main__":
    main()
