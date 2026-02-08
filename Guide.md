# LearnFlow Developer Guide

> **Quick Start**: Build an AI-powered Python tutoring platform using Skills-First Development.  
> AI agents (Claude Code + Goose) build the application - you teach them with skills.

---

## Overview

LearnFlow is a **Hackathon III** project demonstrating **Reusable Intelligence and Cloud-Native Mastery**. 

**Key Concept**: The skills are the product, not the application code.

| Component | Purpose |
|-----------|---------|
| Skills Library | Reusable AI agent skills (`.claude/skills/`) |
| LearnFlow App | AI tutoring platform (built by skills) |
| Governance | Constitution + Specs + AGENTS.md + SKILLS.md |

**Tech Stack**: Kubernetes • Dapr • Kafka • PostgreSQL • FastAPI • Next.js • Kong • ArgoCD

---
## 1. Local Development (Windows - No K8s)
### Frontend Only
```bash
cd src/frontend
npm install
npm run dev # Open: http://localhost:3000
```
### Backend Only
```bash
cd src/backend
python -m venv venv # uv venv
venv\Scripts\activate # .venv\Scripts\activate
pip install -r requirements.txt # uv sync
uvicorn main:app --reload --port 8000 # API: http://localhost:8000
```
### Both Together
```bash
# Terminal 1 - Backend
cd src/backend && uvicorn main:app --reload --port 8000
# Terminal 2 - Frontend
cd src/frontend && npm run dev
```

### Kill Process (if needed)
```bash
taskkill /F /IM uvicorn.exe /T
```
## 2. Governance Files

| File | Purpose | Location |
|------|---------|----------|
| `constitution.md` | Strategic law | `.specify/memory/` |
| `specs/governance/*` | Machine-readable rules | `specs/` |
| `AGENTS.md` | Agent behavioral contract | Root |
| `SKILLS.md` | Skill execution contract | Root |

**Read order for agents**: SKILLS.md → AGENTS.md → specs → constitution

---

## 3. Phase Execution Commands

### Prerequisites Check
```bash
# Windows (PowerShell)
minikube version          # Kubernetes local cluster
docker --version          # Container runtime
helm version             # K8s package manager
kubectl version          # K8s CLI
python --version         # Python 3.10+
node --version           # Node.js 18+

# WSL/Ubuntu
which minikube docker helm kubectl python3 node
```

---

## Phase 1: Foundation & Skills Setup (Windows/WSL)

### 1.1 Governance Validation
```bash
# Windows
cd D:\Panaverse\projects\3rd_hackathon
python .claude\skills\spec-governance-check\scripts\validate_repo.py

# Expected output:
# [OK] Governance check passed OR [FAIL] with issues list
```

### 1.2 Generate AGENTS.md (if needed)
```bash
# WSL/Ubuntu
cd ~/.../3rd_hackathon
bash .claude/skills/agents-md-gen/scripts/generate_agents_md.sh
```

### 1.3 Verify Skills Structure
```bash
# Windows
dir /b .claude\skills

# Expected: 8 skills
# agents-md-gen, docusaurus-deploy, fastapi-dapr-agent, kafka-k8s-setup
# mcp-code-execution, nextjs-k8s-deploy, postgres-k8s-setup, spec-governance-check
```

---

## Phase 2: Infrastructure Setup (WSL Required)

### 2.1 Start Minikube Cluster
```bash
# WSL/Ubuntu
minikube start --cpus=4 --memory=8192 --driver=docker

# Verify cluster
kubectl cluster-info
minikube status
```

### 2.2 Deploy Kafka
```bash
cd .claude/skills/kafka-k8s-setup
./scripts/deploy.sh
python scripts/verify.py

# Expected: "✓ kafka: 3/3 pods running"
```

### 2.3 Deploy PostgreSQL
```bash
cd .claude/skills/postgres-k8s-setup
./scripts/deploy.sh
./scripts/migrate.sh
python scripts/verify.py

# Expected: "✓ postgres: Connection successful"
```

### 2.4 Verify Infrastructure
```bash
kubectl get pods -A | grep -E "(kafka|postgres)"

# All pods should be Running
```

---

## Phase 3: Backend Services

### 3.1 Create Triage Agent Service
```bash
cd .claude/skills/fastapi-dapr-agent
./scripts/generate_service.sh triage-agent
./scripts/deploy_dapr.sh triage-agent
python scripts/verify_service.py triage-agent
```

### 3.2 Create Other Agents
```bash
# Repeat for each agent
./scripts/generate_service.sh concepts-agent
./scripts/deploy_dapr.sh concepts-agent

./scripts/generate_service.sh debug-agent
./scripts/deploy_dapr.sh debug-agent

./scripts/generate_service.sh exercise-agent
./scripts/deploy_dapr.sh exercise-agent

./scripts/generate_service.sh progress-agent
./scripts/deploy_dapr.sh progress-agent

./scripts/generate_service.sh code-review-agent
./scripts/deploy_dapr.sh code-review-agent
```

### 3.3 Verify All Services
```bash
kubectl get pods -n learnflow | grep agent
# All pods should be Running with 2/2 (includes Dapr sidecar)
```

---

## Phase 4: Frontend Deployment

### 4.1 Prepare Next.js Deployment
```bash
cd .claude/skills/nextjs-k8s-deploy
./scripts/prepare_deployment.sh learnflow-frontend
./scripts/build_push_image.sh learnflow-frontend
./scripts/deploy_nextjs.sh learnflow-frontend
python scripts/verify_deployment.py learnflow-frontend
```

### 4.2 Access Frontend (Local)
```bash
# Port forward to local machine
kubectl port-forward svc/learnflow-frontend 3000:80 -n learnflow

# Open browser: http://localhost:3000
```

### 4.3 OR use Minikube Service
```bash
minikube service learnflow-frontend -n learnflow --url
# Opens directly in browser
```

---

## Phase 5: Documentation Deployment

### 5.1 Deploy Docusaurus Site
```bash
cd .claude/skills/docusaurus-deploy
./scripts/prepare_site.sh learnflow-docs
./scripts/build_push_docs.sh learnflow-docs
./scripts/deploy_docusaurus.sh learnflow-docs
python scripts/verify_site.py learnflow-docs
```

### 5.2 Access Documentation
```bash
kubectl port-forward svc/learnflow-docs 8080:80 -n learnflow
# Open: http://localhost:8080
```

---

## Troubleshooting

### Governance Issues
| Problem | Solution |
|---------|----------|
| Score < 90 | Check issues list, fix token limits or add verify scripts |
| Missing specs | Run `dir specs\governance` to verify files exist |
| Path issues | Run from project root directory |

### Minikube Issues
| Problem | Solution |
|---------|----------|
| Won't start | `minikube delete && minikube start --driver=docker` |
| Driver error | Ensure Docker Desktop is running with WSL integration |
| Resources | Increase: `--cpus=4 --memory=8192` |

### Kubernetes Issues
| Problem | Solution |
|---------|----------|
| Pods Pending | `kubectl describe pod <name>` - check Events |
| ImagePullBackOff | Verify image name, check registry access |
| CrashLoopBackOff | `kubectl logs <pod> --previous` for errors |
| Service inaccessible | Verify selector matches pod labels |

### Skill Issues
| Problem | Solution |
|---------|----------|
| Script permission denied | WSL: `chmod +x scripts/*.sh` |
| Python script fails | Ensure `kubectl` in PATH, cluster running |
| Skill not found | Verify `.claude/skills/<name>/SKILL.md` exists |

---

## Quick Reference

### Governance Check
```bash
python .claude\skills\spec-governance-check\scripts\validate_repo.py
```

### View All Skills
```bash
# Windows
dir /b .claude\skills

# WSL
ls .claude/skills/
```

### Check Cluster Status
```bash
kubectl get pods -A
minikube status
```

### Access Services
```bash
kubectl port-forward svc/<service> <local-port>:<service-port> -n learnflow
```

---

## Key Files

| File | Purpose |
|------|---------|
| `SKILLS.md` | Skill index & execution contract |
| `AGENTS.md` | Agent behavioral contract |
| `constitution.md` | Project governance law |
| `specs/governance/*` | Machine-readable rules |
| `guide.md` | This file |
| `variables.md` | Environment variables |

---

**Version**: 2.0  
**Last Updated**: 2026-02-08  
**Governance Score**: 76/100
