# SKILLS.md
## Skill Operating Contract & Canonical Index

**Status**: Authoritative  
**Applies To**: All AI Coding Agents (Claude Code, Goose, Codex-compatible)  
**Governed By**: `specs/governance/skills.spec.md`  
**Repository**: Skills Library - Reusable Intelligence

---

## 1. Purpose of This File

This is the **single canonical entry point** for all Skills in this repository.

It exists to:
- Define how Skills must be structured
- Provide a complete index of available Skills
- Enforce Skill-first development
- Ensure cross-agent compatibility

**If a Skill is not listed here, it does not exist.**

---

## 2. Skill Philosophy

> **The Skill is the Product.**  
> **Code is the byproduct.**

Skills are:
- Reusable across projects
- Executable by any AI agent
- Token-efficient by design
- Self-validating

---

## 3. Mandatory Skill Anatomy

Every Skill MUST follow this structure:

```
.claude/skills/<skill-name>/
├── SKILL.md           # ≤ 200 tokens - Loaded into context
├── REFERENCE.md       # Deep docs - Loaded on demand
└── scripts/
    ├── main.sh        # Primary execution
    ├── verify.py      # Validation script
    └── [helpers]      # Supporting scripts
```

### Token Budget

| Component | Token Limit | Loaded |
|-----------|-------------|--------|
| SKILL.md | ≤ 150 | Always |
| REFERENCE.md | Unlimited | On demand |
| scripts/* | 0 | Never (external execution) |

---

## 4. Skill Usage Protocol

### 4.1 If a Skill Exists
- ✅ Use it
- ❌ Do NOT re-implement logic
- ❌ Do NOT inline commands

### 4.2 If a Skill Does NOT Exist
1. Create a new Skill following anatomy
2. Register it in this file
3. Then execute it

**Skipping Skill creation is a violation.**

---

## 5. MCP Code Execution Law

All MCP usage MUST follow the **Code Execution Pattern**.

### ✅ Allowed
- MCP calls inside scripts
- Filtered results returned
- Minimal output (< 50 tokens)

### ❌ Forbidden
- Direct MCP tool loading
- Raw MCP payloads in context
- Tool schemas in context

> **MCP is a backend API, not a chat interface.**

---

## 6. Canonical Skill Index

This is the **single source of truth** for Skills in this library.

### 6.1 Foundation & Governance Skills

| Skill | Purpose | Scripts | Status |
|-------|---------|---------|--------|
| `agents-md-gen` | Generate AGENTS.md | 1 | ✅ Ready |
| `spec-governance-check` | Validate governance | 1 | ✅ Ready |

### 6.2 Kubernetes & Infrastructure Skills

| Skill | Purpose | Scripts | Status |
|-------|---------|---------|--------|
| `kafka-k8s-setup` | Deploy Kafka | 2 | ✅ Ready |
| `postgres-k8s-setup` | Deploy PostgreSQL | 3 | ✅ Ready |

### 6.3 Application Runtime Skills

| Skill | Purpose | Scripts | Status |
|-------|---------|---------|--------|
| `fastapi-dapr-agent` | FastAPI + Dapr | 3 | ✅ Ready |
| `nextjs-k8s-deploy` | Next.js deploy | 4 | ✅ Ready |
| `mcp-code-execution` | MCP pattern | 3 | ✅ Ready |

### 6.4 Documentation Skills

| Skill | Purpose | Scripts | Status |
|-------|---------|---------|--------|
| `docusaurus-deploy` | Docs site | 4 | ✅ Ready |

**Total: 8 Skills, 21 Scripts**

---

## 7. Skill Registration Rules

Any new Skill MUST:

1. ✅ Follow mandatory anatomy
2. ✅ Be added to the Canonical Index
3. ✅ Declare validation criteria
4. ✅ Be agent-agnostic
5. ✅ Be reusable beyond one repo

**Unregistered Skills are non-existent.**

---

## 8. Validation Is Part of the Skill

A Skill without validation is **incomplete**.

Validation MUST:
- Be explicit
- Be script-based
- Produce minimal output
- Fail loudly

---

## 9. Anti-Patterns (Hard Stop)

| Anti-Pattern | Violation |
|--------------|-----------|
| Write infrastructure manually | Use Skills |
| Inline YAML/JSON blobs | Context bloat |
| Skip validation | Truth violation |
| Agent-specific variants | Portability violation |

---

## 10. Relationship to Other Files

| File | Role |
|------|------|
| `constitution.md` | Strategic law |
| `specs/governance/*` | Machine-readable law |
| `AGENTS.md` | Behavioral contract |
| `SKILLS.md` | Execution contract |

---

## 11. Final Reminder

> **The Spec defines intent**  
> **The Skill defines execution**  
> **The Script does the work**  
> **Validation defines truth**

**READ THIS FILE FIRST.**

---

**Version**: 1.0  
**Skills**: 8  
**Last Updated**: 2026-02-08

— End of SKILLS.md —
