#!/usr/bin/env python3
"""
MCP Operation Executor
Execute MCP operations with minimal output for token efficiency

This script wraps MCP server calls and returns only essential results,
keeping the agent's context window clean.
"""
import subprocess
import json
import sys
import os
from typing import Optional, Dict, Any

def execute_mcp_operation(
    server_name: str,
    method: str,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Execute an MCP operation and return minimal results.
    
    The key insight: all data processing happens HERE, not in the agent context.
    Only the final, minimal result is returned to the agent.
    """
    params = params or {}
    
    # Construct the MCP request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }
    
    try:
        # Execute via the MCP client
        result = subprocess.run(
            ["python", "mcp_client.py", server_name, json.dumps(request)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr[:200],  # Truncate for token efficiency
                "summary": f"✗ Operation failed: {method}"
            }
        
        # Parse the raw response
        raw_response = json.loads(result.stdout)
        
        # Process and minimize the response
        return minimize_response(raw_response, method)
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Operation timed out",
            "summary": f"✗ Timeout: {method}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid response: {str(e)[:100]}",
            "summary": f"✗ Parse error: {method}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)[:200],
            "summary": f"✗ Error: {method}"
        }

def minimize_response(response: Dict[str, Any], method: str) -> Dict[str, Any]:
    """
    Minimize the MCP response to reduce token consumption.
    
    This is the key to the MCP Code Execution pattern:
    - Full data is processed in the script
    - Only summary/minimal result returns to agent
    """
    if "error" in response:
        return {
            "success": False,
            "error": str(response["error"])[:200],
            "summary": f"✗ {method} failed"
        }
    
    result = response.get("result", {})
    
    # Extract only essential information
    if isinstance(result, list):
        # For list results, return count and first few items
        count = len(result)
        sample = result[:3] if count > 3 else result
        return {
            "success": True,
            "count": count,
            "sample": sample,
            "summary": f"✓ {method}: {count} items"
        }
    elif isinstance(result, dict):
        # For dict results, return key counts
        keys = list(result.keys())[:5]
        return {
            "success": True,
            "keys": keys,
            "summary": f"✓ {method}: {len(keys)} keys"
        }
    else:
        # For simple results, return as-is if small
        result_str = str(result)
        if len(result_str) > 200:
            result_str = result_str[:200] + "..."
        return {
            "success": True,
            "result": result_str,
            "summary": f"✓ {method} completed"
        }

def main():
    """Main entry point for MCP operation execution."""
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False,
            "error": "Usage: python mcp_operation.py <server_name> <method> [params_json]",
            "summary": "✗ Invalid arguments"
        }))
        sys.exit(1)
    
    server_name = sys.argv[1]
    method = sys.argv[2]
    params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    
    result = execute_mcp_operation(server_name, method, params)
    
    # Output minimal JSON result
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result.get("success") else 1)

if __name__ == "__main__":
    main()
