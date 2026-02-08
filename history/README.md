# History Directory

This directory maintains the complete history of architectural decisions, development prompts, and project evolution for the LearnFlow Agentic AI Platform.

## Structure

```
history/
├── prompts/                    # Prompt History Records (PHR)
│   ├── constitution/           # Constitution-related discussions
│   ├── general/                # General development prompts
│   └── <feature-name>/         # Feature-specific prompts
└── adr/                        # Architecture Decision Records
```

## Purpose

### Prompt History Records (PHR)
Capture every significant interaction during development:
- **Implementation work**: Code changes, new features
- **Planning/architecture**: Design discussions
- **Debugging sessions**: Problem-solving traces
- **Spec/task/plan creation**: Documentation evolution
- **Multi-step workflows**: Complex development sequences

### Architecture Decision Records (ADR)
Document significant architectural decisions:
- Long-term consequences for architecture/platform/security
- Multiple viable options with tradeoffs considered
- Cross-cutting concerns that influence system design

## File Naming Conventions

### PHR Files
```
<ID>-<slug>.<stage>.prompt.md
```
- **ID**: Auto-incrementing integer
- **slug**: 3-7 word descriptive title
- **stage**: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

### ADR Files
```
ADR-<ID>-<slug>.md
```
- **ID**: Auto-incrementing integer
- **slug**: Descriptive title of the decision

## Usage

PHRs are created automatically after each significant development interaction. ADRs require explicit consent before creation - the agent will suggest when one is needed.

---

**Maintained by**: AI Agents (Claude Code, Goose) + Human Developers
