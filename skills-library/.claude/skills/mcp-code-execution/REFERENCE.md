# MCP Code Execution Reference

## Overview
This reference guide provides detailed information about implementing the MCP (Model Context Protocol) code execution pattern for token-efficient AI agent operations.

## The Token Problem
Direct MCP tool calls consume significant token space:
- Tool definitions in context: 10,000-15,000 tokens
- Data transfer: Variable based on operation size
- Result processing: Additional token overhead

## The Solution Pattern
Wrap MCP operations in scripts that execute externally:
- SKILL.md: Load instructions (~100 tokens)
- scripts/: Execute operations (0 tokens loaded)
- Minimal output: Only essential results (~50-100 tokens)

## Advanced Configuration Options

### MCP Server Setup
```bash
# Start MCP server
mcp-server --port 8080 --config ./mcp-config.json

# Verify server is running
curl http://localhost:8080/health
```

### Client Wrapper Patterns
```python
# Example client wrapper
import subprocess
import json

def execute_mcp_operation(operation_data):
    # Execute operation via script
    result = subprocess.run(
        ['python', 'scripts/mcp_executor.py'],
        input=json.dumps(operation_data),
        capture_output=True,
        text=True
    )

    # Return minimal result
    return json.loads(result.stdout)
```

### Token Optimization Strategies
1. **Filter Early**: Process data in scripts before returning
2. **Summarize Results**: Return summaries instead of full datasets
3. **Batch Operations**: Combine multiple operations in one script
4. **Lazy Loading**: Load detailed data only when explicitly requested

## Best Practices
- Always return minimal, essential information to agent context
- Use structured output formats (JSON) for consistency
- Implement proper error handling in scripts
- Log detailed operations separately from agent context
- Validate operations before execution