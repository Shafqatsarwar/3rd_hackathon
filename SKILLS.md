# SKILLS.md
## Skill Operating Contract & Canonical Index

**Status**: Authoritative  
**Applies To**: All AI Coding Agents (Claude Code, Goose, Codex-compatible)  
**Governed By**: `specs/governance/skills.spec.md`  
**Project**: LearnFlow - AI-Powered Python Tutoring Platform

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

This is the **single source of truth** for Skills in this project.

### 6.1 Foundation & Governance Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| `agents-md-gen` | Generate and maintain `AGENTS.md` | ✅ Ready |
| `spec-governance-check` | Enforce spec + constitution compliance | ✅ Ready |

### 6.2 Kubernetes & Infrastructure Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| `kafka-k8s-setup` | Deploy Kafka on Kubernetes | ✅ Ready |
| `postgres-k8s-setup` | Deploy PostgreSQL + migrations | ✅ Ready |

### 6.3 Application Runtime Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| `fastapi-dapr-agent` | Create FastAPI + Dapr services | ✅ Ready |
| `nextjs-k8s-deploy` | Build & deploy Next.js frontend | ✅ Ready |
| `mcp-code-execution` | MCP via script execution pattern | ✅ Ready |

### 6.4 Documentation & Quality Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| `docusaurus-deploy` | Deploy documentation site | ✅ Ready |

---

## 7. Skill Quick Reference

### agents-md-gen
```bash
cd .claude/skills/agents-md-gen
./scripts/generate_agents_md.sh
```

### spec-governance-check
```bash
cd .claude/skills/spec-governance-check
python scripts/validate_repo.py
```

### kafka-k8s-setup
```bash
cd .claude/skills/kafka-k8s-setup
./scripts/deploy.sh
python scripts/verify.py
```

### postgres-k8s-setup
```bash
cd .claude/skills/postgres-k8s-setup
./scripts/deploy.sh
./scripts/migrate.sh
python scripts/verify.py
```

### fastapi-dapr-agent
```bash
cd .claude/skills/fastapi-dapr-agent
./scripts/generate_service.sh <service-name>
./scripts/deploy_dapr.sh <service-name>
python scripts/verify_service.py <service-name>
```

### nextjs-k8s-deploy
```bash
cd .claude/skills/nextjs-k8s-deploy
./scripts/prepare_deployment.sh <app-name>
./scripts/build_push_image.sh <app-name>
./scripts/deploy_nextjs.sh <app-name>
python scripts/verify_deployment.py <app-name>
```

### mcp-code-execution
```bash
cd .claude/skills/mcp-code-execution
./scripts/setup_mcp.sh
python scripts/create_client.py
python scripts/mcp_operation.py <server> <method> [params]
```

### docusaurus-deploy
```bash
cd .claude/skills/docusaurus-deploy
./scripts/prepare_site.sh <site-name>
./scripts/build_push_docs.sh <site-name>
./scripts/deploy_docusaurus.sh <site-name>
python scripts/verify_site.py <site-name>
```

---

## 8. Skill Registration Rules

Any new Skill MUST:

1. ✅ Follow mandatory anatomy (SKILL.md, scripts/, REFERENCE.md)
2. ✅ Be added to the Canonical Index above
3. ✅ Declare validation criteria in SKILL.md
4. ✅ Be agent-agnostic (Claude + Goose)
5. ✅ Be reusable beyond one repo
6. ✅ Have verify.py or equivalent

**Unregistered Skills are non-existent.**

---

## 9. Validation Is Part of the Skill

A Skill without validation is **incomplete**.

Validation MUST:
- Be explicit (not assumed)
- Be script-based (verify.py)
- Produce minimal output (< 50 tokens)
- Fail loudly (exit code non-zero)

**Valid Validation Examples:**
- Pods running: `kubectl get pods`
- Topics exist: `kafka-topics --list`
- Schemas applied: `psql -c "\dt"`
- Services reachable: `curl /health`

---

## 10. Anti-Patterns (Hard Stop)

Agents MUST NOT:

| Anti-Pattern | Violation |
|--------------|-----------|
| Write infrastructure manually | Use Skills |
| Use `kubectl` outside Skills | Wrap in Skill |
| Inline YAML/JSON blobs | Context bloat |
| Skip validation | Truth violation |
| Create agent-specific variants | Portability violation |
| "Temporarily" bypass this file | Governance violation |

**If detected: STOP → FIX → RETRY**

---

## 11. Relationship to Other Files

| File | Role | Location |
|------|------|----------|
| `constitution.md` | Philosophical & strategic law | `.specify/memory/` |
| `specs/governance/*.spec.md` | Machine-readable law | `specs/governance/` |
| `AGENTS.md` | Behavioral contract | Root |
| `SKILLS.md` | Operational execution contract | Root |

**All four must agree. Conflicts are bugs.**

---

## 12. Token Efficiency Proof

| Approach | Token Cost |
|----------|------------|
| Direct MCP (5 tools) | ~50,000 tokens |
| Inline code authoring | ~5,000+ tokens |
| **Skills + Scripts** | **~200 tokens** |

**Savings: 99.7%**

---

## 13. Final Reminder (Non-Negotiable)

> **The Spec defines intent**  
> **The Skill defines execution**  
> **The Script does the work**  
> **Validation defines truth**

If you are unsure what to do:

```
┌─────────────────────────────────────────┐
│     READ THIS FILE FIRST.               │
│                                         │
│     STOP → CHECK SKILL INDEX → EXECUTE  │
└─────────────────────────────────────────┘
```

---

**Version**: 1.0  
**Skills**: 8  
**Last Updated**: 2026-02-08

— End of SKILLS.md —
