# Hackathon III: Master Submission Guide 🏆

This repository is structured into four distinct deliverables, each serving a unique purpose in the **AAIF (Agentic AI Framework)** ecosystem. Follow this guide to build, deploy, and present the system.

---

## 1. Project Architecture (The Four-Repo Structure)

| Component | Location | Role |
|-----------|----------|------|
| **LearnFlow App** | `src/` | AI-Powered Tutoring Dashboard (FastAPI + Next.js). |
| **Skills Library** | `.claude/skills/` | 9 Reusable Intelligence skills for autonomous CLI action. |
| **CAPS Library** | `specs/` | The Governance Layer (Constitution, Agents, Product, Specs). |
| **Spec-Kit Plus** | `.specify/` | The SDD-RI Engine (Automation, PHRs, ADRs). |

---

## 2. Quick Start (Build & Run)

### Prerequisites
- **Minikube**: Running with 2200MB+ RAM.
- **Docker**: Desktop or WSL integration enabled.
- **PowerShell 7+**: For Spec-Kit automation.

### App Deployment (LearnFlow)
Run the orchestrated deployment script:
```bash
# Deploys Infrastructure (Kafka/Postgres) and 6 Backend Agents
./deploy_infra_wsl.sh
./deploy_phase2.sh
./skills/phase3-deploy/scripts/deploy_all_agents.sh

# Deploy Frontend
cd src/frontend
docker build -t learnflow-frontend:latest .
kubectl apply -f deployment.yml
```

### Accessing the Interface
```bash
# Bridge the Backend
kubectl port-forward svc/triage-agent 8000:80 -n learnflow --address 0.0.0.0 &

# Bridge the Frontend
kubectl port-forward svc/learnflow-frontend 3000:80 -n learnflow --address 0.0.0.0
```
Visit: [http://localhost:3000](http://localhost:3000)

---

## 3. Presentation Guides (90-Second Videos)

### Video 1: The LearnFlow Application
- **Focus**: Show the chat interface.
- **Key Demo**: Ask a coding question and show the Triage-Agent routing to the Concepts-Agent.
- **Highlight**: "System Online" green status and Dapr sidecar integration.

### Video 2: The Skills Library
- **Focus**: `mcp-code-execution` pattern.
- **Key Demo**: Show `.claude/skills/` directory. Run `python verify.py` in one of the skills.
- **Highlight**: 90% reduction in context bloat via "Intent-Execution" separation.

### Video 3: CAPS Library (Governance)
- **Focus**: Spec-Driven Development.
- **Key Demo**: Open `specs/governance/system.spec.md` (Supreme Spec).
- **Highlight**: Automated compliance checking via `validate_repo.py`.

### Video 4: Spec-Kit Plus (The Engine)
- **Focus**: Developer Experience (DX).
- **Key Demo**: Run `./.specify/scripts/powershell/update-agent-context.ps1`.
- **Highlight**: Automatic synchronization of memory files (`CLAUDE.md`, etc.) across multiple agents.

---

## 4. Maintenance & Extensions
All automation scripts are located in `.specify/scripts/`. For full documentation on each deliverable, refer to the individual `README.md` files in their respective folders.

---
**Status**: Ready for Submission  
**Standard**: AAIF Reusable Intelligence & Cloud-Native Mastery  
