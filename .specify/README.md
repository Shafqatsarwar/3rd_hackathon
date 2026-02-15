# Spec-Kit Plus: SDD-RI Extension

Spec-Kit Plus is a portable engine for **Specification-Driven Development with Reusable Intelligence (SDD-RI)**. It transforms project governance from passive documentation into an active, machine-readable validation layer.

## Core Acronym: SD-RI
- **SD**: Spec-Driven (The "What")
- **RI**: Reusable Intelligence (The "How")

## Extension Structure

```text
.specify/
├── memory/             # Persistent project context (Constitution)
├── templates/          # Standardized SDD-RI blueprints
│   ├── phr-template    # Prompt History Record (Capture)
│   ├── adr-template    # Architecture Decision Record (Reasoning)
│   ├── spec-template   # Functional Specification (Goal)
│   ├── plan-template   # Technical Implementation Plan (Path)
│   └── tasks-template  # Test-Driven Task Breakdown (Action)
└── scripts/            # Automation for PHR/ADR generation
```

## The SDD-RI Engine (Automation)

The `.specify/scripts/` folder contains a advanced PowerShell engine for coordinating development:

| Script | Purpose | Feature |
|--------|---------|---------|
| `update-agent-context.ps1` | Agent Synchronization | Automatically updates `CLAUDE.md`, `GEMINI.md`, etc. with latest plan data. |
| `create-new-feature.ps1` | Scaffolding | Initializes CAPS-compliant directories for new features. |
| `check-prerequisites.ps1` | Environment | Ensures WSL, PowerShell, and Python environments are aligned. |
| `setup-plan.ps1` | Methodology | Prepares the technical strategy from templates. |

## The SDD-RI Workflow

1. **Spec**: Define the intent in `specs/<feature>/spec.md`.
2. **Plan**: Draft technical strategy in `specs/<feature>/plan.md`.
3. **Tasks**: Break down actions in `specs/<feature>/tasks.md`.
4. **Automate**: Run `./.specify/scripts/powershell/update-agent-context.ps1` to sync memory.
5. **Capture**: Every user interaction creates a **PHR** in `history/prompts/`.
6. **Decide**: Significant changes generate an **ADR** in `history/adr/`.

## Governance Integration

The extension is governed by the `specs/governance/` library, which enforces strict rules on context efficiency and autonomous execution.

---
**Status**: Stable  
**AAIF Standard**: Compliant  
