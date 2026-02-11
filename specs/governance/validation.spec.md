---
type: governance
scope: validation
version: 1.0
---

# Validation Specification

> **Truth & Verification** – Rules for validating all agent actions.

## Validation Mandate

> **No execution is valid without verification.**

This is an absolute rule. Every action MUST be validated.

---

## Validation Principle

```
Execution without Validation = Invalid
Absence of Errors ≠ Success
Only Positive Confirmation = Success
```

---

## Validation Sources

| Source | What It Validates |
|--------|-------------------|
| Kubernetes Status | Pod state, deployment health |
| Health Endpoints | Service availability |
| Kafka Topics | Topic existence, connectivity |
| Database | Schema existence, connectivity |
| Exit Codes | Script success/failure |

---

## Invalid Assumptions

These assumptions are **FORBIDDEN**:

| ❌ Invalid Assumption | ✅ Valid Approach |
|-----------------------|-------------------|
| "Deployment succeeded" (no check) | Run `kubectl get pods` and verify Running |
| "Service is up" (no check) | Hit health endpoint and verify 200 |
| "No errors = success" | Explicitly verify expected state |
| "Command returned" = done | Check exit code is 0 |

---

## Output Rules

Validation output MUST be:

| Property | Requirement |
|----------|-------------|
| Deterministic | Same input → same output |
| Minimal | ≤ 50 tokens |
| Machine-Verifiable | Exit code 0 = pass, non-zero = fail |
| Structured | Consistent format |

---

## Validation Output Format

### Success Format
```
✓ <resource>: <status summary>
```
Example: `✓ kafka: 3/3 pods running`

### Failure Format
```
✗ <resource>: <error summary>
  - Detail 1
  - Detail 2
```
Example:
```
✗ kafka: 1/3 pods running
  - kafka-0: CrashLoopBackOff
  - kafka-1: ImagePullBackOff
```

---

## Validation Script Template

```python
#!/usr/bin/env python3
"""Validation script - minimal output"""
import subprocess
import sys

def validate():
    checks = []
    
    # Check 1: Pods running
    result = subprocess.run(
        ["kubectl", "get", "pods", "-l", "app=kafka", "-o", "json"],
        capture_output=True, text=True
    )
    pods_ok = result.returncode == 0
    checks.append(("pods", pods_ok))
    
    # Check 2: Service exists
    result = subprocess.run(
        ["kubectl", "get", "svc", "kafka"],
        capture_output=True, text=True
    )
    svc_ok = result.returncode == 0
    checks.append(("service", svc_ok))
    
    # Report minimal result
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    
    if passed == total:
        print(f"✓ kafka: {passed}/{total} checks passed")
        sys.exit(0)
    else:
        print(f"✗ kafka: {passed}/{total} checks passed")
        for name, ok in checks:
            if not ok:
                print(f"  - {name}: failed")
        sys.exit(1)

if __name__ == "__main__":
    validate()
```

---

## Validation Integration

Every skill MUST include validation:

```yaml
## Validation (in SKILL.md)
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

And a validation script:
```
scripts/verify.py  # Automated validation
```

---

## Validation Frequency

| Trigger | Action |
|---------|--------|
| After deployment | Run verify.py immediately |
| After retry | Re-validate |
| Before reporting success | Final validation |
| On failure | Validate to confirm failure |

---

## Compliance Checklist

- [ ] Every skill has verify.py (or equivalent)
- [ ] Validation runs automatically
- [ ] Output is minimal (≤ 50 tokens)
- [ ] Exit codes are correct
- [ ] No assumed success

---

**Status**: Active  
**Last Updated**: 2026-02-08
