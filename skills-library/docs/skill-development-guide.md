# Skill Development Guide

> **Complete guide for creating token-efficient, autonomous skills for AI coding agents.**

This guide covers the principles and practices for creating effective skills that work on both Claude Code and Goose.

---

## The Token Problem

Direct MCP (Model Context Protocol) connections consume enormous context space:

| MCP Servers Connected | Token Cost BEFORE Conversation |
|----------------------|-------------------------------|
| 1 server (5 tools)   | ~10,000 tokens               |
| 3 servers (15 tools) | ~30,000 tokens               |
| 5 servers (25 tools) | ~50,000+ tokens              |

**With 5 MCP servers, you've consumed 25% of your context window before typing a single prompt!**

---

## The Solution: Skills + Code Execution

Instead of loading MCP tools directly, wrap them in Skills that execute scripts:

### Token Consumption Comparison

| Component | Direct MCP | Skills + Code Execution |
|-----------|------------|------------------------|
| Instructions | ~15,000 tokens | ~100 tokens |
| Data Transfer | ~25,000+ tokens | 0 tokens (external) |
| Results | ~10,000 tokens | ~50-100 tokens |
| **Total** | **~50,000+ tokens** | **~150-200 tokens** |

**Result: 99.7% token savings**

---

## Skill Structure

Every skill follows this structure:

```
.claude/skills/<skill-name>/
├── SKILL.md              # Instructions (~100 tokens) - ALWAYS LOADED
├── REFERENCE.md          # Deep docs (loaded on-demand) - OPTIONAL LOAD
└── scripts/
    ├── main_action.sh    # Primary executable
    ├── verify.py         # Validation script
    └── helper.py         # Supporting scripts
```

---

## Phase 1: Specification

### SKILL.md Template

```yaml
---
name: skill-name
description: Brief one-line description (< 100 chars)
---

# Skill Title

## When to Use
- Specific trigger condition 1
- Specific trigger condition 2
- Context that indicates this skill is needed

## Instructions
1. Step 1: `./scripts/action.sh [args]`
2. Step 2: `python scripts/verify.py [args]`
3. Step 3: Confirm validation passes

## Validation
- [ ] Success criterion 1
- [ ] Success criterion 2
- [ ] Success criterion 3

See [REFERENCE.md](./REFERENCE.md) for advanced configuration.
```

### Token Budget

| Section | Max Tokens |
|---------|------------|
| YAML frontmatter | 20 |
| Title + When to Use | 50 |
| Instructions | 80 |
| Validation | 30 |
| REFERENCE link | 20 |
| **Total** | **< 200** |

---

## Phase 2: Implementation

### Script Design Principles

1. **Execute OUTSIDE context** - All heavy lifting happens in scripts
2. **Minimal output** - Return only essential results
3. **Structured output** - Use consistent format (JSON or simple text)
4. **Error handling** - Graceful failures with clear messages
5. **Exit codes** - 0 = success, non-zero = failure

### Script Template (Shell)

```bash
#!/bin/bash
# Script description
# Returns minimal output for token efficiency

set -e

# Parse arguments
ARG_NAME=${1:-"default"}

echo "Starting operation..."

# Do the actual work (details stay in script, not context)
# ... complex operations here ...

# Return minimal result
if [ $? -eq 0 ]; then
    echo "✓ Operation complete: $ARG_NAME"
else
    echo "✗ Operation failed: $ARG_NAME"
    exit 1
fi
```

### Script Template (Python)

```python
#!/usr/bin/env python3
"""
Script description
Returns minimal output for token efficiency
"""
import subprocess
import json
import sys

def main():
    arg_name = sys.argv[1] if len(sys.argv) > 1 else "default"
    
    # Do the work (outside context)
    # ... complex operations ...
    
    # Return minimal result
    result = {
        "success": True,
        "summary": f"✓ {arg_name}: operation complete"
    }
    print(json.dumps(result))
    sys.exit(0 if result["success"] else 1)

if __name__ == "__main__":
    main()
```

### Output Guidelines

| ✅ Good Output | ❌ Bad Output |
|----------------|--------------|
| `✓ Kafka: 3/3 pods running` | Full kubectl JSON output |
| `✓ Deploy complete: service-name` | Helm install verbose logs |
| `{"success": true, "count": 5}` | Entire API response body |

---

## Phase 3: Validation

### Testing Checklist

1. **Claude Code Test**
   ```
   # Single prompt → completion
   "Deploy Kafka on Kubernetes"
   
   # Expected: Agent loads skill, runs scripts, reports result
   ```

2. **Goose Test**
   ```
   # Same prompt, same result
   "Deploy Kafka on Kubernetes"
   ```

3. **Token Efficiency Test**
   - SKILL.md < 200 tokens
   - Script output < 100 characters
   - Total context impact < 300 tokens

4. **Autonomy Test**
   - [ ] Agent completes without asking questions
   - [ ] No manual intervention required
   - [ ] Validation checklist passes automatically

### Validation Script Template

```python
#!/usr/bin/env python3
"""Minimal verification script"""
import subprocess
import sys

def main():
    # Check conditions
    checks = []
    
    # Check 1
    result = subprocess.run(["kubectl", "get", "pods"], capture_output=True)
    checks.append(("pods", result.returncode == 0))
    
    # Check 2
    # ... more checks ...
    
    # Report minimal result
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    
    if passed == total:
        print(f"✓ All {total} checks passed")
        sys.exit(0)
    else:
        print(f"✗ {total - passed}/{total} checks failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Phase 4: Documentation

### REFERENCE.md Template

```markdown
# Skill Name - Reference Documentation

## Overview
Detailed description of what this skill does and how it works.

## Configuration Options
- Option 1: Description
- Option 2: Description

## Advanced Usage
### Custom Parameters
```bash
./scripts/deploy.sh --custom-flag value
```

### Integration with Other Skills
This skill works with:
- skill-a: For X functionality
- skill-b: For Y functionality

## Troubleshooting
| Problem | Solution |
|---------|----------|
| Issue 1 | Fix 1 |
| Issue 2 | Fix 2 |

## Architecture Details
[Detailed technical information...]
```

### Update Requirements

After creating a skill, update:
1. `skills-library/README.md` - Add to skills table
2. `docs/skill-development-guide.md` - If new patterns discovered
3. Parent project documentation as needed

---

## Cross-Agent Compatibility

### Directory Convention
```
.claude/skills/    ← Used by Claude Code
                   ← Also read by Goose
```

### YAML Frontmatter
```yaml
---
name: lowercase-with-dashes
description: Under 100 characters
---
```

### Script Portability

| Use | Avoid |
|-----|-------|
| `#!/bin/bash` | OS-specific shebangs |
| `python3` | `python` (ambiguous) |
| Standard CLI tools | OS-specific tools |
| Environment variables | Hardcoded paths |

---

## Quality Checklist

Before marking a skill as "Ready":

- [ ] **SKILL.md** under 200 tokens
- [ ] **Trigger conditions** are specific and clear
- [ ] **Instructions** are numbered and actionable
- [ ] **Validation checklist** has 3-5 criteria
- [ ] **Scripts** execute outside context
- [ ] **Output** is minimal (< 100 chars typical)
- [ ] **Exit codes** are correct (0=success)
- [ ] **REFERENCE.md** covers advanced options
- [ ] **Tested** on Claude Code
- [ ] **Tested** on Goose (if available)
- [ ] **Added** to skills-library README

---

## Examples

### Minimal Skill (agents-md-gen)
- SKILL.md: 24 lines, ~100 tokens
- Scripts: 1 (generate_agents_md.sh)
- Validation: 4 criteria
- **Result**: Single prompt → AGENTS.md created

### Full Skill (fastapi-dapr-agent)
- SKILL.md: 25 lines, ~120 tokens
- Scripts: 3 (generate, deploy, verify)
- Validation: 4 criteria
- **Result**: Single prompt → Service running with Dapr

---

## Common Patterns

### Resource Creation Pattern
```
1. Generate configuration → generate.sh
2. Apply to cluster → deploy.sh
3. Verify success → verify.py
```

### Build & Deploy Pattern
```
1. Prepare files → prepare.sh
2. Build image → build.sh
3. Deploy → deploy.sh
4. Verify → verify.py
```

### Integration Pattern
```
1. Setup connection → setup.sh
2. Create client → create_client.py
3. Execute operations → operation.py
```

---

*Last Updated: 2026-02-08*