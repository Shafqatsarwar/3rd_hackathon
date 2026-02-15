# CAPS Library: The Governance Core

The **CAPS Library** is the authoritative source of truth for the LearnFlow system. It follows the **C-A-P-S** governance methodology.

## What is CAPS?

| Layer | Component | Purpose |
|-------|-----------|---------|
| **C** | **Constitution** | The "Supreme Law" - prose principles in `.specify/memory/`. |
| **A** | **Agents** | Definitions of AI roles and boundaries in `specs/learnflow/agents.spec.md`. |
| **P** | **Product** | Business requirements and feature specs in `specs/learnflow/product.spec.md`. |
| **S** | **Specs** | Machine-readable technical rules in `specs/governance/`. |

## Library Structure

```text
specs/
├── governance/             # System Architecture & Compliance
│   ├── system.spec.md      # Immutable rules
│   ├── skills.spec.md      # Executable patterns
│   └── mcp.spec.md         # Data access rules
└── learnflow/              # Domain-Specific Knowledge
    ├── product.spec.md     # Tutoring logic
    └── agents.spec.md      # Multi-agent routing
```

## Governance Enforcement

All agents MUST prioritize these specs over internal knowledge. Compliance is enforced autonomously via the `spec-governance-check` skill.

---
**Status**: Authoritative  
**Standard**: AAIF Spec-Kit Plus  
