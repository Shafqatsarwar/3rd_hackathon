---
type: governance
scope: skills
version: 1.0
---

# Skill Specification

> **Skill Canon Law** – Machine-readable rules for skill creation and execution.

## Skill Definition

A **Skill** is a reusable, executable instruction set that enables agents to perform a task autonomously.

```
Skill = Intent (SKILL.md) + Execution (scripts/) + Verification (validation)
```

---

## Required Structure

Every Skill MUST contain:

```
.claude/skills/<skill-name>/
├── SKILL.md           # ≤ 200 tokens - Intent only
├── REFERENCE.md       # Optional - Deep documentation
└── scripts/
    ├── main.sh        # Primary execution
    ├── verify.py      # Validation logic
    └── [helpers]      # Supporting scripts
```

### Component Requirements

| Component | Required | Token Limit | Purpose |
|-----------|----------|-------------|---------|
| SKILL.md | ✅ Yes | ≤ 150 | Define intent and steps |
| scripts/ | ✅ Yes | 0 (external) | Execute operations |
| verify.py | ✅ Yes | 0 (external) | Validate success |
| REFERENCE.md | ⚪ Optional | On-demand | Advanced docs |

---

## SKILL.md Format

```yaml
---
name: lowercase-with-dashes
description: Brief description (< 100 chars)
---

# Skill Title

## When to Use
- Trigger condition 1
- Trigger condition 2

## Instructions
1. Command 1: `./scripts/action.sh`
2. Command 2: `python scripts/verify.py`

## Validation
- [ ] Criterion 1
- [ ] Criterion 2

See [REFERENCE.md](./REFERENCE.md) for advanced options.
```

---

## Execution Rules

| Rule | Requirement |
|------|-------------|
| SKILL.md | Defines intent only, no heavy logic |
| Scripts | Perform ALL heavy operations |
| Exit Codes | Non-zero on failure, zero on success |
| Output | Only final status enters context (< 50 tokens) |

---

## Portability Requirement

Skills MUST:
- ✅ Work without modification on **Claude Code**
- ✅ Work without modification on **Goose**
- ✅ Avoid agent-specific assumptions
- ✅ Use portable shell commands (`bash`, `python3`)
- ✅ Use environment variables, not hardcoded paths

---

## Anti-Patterns (Forbidden)

| Anti-Pattern | Why Forbidden |
|--------------|---------------|
| Application code in SKILL.md | Skills define intent, not implementation |
| Inline shell commands | All commands go in scripts/ |
| Logs/manifests in context | Causes token bloat |
| Agent-specific hacks | Breaks cross-agent compatibility |
| No validation | Violates verification mandate |

---

## Skill Validation Checklist

Before marking a skill as "Ready":

- [ ] SKILL.md ≤ 200 tokens
- [ ] scripts/ directory exists
- [ ] At least one execution script
- [ ] verify.py or equivalent exists
- [ ] Tested on Claude Code
- [ ] Tested on Goose (if available)
- [ ] Output is minimal (< 50 tokens)

---

**Status**: Active  
**Last Updated**: 2026-02-08
