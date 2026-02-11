# Spec-Kit Plus Governance Layer

This directory contains the **machine-readable specifications** that govern all agentic behavior in the LearnFlow project.

## Overview

Spec-Kit Plus transforms governance from prose-based documents into actionable specifications that agents can read and validate against.

```
Constitution (Prose) → Specs (Machine-Readable) → Skills (Executable)
```

---

## Spec Structure

```
specs/
├── governance/                 # System-wide governance rules
│   ├── system.spec.md          # Supreme spec - immutable rules
│   ├── skills.spec.md          # Skill canon law
│   ├── mcp.spec.md             # MCP code execution doctrine
│   ├── architecture.spec.md    # Cloud-native enforcement
│   ├── autonomy.spec.md        # Autonomy scoring logic
│   └── validation.spec.md      # Truth & verification
├── learnflow/                  # Product-specific specs
│   ├── product.spec.md         # Product definition
│   └── agents.spec.md          # AI agent specifications
└── README.md                   # This file
```

---

## Spec Types

| Type | Purpose | Example |
|------|---------|---------|
| `governance` | System-wide rules | `system.spec.md` |
| `product` | Product requirements | `product.spec.md` |
| `system` | System components | `agents.spec.md` |

---

## How Agents Use Specs

### Spec-Kit Plus Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. Spec (Intent)                                        │
│    ↓                                                    │
│ 2. Skill Selection/Generation                           │
│    ↓                                                    │
│ 3. Script Execution                                     │
│    ↓                                                    │
│ 4. Validation (against specs)                           │
└─────────────────────────────────────────────────────────┘
```

### Agent Behavior

Agents MUST:
1. **Read specs first** before taking action
2. **Select or generate Skills** based on specs
3. **Execute Skills** following spec rules
4. **Validate against specs** to confirm compliance

---

## Governance Specs Summary

| Spec | Priority | Purpose |
|------|----------|---------|
| `system.spec.md` | Supreme | Immutable governing principles |
| `skills.spec.md` | High | Skill structure and rules |
| `mcp.spec.md` | High | MCP usage patterns |
| `architecture.spec.md` | High | Cloud-native requirements |
| `autonomy.spec.md` | High | Autonomy scoring |
| `validation.spec.md` | High | Verification requirements |

---

## Compliance Verification

Use the `spec-governance-check` skill to verify compliance:

```bash
cd .claude/skills/spec-governance-check
python scripts/validate_repo.py
```

This will:
- Scan all skills
- Compare behavior vs specs
- Report compliance status
- Fail builds that violate governance

---

## Relationship to Constitution

| Document | Format | Purpose |
|----------|--------|---------|
| `constitution.md` | Prose | Human-readable governance |
| `specs/*.spec.md` | Structured | Machine-readable rules |
| Skills | Executable | Autonomous actions |

The specs are **derived from** the constitution but formatted for machine consumption.

---

**Status**: Active  
**Last Updated**: 2026-02-08
