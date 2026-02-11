# Prompt History Records (PHR)

This directory contains all Prompt History Records for the LearnFlow project.

## Organization

PHRs are organized by context:

| Directory | Purpose |
|-----------|---------|
| `constitution/` | Constitution creation, amendments, governance discussions |
| `general/` | General development prompts not tied to a specific feature |
| `<feature-name>/` | Feature-specific development (created per-feature) |

## PHR Stages

Each PHR is tagged with a development stage:

| Stage | Description |
|-------|-------------|
| `constitution` | Project principles and governance |
| `spec` | Feature specification work |
| `plan` | Architecture and planning |
| `tasks` | Task breakdown and estimation |
| `red` | Test-first development (failing tests) |
| `green` | Implementation to pass tests |
| `refactor` | Code improvement without behavior change |
| `explainer` | Documentation and explanation |
| `misc` | Miscellaneous development work |
| `general` | General prompts not tied to features |

## Template Location

PHR template: `.specify/templates/phr-template.prompt.md`

---

**Auto-generated**: PHRs are created automatically by AI agents after each interaction.
