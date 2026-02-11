---
name: phase3-deploy
description: Deploy all 6 AI agents to Kubernetes with Dapr sidecars
---

# Phase 3 Deployment - AI Agents

## When to Use
- Deploying LearnFlow AI tutoring agents
- Setting up event-driven microservices
- Phase 3 of hackathon project

## Instructions
1. Ensure infrastructure: `./scripts/check_infra.sh`
2. Deploy all agents: `./scripts/deploy_all_agents.sh`
3. Verify deployment: `python scripts/verify_phase3.py`

## Validation
- [ ] 6 agent pods running (2/2 containers each)
- [ ] Dapr sidecars healthy
- [ ] Kafka topics created
- [ ] API endpoints accessible

See [REFERENCE.md](./REFERENCE.md) for troubleshooting.
