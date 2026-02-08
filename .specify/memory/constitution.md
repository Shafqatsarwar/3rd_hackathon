# Constitution of the Agentic System
## Reusable Intelligence & Cloud-Native Mastery

**Version**: 2.0  
**Status**: Authoritative  
**Applies To**: All AI Coding Agents (Claude Code, Goose, Codex-compatible agents)  
**Project**: LearnFlow - AI-Powered Python Tutoring Platform  
**Ratified**: 2026-02-08

---

## 1. Purpose & Mission

### 1.1 Core Mission
The mission of this agentic system is to **build cloud-native, distributed applications autonomously** by executing **reusable, measurable Skills**, not by manual code authoring.

> **The Skill is the Product.**  
> **The Application is Proof.**

### 1.2 Paradigm Shift
This system operates under **Agentic Development**, not traditional development.

| Traditional Development | Agentic Development |
|------------------------|---------------------|
| Human writes code | Human writes Skills |
| Code is the asset | Skills are the asset |
| One-off delivery | Reusable intelligence |
| Manual execution | Autonomous execution |
| Debug by reading | Debug by re-running |

### 1.3 LearnFlow Context
LearnFlow is an AI-powered Python tutoring platform. The skills created here will:
- Build the complete platform autonomously
- Demonstrate cloud-native patterns (K8s, Kafka, Dapr)
- Serve as reusable templates for future projects

---

## 2. Constitutional First Principles

These principles are **non-negotiable**.

### 2.1 Skills Over Code
- Agents **MUST NOT** write application code manually unless explicitly instructed
- All behavior **MUST** be driven by **Skills with MCP Code Execution**
- Any repeated pattern **MUST** be elevated into a Skill
- Skills are the primary deliverable, not the application

### 2.2 Code Executes, Tokens Do Not
- MCP tools **MUST NOT** be loaded directly into agent context
- Heavy operations **MUST** execute via scripts outside context
- Context must only contain:
  - Minimal instructions (~100 tokens)
  - Final results (~50 tokens)
  - Validation outcomes

**Token Efficiency Law:**
```
BEFORE (Direct MCP):        ~50,000+ tokens per operation
AFTER (Skills + Scripts):   ~150 tokens per operation
SAVINGS:                    99.7%
```

### 2.3 Autonomy Is the Goal
- Gold standard: **Single prompt → running system**
- Human intervention is considered a **failure signal**, not success
- Agents must self-verify and self-correct using Skills
- If a human must intervene, the Skill is incomplete

---

## 3. Agent Authority & Scope

### 3.1 What the Agent Is ALLOWED To Do
Agents MAY:
- Load and execute Skills from `.claude/skills/`
- Run scripts defined by Skills
- Create repositories, files, services, and Kubernetes resources
- Deploy, verify, and validate infrastructure
- Generate documentation via Skills
- Use MCP only through code execution patterns
- Create new Skills for repeated patterns
- Modify existing Skills to improve them

### 3.2 What the Agent Is FORBIDDEN From Doing
Agents MUST NOT:
- Connect MCP servers directly to context
- Inline large outputs (logs, JSON, manifests) into context
- Write infrastructure manually without a Skill
- Bypass validation steps defined in a Skill
- Assume human approval unless explicitly stated
- Execute destructive operations without validation
- Ignore exit codes from scripts

### 3.3 Escalation Protocol
When encountering issues:
1. Retry using the same Skill (up to 3 attempts)
2. Check REFERENCE.md for troubleshooting
3. Modify script to handle edge case
4. Only then escalate to human

---

## 4. Skill Canon Law

### 4.1 Mandatory Skill Structure
Every Skill MUST follow this structure:

```
.claude/skills/<skill-name>/
├── SKILL.md           # Minimal instructions (~100 tokens)
├── REFERENCE.md       # Deep documentation (loaded on-demand)
└── scripts/
    ├── main.sh        # Primary execution script
    ├── verify.py      # Validation script
    └── helpers/       # Supporting scripts (optional)
```

### 4.2 SKILL.md Requirements
Each `SKILL.md` MUST define:

```yaml
---
name: lowercase-with-dashes
description: One-line description (< 100 chars)
---

# Skill Title

## When to Use
- Trigger condition 1
- Trigger condition 2

## Instructions
1. Step 1: `command`
2. Step 2: `command`
3. Step 3: Validate

## Validation
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

See [REFERENCE.md](./REFERENCE.md) for advanced options.
```

### 4.3 Token Budget
| Section | Max Tokens |
|---------|------------|
| YAML frontmatter | 20 |
| Title + When to Use | 50 |
| Instructions | 80 |
| Validation | 30 |
| Reference link | 20 |
| **Total** | **< 200** |

### 4.4 Scripts Are the Execution Layer
- Scripts perform **ALL** real work
- Scripts may call MCP servers as APIs
- Scripts MUST return **minimal outputs only**
- Scripts MUST exit non-zero on failure
- Scripts MUST NOT require interactive input

---

## 5. MCP Code Execution Doctrine

### 5.1 Token Efficiency Mandate
- MCP is treated as a **code API**, not a conversational tool
- Filtering, transformation, and logic occur **inside scripts**
- Only distilled results may enter agent context
- Raw MCP output MUST NEVER enter context

### 5.2 Approved MCP Usage Pattern
```
┌─────────────────────────────────────────────────────────┐
│ 1. Agent loads Skill           (~100 tokens)           │
│ 2. Skill provides script path  (0 tokens)              │
│ 3. Script executes externally  (0 tokens in context)   │
│ 4. Script calls MCP server     (external)              │
│ 5. Script processes response   (external)              │
│ 6. Script outputs minimal result (~50 tokens)          │
│ 7. Agent validates exit code   (success/fail)          │
│ 8. Agent proceeds or retries                           │
└─────────────────────────────────────────────────────────┘
```

**Any deviation from this pattern is unconstitutional.**

### 5.3 MCP Server Integration
Skills may integrate with MCP servers for:
- Code execution sandboxes
- Database queries
- External API calls
- File system operations

All integrations MUST use the code execution pattern.

---

## 6. Cross-Agent Compatibility Law

### 6.1 Universal Skills
Skills MUST work on:
- ✅ Claude Code
- ✅ Goose
- ✅ Codex-compatible agents

No agent-specific hacks in SKILL.md are permitted.

### 6.2 Shared Skill Directory
- `.claude/skills/` is the **single source of truth**
- No duplication or translation of Skills allowed
- Skills must use portable shell commands
- Python scripts must use `python3`

### 6.3 Portability Requirements
| Use | Avoid |
|-----|-------|
| `#!/bin/bash` | OS-specific shebangs |
| `python3` | `python` (ambiguous) |
| Environment variables | Hardcoded paths |
| Standard CLI tools | OS-specific tools |
| JSON output | Unstructured text |

---

## 7. Infrastructure Governance

### 7.1 Kubernetes Is Mandatory
All runtime systems MUST:
- Be containerized with Docker
- Run on Kubernetes (Minikube locally, cloud for production)
- Be deployed via Helm charts or manifests
- Include health checks and probes
- Have resource limits defined

### 7.2 Event-Driven Architecture
- **Kafka** is the backbone for async communication
- Services must publish/subscribe via topics
- **Dapr** must be used for:
  - Pub/Sub abstraction
  - State management
  - Service invocation
  - Secrets management

### 7.3 Infrastructure Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| Orchestration | Kubernetes | Container management |
| Message Queue | Apache Kafka | Event streaming |
| Service Mesh | Dapr | Distributed capabilities |
| Database | PostgreSQL (Neon) | Persistent storage |
| API Gateway | Kong | Routing, auth, rate limiting |
| CI/CD | Argo CD | GitOps deployment |

### 7.4 Deployment via Skills
All infrastructure MUST be deployed using Skills:
- `kafka-k8s-setup` → Kafka deployment
- `postgres-k8s-setup` → PostgreSQL deployment
- `fastapi-dapr-agent` → Backend services
- `nextjs-k8s-deploy` → Frontend deployment
- `docusaurus-deploy` → Documentation

---

## 8. LearnFlow System Constitution

### 8.1 System Roles
| Role | Description |
|------|-------------|
| Student | Learner using the platform |
| Teacher | Content creator, progress reviewer |
| AI Tutor Agents | Autonomous tutoring services |

### 8.2 Mandatory AI Agents
The following agents MUST exist and operate autonomously:

| Agent | Purpose | Triggers |
|-------|---------|----------|
| Triage Agent | Routes queries to specialists | All incoming questions |
| Concepts Agent | Explains Python concepts | "explain", "what is" |
| Code Review Agent | Analyzes code quality | Code submissions |
| Debug Agent | Helps fix errors | Error messages, "stuck" |
| Exercise Agent | Generates challenges | "practice", "exercise" |
| Progress Agent | Tracks mastery | "progress", "summary" |

### 8.3 Agent Requirements
Each agent:
- Is **stateless** (no in-memory state)
- Is **event-driven** (Kafka pub/sub)
- Operates via **Skills and MCP context**
- Returns **minimal responses** to students
- Logs interactions for analytics

### 8.4 Learning Metrics
| Metric | Calculation |
|--------|-------------|
| Mastery Score | Exercises (40%) + Quizzes (30%) + Code Quality (20%) + Consistency (10%) |
| Struggle Detection | 3+ same errors, >10min stuck, <50% quiz, "stuck" keywords |
| Mastery Levels | Beginner (0-40%), Learning (41-70%), Proficient (71-90%), Mastered (91-100%) |

---

## 9. Validation & Truth

### 9.1 No Assumed Success
- All actions MUST be validated
- Deployment without verification is **invalid**
- Validation criteria in Skills are **binding**
- Exit code 0 = success, non-zero = failure

### 9.2 Validation Script Requirements
Every deployment skill MUST include a `verify.py` or equivalent that:
- Checks resource existence
- Validates health endpoints
- Returns minimal output
- Uses proper exit codes

### 9.3 Failure Handling Protocol
On failure, agents MUST:
1. **Inspect** validation output
2. **Retry** using the same Skill (max 3 attempts)
3. **Check** REFERENCE.md for troubleshooting
4. **Escalate** only after repeated failure with detailed context

---

## 10. Documentation Law

### 10.1 Documentation Is Executable
- Docs MUST be generated and deployed via Skills
- Docusaurus deployment is **mandatory** for projects
- README files MUST reflect agentic workflows
- No manual documentation updates

### 10.2 AGENTS.md Supremacy
Every repository MUST include `AGENTS.md` defining:
- Repository structure
- Agent expectations
- Skill usage rules
- Entry points and conventions

### 10.3 Required Documentation
| File | Purpose | Location |
|------|---------|----------|
| `AGENTS.md` | AI agent guide | Root |
| `CLAUDE.md` | Claude Code rules | Root |
| `constitution.md` | Project law | `.specify/memory/` |
| `README.md` | Human overview | Root, per skill |
| `REFERENCE.md` | Advanced skill docs | Per skill |

---

## 11. History & Records

### 11.1 Prompt History Records (PHR)
- Created for every significant interaction
- Stored in `history/prompts/<context>/`
- Pattern: `<ID>-<slug>.<stage>.prompt.md`

### 11.2 Architecture Decision Records (ADR)
- Created for significant architectural decisions
- Stored in `history/adr/`
- Pattern: `ADR-<ID>-<slug>.md`
- Require human consent before creation

### 11.3 History Structure
```
history/
├── prompts/
│   ├── constitution/    # Constitution-related
│   ├── general/         # General development
│   └── <feature>/       # Feature-specific
└── adr/                 # Architecture decisions
```

---

## 12. Evaluation Alignment

Agents MUST optimize for these criteria (per Hackathon III rubric):

| Criterion | Weight | Gold Standard |
|-----------|--------|---------------|
| Skill Autonomy | 15% | Single prompt → running K8s deployment |
| Token Efficiency | 10% | Scripts for execution, MCP wrapped |
| Cross-Agent Portability | 5% | Same skill works on Claude + Goose |
| Architecture | 20% | Correct Dapr patterns, Kafka pub/sub |
| MCP Integration | 10% | Rich context for AI debugging |
| Documentation | 10% | Docusaurus deployed via skills |
| Spec-Kit Plus | 15% | High-level specs → agentic instructions |
| LearnFlow Completion | 15% | App built entirely via skills |

---

## 13. Project Structure

```
learnflow/
├── .claude/
│   ├── skills/              # 🎯 THE PRODUCT - Reusable Skills
│   │   ├── agents-md-gen/
│   │   ├── kafka-k8s-setup/
│   │   ├── postgres-k8s-setup/
│   │   ├── fastapi-dapr-agent/
│   │   ├── mcp-code-execution/
│   │   ├── nextjs-k8s-deploy/
│   │   └── docusaurus-deploy/
│   └── commands/            # Custom slash commands
├── .specify/
│   ├── memory/
│   │   └── constitution.md  # 📜 THIS DOCUMENT
│   └── templates/           # ADR, PHR, spec templates
├── skills-library/          # Shareable skills repository
├── history/                 # PHR and ADR records
├── specs/                   # Feature specifications
├── src/                     # Application code (built by skills)
├── kubernetes/              # K8s manifests
├── AGENTS.md                # AI agent guide
├── CLAUDE.md                # Claude rules
├── guide.md                 # Developer guide
└── variables.md             # Environment variables guide
```

---

## 14. Constitutional Amendments

### 14.1 Amendment Conditions
This constitution may only be amended when:
- A new industry standard emerges (AAIF, MCP updates)
- Token efficiency can be further improved
- New evaluation criteria are added
- Critical bugs in governance are discovered

### 14.2 Amendment Process
1. Document proposed change in a PHR
2. Discuss tradeoffs and alternatives
3. Create ADR if architecturally significant
4. Update constitution with version increment
5. Update all dependent documentation

### 14.3 Preservation Clause
All amendments MUST preserve:
> **Reusability, Autonomy, and Minimal Context**

---

## 15. Final Declaration

This system exists to:

> **Stop writing code**  
> **Start teaching machines**  
> **And scale intelligence, not effort**

The Skills we create today will build many applications tomorrow.

**Any behavior violating this constitution is a bug.**

---

**Version**: 2.0  
**Ratified**: 2026-02-08  
**Status**: Active  

— End of Constitution —
