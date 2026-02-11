---
type: governance
priority: supreme
version: 1.0
---

# System Governance Specification

> **Supreme Spec** – Defines immutable rules governing all agentic behavior.

## Objective

Define immutable rules governing all agentic behavior, execution patterns, and architectural decisions.

---

## Governing Principles

| # | Principle | Description |
|---|-----------|-------------|
| 1 | Skills are Primary | Skills are the primary executable unit |
| 2 | Maximize Autonomy | Agents must maximize autonomy |
| 3 | Tokens are Scarce | Context tokens are a scarce resource |
| 4 | Code Executes | Execution happens in code, not context |

---

## Non-Negotiables

These rules cannot be violated under any circumstances:

- ❌ **No manual application coding** – Agents build via Skills
- ❌ **No direct MCP tool loading** – MCP accessed via scripts only
- ❌ **No unvalidated execution** – All actions require verification
- ❌ **No agent-specific skill divergence** – Skills work on all agents

---

## Success Definition

A compliant system can:

- ✅ Build, deploy, and validate infrastructure from a **single prompt**
- ✅ Operate with **minimal context usage** (< 300 tokens per operation)
- ✅ Execute **identically** across Claude Code and Goose
- ✅ Self-verify and self-correct without human intervention

---

## Failure Definition

Any of the following constitutes **system failure**:

| Failure Type | Description |
|--------------|-------------|
| Human Intervention | Manual fixes, retries, or validation required |
| Context Bloat | Large outputs (logs, JSON, manifests) in context |
| Direct MCP Loading | MCP tools loaded into agent context |
| Skipped Validation | Execution assumed successful without checks |

---

## Compliance Verification

To verify system compliance:

1. Run `spec-governance-check` skill
2. Verify all skills have validation scripts
3. Confirm token usage < 300 per operation
4. Test on both Claude Code and Goose

---

**Status**: Active  
**Last Updated**: 2026-02-08
