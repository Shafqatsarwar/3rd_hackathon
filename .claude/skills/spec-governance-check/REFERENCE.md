# Spec Governance Check - Reference Documentation

## Overview
This skill validates that the repository complies with all governance specifications defined in `specs/governance/`.

## What It Checks

### Skill Compliance
- SKILL.md exists and is < 150 tokens
- scripts/ directory exists
- At least one execution script
- verify.py or equivalent exists
- YAML frontmatter is valid

### Architecture Compliance
- Kubernetes manifests exist
- Dapr configuration present
- No hardcoded values

### MCP Compliance
- No direct MCP tool loading patterns
- Scripts use minimal output patterns

## Configuration

### Environment Variables
- `SPECS_DIR`: Path to specs directory (default: `specs/`)
- `SKILLS_DIR`: Path to skills directory (default: `.claude/skills/`)
- `STRICT_MODE`: Fail on any warning (default: `false`)

### Exclusions
Create `.governance-ignore` to exclude paths:
```
# Ignore test skills
.claude/skills/test-*
# Ignore drafts
specs/drafts/
```

## Output Format

### Success
```
✓ Governance check passed
  Skills: 8/8 compliant
  Specs: 8/8 present
  Score: 100/100
```

### Failure
```
✗ Governance check failed
  Skills: 6/8 compliant
  Issues:
    - fastapi-dapr-agent: Missing verify.py
    - nextjs-k8s-deploy: SKILL.md exceeds 150 tokens
  Score: 75/100
```

## Integration

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
python .claude/skills/spec-governance-check/scripts/validate_repo.py
```

### CI/CD
```yaml
# GitHub Actions
- name: Governance Check
  run: python .claude/skills/spec-governance-check/scripts/validate_repo.py
```

## Scoring Rubric

| Criterion | Points |
|-----------|--------|
| All skills have SKILL.md | 20 |
| All skills have scripts/ | 20 |
| All skills have verify.py | 20 |
| SKILL.md < 150 tokens | 15 |
| No anti-patterns | 15 |
| Specs complete | 10 |
| **Total** | **100** |
