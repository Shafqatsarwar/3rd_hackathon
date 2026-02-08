---
type: governance
scope: autonomy
version: 1.0
---

# Autonomy Specification

> **Autonomy Scoring Logic** – Measuring and enforcing agent autonomy.

## Autonomy Levels

| Level | Name | Description |
|-------|------|-------------|
| 0 | Human-Driven | Human writes code, agent assists |
| 1 | Assisted | Agent suggests, human approves each step |
| 2 | Multi-Step Autonomous | Agent completes multi-step tasks |
| 3 | Single-Prompt-to-Deployment | One prompt → running system |

---

## Required Level

```
┌─────────────────────────────────────────────────────────┐
│            AUTONOMY REQUIREMENTS                        │
├─────────────────────────────────────────────────────────┤
│  Minimum acceptable level:  Level 2                     │
│  Target level:              Level 3                     │
│  Gold standard:             Single prompt → K8s deploy  │
└─────────────────────────────────────────────────────────┘
```

---

## Level 3 Definition

A Level 3 autonomous system can:

1. **Parse** a single prompt (e.g., "Deploy Kafka on Kubernetes")
2. **Select** the appropriate skill
3. **Execute** all scripts
4. **Validate** success
5. **Report** minimal result

**Without any human intervention.**

---

## Autonomy Violations

The following constitute autonomy violations:

| Violation | Description | Penalty |
|-----------|-------------|---------|
| Manual Fixes | Human corrects script errors | Level drops to 1 |
| Manual Retries | Human re-runs failed commands | Level drops to 1 |
| Human Validation | Human checks if deployment worked | Level drops to 2 |
| Inline Debugging | Agent asks for help mid-execution | Level drops to 1 |

---

## Expected Agent Behavior

### On Success
```
1. Execute skill
2. Run validation
3. Report: "✓ Operation complete"
4. Exit code: 0
```

### On Failure
```
1. Inspect validation output
2. Re-run validation (confirm failure)
3. Retry skill (max 3 attempts)
4. If still failing: Escalate with context
```

### Escalation Format
```
✗ Operation failed after 3 attempts
  Skill: kafka-k8s-setup
  Error: Pod not entering Running state
  Last output: CrashLoopBackOff
  Suggestion: Check resource limits
```

---

## Autonomy Scoring

| Criteria | Points |
|----------|--------|
| Zero human intervention | +40 |
| Self-validation | +20 |
| Self-retry on failure | +20 |
| Minimal context output | +10 |
| Cross-agent compatible | +10 |
| **Total** | **100** |

### Score Interpretation
| Score | Level | Status |
|-------|-------|--------|
| 90-100 | Level 3 | ✅ Compliant |
| 70-89 | Level 2 | ⚠️ Acceptable |
| 50-69 | Level 1 | ❌ Needs improvement |
| < 50 | Level 0 | ❌ Non-compliant |

---

## Autonomy Test Script

To verify autonomy level:

```bash
# Test: Single prompt → deployment
echo "Deploy Kafka on Kubernetes" | claude --skill kafka-k8s-setup

# Expected: No human interaction required
# Output: "✓ Kafka: 3/3 pods running"
```

---

## Anti-Patterns

| Pattern | Why It's Bad |
|---------|--------------|
| "What should I do next?" | Agent should know from skill |
| "Please verify the deployment" | Agent should self-verify |
| Waiting for human approval | Skill should define approval |
| Outputting full logs | Violates minimal output rule |

---

**Status**: Active  
**Last Updated**: 2026-02-08
