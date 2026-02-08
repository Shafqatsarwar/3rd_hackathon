# Skills Library for LearnFlow

> **Hackathon III**: Reusable Intelligence and Cloud-Native Mastery  
> **Philosophy**: The skills are the product - applications are demonstrations of their power.

This repository contains a collection of reusable skills that enable AI coding agents (Claude Code and Goose) to build and deploy the LearnFlow AI-powered Python tutoring platform.

---

## Overview

The skills in this library follow the **MCP Code Execution pattern** to achieve maximum token efficiency and autonomous operation. Each skill consists of:

| Component | Purpose | Token Cost |
|-----------|---------|------------|
| `SKILL.md` | Instructions loaded into agent context | ~100 tokens |
| `scripts/` | Executable code (runs outside context) | 0 tokens |
| `REFERENCE.md` | Advanced docs (loaded on-demand) | 0 tokens |

---

## Skills Included

| Skill | Purpose | Scripts | Status |
|-------|---------|---------|--------|
| `agents-md-gen` | Generate AGENTS.md files for AI agents | 1 | ✅ Ready |
| `kafka-k8s-setup` | Deploy Apache Kafka on Kubernetes | 2 | ✅ Ready |
| `postgres-k8s-setup` | Deploy PostgreSQL on Kubernetes | 3 | ✅ Ready |
| `fastapi-dapr-agent` | Create FastAPI + Dapr microservices | 3 | ✅ Ready |
| `mcp-code-execution` | MCP with code execution pattern | 3 | ✅ Ready |
| `nextjs-k8s-deploy` | Deploy Next.js on Kubernetes | 4 | ✅ Ready |
| `docusaurus-deploy` | Deploy Docusaurus documentation | 4 | ✅ Ready |

**Total: 7 skills, 20 scripts**

---

## Skill Details

### agents-md-gen
Generate AGENTS.md files that help AI agents understand repository structure.
```bash
./scripts/generate_agents_md.sh
```

### kafka-k8s-setup
Deploy Apache Kafka on Kubernetes using Helm.
```bash
./scripts/deploy.sh
python scripts/verify.py
```

### postgres-k8s-setup
Deploy PostgreSQL on Kubernetes with migrations.
```bash
./scripts/deploy.sh
./scripts/migrate.sh
python scripts/verify.py
```

### fastapi-dapr-agent
Create FastAPI microservices with Dapr integration (state, pub/sub, invocation).
```bash
./scripts/generate_service.sh <service-name>
./scripts/deploy_dapr.sh <service-name>
python scripts/verify_service.py <service-name>
```

### mcp-code-execution
Implement the MCP Code Execution pattern for token efficiency.
```bash
./scripts/setup_mcp.sh
python scripts/create_client.py
python scripts/mcp_operation.py <server> <method> [params]
```

### nextjs-k8s-deploy
Deploy Next.js applications on Kubernetes.
```bash
./scripts/prepare_deployment.sh <app-name>
./scripts/build_push_image.sh <app-name>
./scripts/deploy_nextjs.sh <app-name>
python scripts/verify_deployment.py <app-name>
```

### docusaurus-deploy
Deploy Docusaurus documentation sites on Kubernetes.
```bash
./scripts/prepare_site.sh <site-name>
./scripts/build_push_docs.sh <site-name>
./scripts/deploy_docusaurus.sh <site-name>
python scripts/verify_site.py <site-name>
```

---

## Token Efficiency

This library demonstrates the dramatic token savings of the Skills + Code Execution pattern:

```
┌─────────────────────────────────────────────────────────────┐
│ BEFORE (Direct MCP)           │ AFTER (Skills + Scripts)    │
├───────────────────────────────┼─────────────────────────────┤
│ Tool definitions: ~15,000     │ SKILL.md: ~100 tokens       │
│ Data transfer: ~25,000+       │ Script execution: 0 tokens  │
│ Result processing: ~10,000    │ Minimal result: ~50 tokens  │
├───────────────────────────────┼─────────────────────────────┤
│ TOTAL: ~50,000+ tokens        │ TOTAL: ~150 tokens          │
│                               │ SAVINGS: 99.7%              │
└─────────────────────────────────────────────────────────────┘
```

---

## Usage

AI agents use these skills to autonomously build the LearnFlow platform:

1. **Trigger**: Agent detects need for a capability (e.g., "deploy Kafka")
2. **Load**: Agent reads SKILL.md (~100 tokens)
3. **Execute**: Agent runs scripts (0 context tokens)
4. **Validate**: Agent checks completion against checklist
5. **Report**: Minimal result returned to context

### Example Flow
```
User: "Deploy Kafka on Kubernetes"

Agent: Loading kafka-k8s-setup skill...
Agent: Running ./scripts/deploy.sh
       ✓ Kafka deployed to namespace 'kafka'
Agent: Running python scripts/verify.py
       ✓ All 3 pods running
Agent: Validation complete. Kafka is ready.
```

---

## Cross-Agent Compatibility

All skills work on both **Claude Code** and **Goose**:

- Use `.claude/skills/` directory (read by both)
- YAML frontmatter follows industry standard
- Scripts use portable shell + Python
- Results are structured and minimal

---

## Development

### Creating a New Skill

1. Create directory: `.claude/skills/<skill-name>/`
2. Create `SKILL.md` (< 200 tokens):
   ```yaml
   ---
   name: skill-name
   description: Brief description
   ---
   # Skill Title
   ## When to Use
   ## Instructions
   ## Validation
   ```
3. Create `scripts/` with executable scripts
4. Create `REFERENCE.md` for advanced docs
5. Test with Claude Code AND Goose

### Skill Requirements

- [x] SKILL.md under 200 tokens
- [x] Scripts execute outside context window
- [x] Scripts return minimal output
- [x] Validation checklist included
- [x] Works on Claude Code + Goose
- [x] REFERENCE.md for advanced options

See [docs/skill-development-guide.md](docs/skill-development-guide.md) for detailed guide.

---

## Project Structure

```
skills-library/
├── .claude/skills/
│   ├── agents-md-gen/
│   │   ├── SKILL.md
│   │   ├── REFERENCE.md
│   │   └── scripts/
│   ├── kafka-k8s-setup/
│   ├── postgres-k8s-setup/
│   ├── fastapi-dapr-agent/
│   ├── mcp-code-execution/
│   ├── nextjs-k8s-deploy/
│   └── docusaurus-deploy/
├── docs/
│   └── skill-development-guide.md
└── README.md
```

---

## License

MIT

---

*Last Updated: 2026-02-08 | Skills: 7 | Scripts: 20 | All skills validated and ready.*