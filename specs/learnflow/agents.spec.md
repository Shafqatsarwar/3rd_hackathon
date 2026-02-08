---
type: system
scope: agents
version: 1.0
---

# LearnFlow Agent Specification

> **AI Agent System** – Defining the autonomous tutoring agents.

## Agent Architecture

LearnFlow uses a **multi-agent system** where specialized AI agents handle different aspects of tutoring. Agents are:
- Stateless
- Event-driven
- Governed by Skills
- Independently deployable

---

## Required Agents

| Agent | Purpose | Kafka Topic |
|-------|---------|-------------|
| Triage Agent | Routes queries to specialists | `learnflow.query.incoming` |
| Concepts Agent | Explains Python concepts | `learnflow.concepts.request` |
| Code Review Agent | Analyzes code quality | `learnflow.codereview.request` |
| Debug Agent | Helps fix errors | `learnflow.debug.request` |
| Exercise Agent | Generates/grades challenges | `learnflow.exercise.request` |
| Progress Agent | Tracks mastery | `learnflow.progress.request` |

---

## Agent Specifications

### Triage Agent
```yaml
name: triage-agent
purpose: Route incoming queries to appropriate specialist
triggers:
  - All incoming student messages
routing_rules:
  - "explain", "what is" → Concepts Agent
  - "error", "bug", "stuck" → Debug Agent
  - "review", "PEP 8" → Code Review Agent
  - "practice", "exercise" → Exercise Agent
  - "progress", "summary" → Progress Agent
```

### Concepts Agent
```yaml
name: concepts-agent
purpose: Explain Python concepts adaptively
triggers:
  - Routed from Triage (concept queries)
capabilities:
  - Adaptive complexity based on level
  - Code examples
  - Interactive follow-ups
output:
  - Explanation text
  - Code snippets
  - Suggested exercises
```

### Code Review Agent
```yaml
name: code-review-agent
purpose: Analyze code quality
triggers:
  - Code submission with review request
capabilities:
  - PEP 8 compliance check
  - Logic error detection
  - Efficiency suggestions
  - Readability scoring
output:
  - Quality score (0-100)
  - Issue list
  - Improvement suggestions
```

### Debug Agent
```yaml
name: debug-agent
purpose: Help students fix errors
triggers:
  - Error messages
  - "stuck" keyword
  - Multiple failed executions
capabilities:
  - Parse error messages
  - Identify root causes
  - Provide hints (not solutions)
  - Track common error patterns
output:
  - Error explanation
  - Hint (progressive disclosure)
  - Solution (only if stuck)
```

### Exercise Agent
```yaml
name: exercise-agent
purpose: Generate and grade exercises
triggers:
  - Topic completion
  - Exercise request
  - Practice command
capabilities:
  - Generate topic-specific challenges
  - Auto-grade submissions
  - Provide instant feedback
  - Adjust difficulty
output:
  - Exercise prompt
  - Test cases
  - Grade and feedback
```

### Progress Agent
```yaml
name: progress-agent
purpose: Track and report mastery
triggers:
  - After exercise completion
  - Progress request
  - Daily summary
capabilities:
  - Calculate mastery score
  - Track topic progress
  - Detect struggles
  - Recommend next steps
output:
  - Mastery score
  - Topic breakdown
  - Recommendations
```

---

## Agent Constraints

All agents MUST adhere to:

| Constraint | Requirement |
|------------|-------------|
| Statefulness | Stateless (no in-memory state) |
| Events | Event-driven (Kafka pub/sub) |
| Governance | Governed by Skills |
| Infrastructure | No direct infrastructure access |
| Context | Output < 500 tokens |
| Logging | Log all interactions |

---

## Agent Communication

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│                         ↓                                │
│                    API Gateway (Kong)                    │
│                         ↓                                │
│                    Triage Agent                          │
│              ↙     ↓     ↓     ↓     ↘                   │
│         Concepts | Review | Debug | Exercise | Progress  │
│              ↓     ↓     ↓     ↓     ↓                   │
│                    Kafka (Events)                        │
│                         ↓                                │
│                    PostgreSQL                            │
└─────────────────────────────────────────────────────────┘
```

---

## Agent Deployment

Agents are deployed via the `fastapi-dapr-agent` skill:

```bash
# Deploy each agent
./scripts/generate_service.sh triage-agent
./scripts/deploy_dapr.sh triage-agent

./scripts/generate_service.sh concepts-agent
./scripts/deploy_dapr.sh concepts-agent

# ... repeat for all agents
```

---

## Agent Testing

Each agent must pass:

1. **Unit Tests**: Function-level tests
2. **Integration Tests**: Kafka pub/sub works
3. **Autonomy Tests**: Handles queries without human help
4. **Load Tests**: Handles concurrent requests

---

**Status**: Active  
**Last Updated**: 2026-02-08
