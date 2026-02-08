---
name: mcp-code-execution
description: MCP with code execution pattern for token-efficient AI agent operations
---

# MCP Code Execution Pattern

## When to Use
- When connecting AI agents to external systems without token bloat
- Need to reduce context window consumption from MCP tools
- Want to execute complex operations with minimal agent context impact
- Moving from direct MCP calls to script-based execution

## Instructions
1. Run the MCP setup: `./scripts/setup_mcp.sh`
2. Create MCP client wrapper: `python scripts/create_client.py`
3. Execute MCP operations via scripts: `python scripts/mcp_operation.py`
4. Return minimal results to maintain token efficiency

## Validation
- [ ] MCP server is running and accessible
- [ ] Client wrapper script executes without errors
- [ ] Operations return minimal results to agent context
- [ ] Token consumption is reduced by 80%+

See [REFERENCE.md](./REFERENCE.md) for advanced configuration options.