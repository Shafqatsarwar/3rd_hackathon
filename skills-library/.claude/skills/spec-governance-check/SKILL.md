---
name: spec-governance-check
description: Validate repository compliance against governance specifications
---

# Spec Governance Check

## When to Use
- Before committing changes
- During CI/CD pipeline
- When verifying skill compliance
- To audit repository governance

## Instructions
1. Run validation: `python scripts/validate_repo.py`
2. Review compliance report
3. Fix any violations before proceeding

## Validation
- [ ] All skills have SKILL.md < 150 tokens
- [ ] All skills have scripts/ directory
- [ ] All skills have validation logic
- [ ] No forbidden anti-patterns detected

See [REFERENCE.md](./REFERENCE.md) for configuration options.
