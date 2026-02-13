---
name: mcp-code-execution
description: MCP with code execution pattern for token efficiency
---

# MCP Code Execution Pattern

## When to Use
- Connecting agents to external systems efficiently
- Reducing context window consumption from tools
- Script-based execution for complex tasks

## Instructions
1. Run setup: `./scripts/setup_mcp.sh`
2. Create client: `python scripts/create_client.py`
3. Execute operations: `python scripts/mcp_operation.py`

## Validation
- [x] MCP server is running and accessible
- [x] Token consumption is reduced by 80%+

See [REFERENCE.md](./REFERENCE.md).