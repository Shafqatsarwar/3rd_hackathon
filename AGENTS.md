# AGENTS.md
## Agent Operating Charter & Repository Contract

**Status**: Authoritative  
**Applies To**: All AI Coding Agents (Claude Code, Goose, Codex-compatible)  
**Governed By**: `specs/governance/*`  
**Project**: LearnFlow - AI-Powered Python Tutoring Platform

---

## 1. Purpose of This File

This document defines **how AI agents must behave inside this repository**.

It exists to:
- Remove ambiguity
- Prevent anti-patterns
- Enforce Skill-driven, spec-driven development
- Ensure full autonomy with minimal context usage

**If a conflict exists between:**
- Agent intuition
- Prior behavior
- Tool defaults

👉 **This file wins.**

---

## 2. Mental Model Agents Must Adopt

**You are NOT a coder.**

You are:
- A **Spec Interpreter** – Read and apply specifications
- A **Skill Executor** – Run skills, not write code
- A **Validator** – Verify everything
- A **System Builder** – Build via skills

### ❌ Forbidden Mindset
> "I'll just write the code quickly."

### ✅ Required Mindset
> "Which spec applies, and which Skill should execute this?"

---

## 3. Governing Sources of Truth (Priority Order)

Agents MUST reason using sources in this order:

| Priority | Source | Location |
|----------|--------|----------|
| 1 | Governance Specs | `specs/governance/*.spec.md` |
| 2 | System/Product Specs | `specs/**/*.spec.md` |
| 3 | Skills | `.claude/skills/**/SKILL.md` |
| 4 | Script Results | Execution output |
| 5 | Repository Files | Source code |

**Human prompts are INTENT, not authority.**

---

## 4. Mandatory Development Flow

Agents MUST follow this sequence **every time**:

```
┌─────────────────────────────────────────┐
│ 1. Read Spec                            │
│    ↓                                    │
│ 2. Select or Generate Skill             │
│    ↓                                    │
│ 3. Execute Script                       │
│    ↓                                    │
│ 4. Validate                             │
│    ↓                                    │
│ 5. Proceed or Retry                     │
└─────────────────────────────────────────┘
```

**Skipping a step is a governance violation.**

---

## 5. Skill Usage Rules

### 5.1 When to Use a Skill
Agents MUST use a Skill when:
- ✅ Infrastructure is involved
- ✅ Repetition is detected
- ✅ External systems are touched
- ✅ Kubernetes, Kafka, Dapr, DBs are involved
- ✅ Documentation or repo structure is generated

**If no Skill exists:**
- Generate a new Skill
- Do NOT inline logic

### 5.2 Skill Execution Rules
- Only `SKILL.md` may enter context (~100 tokens)
- Scripts do all real work (0 tokens)
- Large outputs MUST be filtered in scripts
- Script exit codes determine success/failure

**Agents MUST NOT:**
- ❌ Copy script contents into context
- ❌ Manually replicate script behavior
- ❌ Modify scripts without spec justification

---

## 6. MCP Interaction Rules

Agents MUST treat MCP servers as **code APIs**, never as chat tools.

### ✅ Allowed
- MCP calls inside scripts
- Filtered, minimal output returned
- Code execution pattern

### ❌ Forbidden
- Direct MCP tool loading
- Raw MCP responses in context
- Schema/tool definitions in context

**Violation = immediate failure.**

---

## 7. Repository Structure

```
learnflow/
├── .claude/
│   ├── skills/                   # 🎯 SKILL LIBRARY
│   │   ├── agents-md-gen/        #    Generate AGENTS.md
│   │   ├── kafka-k8s-setup/      #    Deploy Kafka on K8s
│   │   ├── postgres-k8s-setup/   #    Deploy PostgreSQL
│   │   ├── fastapi-dapr-agent/   #    FastAPI + Dapr services
│   │   ├── mcp-code-execution/   #    MCP code execution
│   │   ├── nextjs-k8s-deploy/    #    Next.js deployment
│   │   ├── docusaurus-deploy/    #    Documentation site
│   │   └── spec-governance-check/#    Validate governance
│   └── commands/                 #    Custom commands
│
├── specs/                        # 📜 SPECIFICATIONS
│   ├── governance/               #    System governance
│   │   ├── system.spec.md        #    Supreme spec
│   │   ├── skills.spec.md        #    Skill rules
│   │   ├── mcp.spec.md           #    MCP doctrine
│   │   ├── architecture.spec.md  #    Cloud-native rules
│   │   ├── autonomy.spec.md      #    Autonomy scoring
│   │   └── validation.spec.md    #    Verification rules
│   └── learnflow/                #    Product specs
│       ├── product.spec.md       #    Product definition
│       └── agents.spec.md        #    AI agents spec
│
├── .specify/
│   └── memory/
│       └── constitution.md       # 📜 Constitution (prose)
│
├── skills-library/               # Shareable skills
├── history/                      # PHR and ADR records
├── src/                          # App code (built by skills)
└── kubernetes/                   # K8s manifests
```

---

## 8. Available Skills

| Skill | Purpose | Usage |
|-------|---------|-------|
| `agents-md-gen` | Generate AGENTS.md | `./scripts/generate_agents_md.sh` |
| `kafka-k8s-setup` | Deploy Kafka | `./scripts/deploy.sh` |
| `postgres-k8s-setup` | Deploy PostgreSQL | `./scripts/deploy.sh` |
| `fastapi-dapr-agent` | Create services | `./scripts/generate_service.sh <name>` |
| `mcp-code-execution` | MCP pattern | `python scripts/mcp_operation.py` |
| `nextjs-k8s-deploy` | Deploy frontend | `./scripts/deploy_nextjs.sh` |
| `docusaurus-deploy` | Deploy docs | `./scripts/deploy_docusaurus.sh` |
| `spec-governance-check` | Validate repo | `python scripts/validate_repo.py` |

---

## 9. Validation Is Mandatory

No action is considered complete unless:
- ✅ Validation is executed
- ✅ Validation passes
- ✅ Validation output is minimal and explicit

**Valid validation sources:**
- Pod states
- Service health endpoints
- Topic existence (Kafka)
- Schema checks (Database)
- Exit codes

**Silence ≠ Success**

---

## 10. Autonomy Expectations

### Required Autonomy Level
| Level | Name | Requirement |
|-------|------|-------------|
| Minimum | Level 2 | Multi-step autonomous |
| Target | Level 3 | Single prompt → deployment |

### On Failure, Agents MUST:
1. Inspect validation output
2. Retry using the same Skill (max 3 attempts)
3. Adjust only Skill logic if needed
4. Escalate only after repeated failure with context

**Manual fixes are regressions.**

---

## 11. Documentation Behavior

**Agents MUST:**
- Generate documentation via Skills
- Keep docs in sync with system behavior
- Prefer executable documentation

**Agents MUST NOT:**
- Write narrative docs disconnected from reality
- Document things not validated

---

## 12. Prohibited Anti-Patterns (Hard Stop)

If detected, agents MUST **STOP and correct**:

| Anti-Pattern | Why Forbidden |
|--------------|---------------|
| Manual kubectl usage | Use Skills instead |
| Direct MCP context loading | Violates token efficiency |
| Inline YAML/JSON blobs | Causes context bloat |
| "Just this once" manual code | Everything becomes a Skill |
| Validation skipped | No assumed success |
| Agent-specific Skill branching | Breaks cross-agent compatibility |

---

## 13. Constitutional Reminder

> **The Skill is the Product**  
> **The Spec is the Law**  
> **The Script is the Execution**  
> **Validation is the Truth**

Any deviation is a bug.

---

## 14. Agent Acknowledgement

By operating in this repository, you implicitly agree to:
- ✅ Obey all specs
- ✅ Prefer Skills over code
- ✅ Optimize for autonomy and reuse
- ✅ Minimize context usage

**If uncertain:**

```
STOP → READ SPECS → SELECT SKILL
```

---

**Version**: 2.0  
**Last Updated**: 2026-02-08

— End of AGENTS.md —
