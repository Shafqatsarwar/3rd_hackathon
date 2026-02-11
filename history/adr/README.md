# Architecture Decision Records (ADR)

This directory contains all Architecture Decision Records for the LearnFlow project.

## Purpose

ADRs document significant architectural decisions that:

1. **Have long-term impact** on architecture, platform, or security
2. **Consider multiple alternatives** with documented tradeoffs
3. **Affect cross-cutting concerns** (not isolated implementation details)

## ADR Lifecycle

```
Proposed → Accepted → [Superseded | Deprecated]
```

- **Proposed**: Decision is being discussed
- **Accepted**: Decision is adopted and in effect
- **Superseded**: Replaced by a newer ADR
- **Deprecated**: No longer relevant but kept for history

## When to Create an ADR

Before creating an ADR, run the **Significance Test**:

- [ ] **Impact**: Does this have long-term consequences?
- [ ] **Alternatives**: Were multiple viable options considered?
- [ ] **Scope**: Is this a cross-cutting concern?

If ALL three are true → Create an ADR  
If any are false → Document in a PHR instead

## Template

ADR template: `.specify/templates/adr-template.md`

## Naming Convention

```
ADR-<ID>-<slug>.md
```

Example: `ADR-001-skills-first-architecture.md`

## Current ADRs

| ID | Title | Status | Date |
|----|-------|--------|------|
| - | - | - | - |

*ADRs will be listed here as they are created.*

---

**Process**: ADRs are NEVER auto-created. The AI agent suggests when one is needed, and human consent is required before creation.
