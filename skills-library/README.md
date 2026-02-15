# Skills Library: Reusable Intelligence for Agentic CLI

This library provides a collection of **Measurable Skills** that teach AI coding agents (Claude Code, Goose, Codex) how to architect, deploy, and manage distributed systems using the **MCP Code Execution** pattern.

## The Core Principle: "Tokens are Scarce"
Instead of loading massive MCP tool definitions into the agent's context, these skills wrap operations in external scripts. The agent only sees the **intent** (SKILL.md) and the **zero-token execution** (scripts/), resulting in a 90% reduction in context bloat.

## Catalog of Skills

| Skill | Purpose | Features |
|-------|---------|----------|
| `agents-md-gen` | Agent Intelligence | Generates `AGENTS.md` for project context. |
| `kafka-k8s-setup` | Event Streaming | Deploys Kafka + Zookeeper with Helm. |
| `postgres-k8s-setup` | Data Persistence | Deploys PostgreSQL and manages migrations. |
| `fastapi-dapr-agent` | Microservices | Scaffolds FastAPI services with Dapr sidecars. |
| `mcp-code-execution` | AI Patterns | Template for building new MCP-based skills. |
| `nextjs-k8s-deploy` | Frontend | Deploys Next.js in 'Standalone' mode to K8s. |
| `docusaurus-deploy` | Documentation | Deploys searchable Docusaurus sites. |
| `phase3-deploy` | Automation | Orchestrated deployment of multiple agent services. |
| `spec-governance-check`| System Compliance | Validates the entire repository against CAPS rules. |

## How to Use

1. Copy `.claude/skills/` to your repository.
2. Trigger any skill via natural language prompt (e.g., "Deploy Kafka using the library").
3. Confirm script execution and validation results.

---
**Status**: Submission Ready  
**Standard**: AAIF Reusable Intelligence  