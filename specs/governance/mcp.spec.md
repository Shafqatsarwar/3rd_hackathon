---
type: governance
scope: mcp
version: 1.0
---

# MCP Governance Specification

> **MCP Code Execution Doctrine** – Rules for token-efficient MCP usage.

## MCP Usage Model

MCP servers are treated as **programmatic APIs**, not conversational tools.

```
MCP Server ≠ Conversational Tool
MCP Server = Code API (accessed via scripts)
```

---

## Approved Pattern

The ONLY approved pattern for MCP usage:

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Agent loads Skill           (~100 tokens)       │
│ Step 2: Skill executes script       (0 tokens)          │
│ Step 3: Script calls MCP server     (external)          │
│ Step 4: Script filters/processes    (external)          │
│ Step 5: Script outputs minimal      (~20 tokens)        │
│ Step 6: Agent validates exit code                       │
└─────────────────────────────────────────────────────────┘

Total Context Impact: ~120 tokens
vs Direct MCP: ~50,000+ tokens
```

---

## Token Constraints

| Constraint | Requirement |
|------------|-------------|
| MCP Schemas | MUST NOT load into context |
| Raw Responses | MUST NOT enter context |
| Script Output | ≤ 20 tokens where possible |
| Tool Definitions | NEVER in agent context |

---

## MCP Integration Points

Skills may integrate with MCP for:

| Integration | Purpose |
|-------------|---------|
| Code Sandbox | Execute student code safely |
| Database | Query PostgreSQL via MCP |
| External APIs | Call third-party services |
| File System | Managed file operations |

All integrations MUST use the code execution pattern.

---

## Compliance Check

A skill is **INVALID** if it:
- Loads MCP tool definitions into context
- Returns raw MCP responses to agent
- Allows MCP data to exceed 50 tokens in context
- Uses MCP interactively (conversationally)

---

## MCP Script Template

```python
#!/usr/bin/env python3
"""MCP Integration Script - Returns minimal output"""
import json
import sys

def call_mcp(server: str, method: str, params: dict):
    # Call MCP server (implementation varies)
    response = mcp_client.call(server, method, params)
    
    # CRITICAL: Filter and minimize response
    return minimize(response)

def minimize(data):
    """Reduce MCP response to essential info only"""
    if isinstance(data, list):
        return {"count": len(data), "sample": data[:2]}
    elif isinstance(data, dict):
        return {"keys": list(data.keys())[:5]}
    else:
        return {"value": str(data)[:100]}

if __name__ == "__main__":
    result = call_mcp(sys.argv[1], sys.argv[2], {})
    print(json.dumps(result))  # Minimal output
```

---

## Token Efficiency Proof

| Approach | Token Cost |
|----------|------------|
| Direct MCP (5 tools) | ~50,000 tokens |
| Skills + Scripts | ~150 tokens |
| **Savings** | **99.7%** |

---

**Status**: Active  
**Last Updated**: 2026-02-08
