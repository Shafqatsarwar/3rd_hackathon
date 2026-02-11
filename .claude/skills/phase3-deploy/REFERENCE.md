# Phase 3 Deployment Reference

## Overview
Deploys 6 AI tutoring agents to Kubernetes with Dapr sidecars for event-driven architecture.

## Agents Deployed
1. **triage-agent** - Routes student queries to specialists
2. **concepts-agent** - Explains Python concepts
3. **debug-agent** - Helps fix code errors
4. **exercise-agent** - Generates practice challenges
5. **progress-agent** - Tracks learning progress
6. **code-review-agent** - Reviews code quality

## Architecture
```
Student Query → Triage Agent → Kafka Topic → Specialist Agent → Response
                     ↓
                Dapr Pub/Sub
                     ↓
              PostgreSQL (State)
```

## Prerequisites
- Minikube running
- Kafka deployed (3 pods in `kafka` namespace)
- PostgreSQL deployed (1 pod in `postgresql` namespace)
- Dapr installed on cluster

## Deployment Steps

### 1. Check Infrastructure
```bash
cd .claude/skills/phase3-deploy
./scripts/check_infra.sh
```

### 2. Deploy All Agents
```bash
./scripts/deploy_all_agents.sh
```

### 3. Verify Deployment
```bash
python scripts/verify_phase3.py
```

## Expected Output
```
kubectl get pods -n learnflow

NAME                              READY   STATUS    RESTARTS   AGE
triage-agent-xxx                  2/2     Running   0          2m
concepts-agent-xxx                2/2     Running   0          2m
debug-agent-xxx                   2/2     Running   0          2m
exercise-agent-xxx                2/2     Running   0          2m
progress-agent-xxx                2/2     Running   0          2m
code-review-agent-xxx             2/2     Running   0          2m
```

Each pod has 2/2 containers: application + Dapr sidecar.

## Troubleshooting

### Pods Stuck in Pending
```bash
kubectl describe pod <pod-name> -n learnflow
# Check Events section for issues
```

### ImagePullBackOff
```bash
# Check if using correct Python image
kubectl get pod <pod-name> -n learnflow -o yaml | grep image:
```

### Dapr Sidecar Not Injected
```bash
# Verify Dapr is installed
kubectl get pods -n dapr-system

# Check annotations
kubectl get deployment <agent-name> -n learnflow -o yaml | grep dapr
```

### Agent Not Responding
```bash
# Check logs
kubectl logs <pod-name> -n learnflow -c <agent-name>

# Check Dapr logs
kubectl logs <pod-name> -n learnflow -c daprd
```

## Testing Agents

### Port Forward to Agent
```bash
kubectl port-forward svc/triage-agent 8001:80 -n learnflow
```

### Test API
```bash
curl http://localhost:8001/health
curl http://localhost:8001/api/agents
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "explain Python lists"}'
```

## Cleanup
```bash
kubectl delete namespace learnflow
```

## Environment Variables
Each agent receives:
- `AGENT_NAME` - Agent identifier
- `KAFKA_BOOTSTRAP` - Kafka broker address
- `DATABASE_URL` - PostgreSQL connection string

## Resource Limits
Per agent:
- Memory: 256Mi request, 512Mi limit
- CPU: 100m request, 500m limit

## Kafka Topics (Auto-created)
- `student-queries` - Incoming questions
- `agent-responses` - Agent replies
- `progress-updates` - Learning metrics

## Next Steps (Phase 4)
After Phase 3 verification:
1. Deploy frontend with `nextjs-k8s-deploy` skill
2. Deploy documentation with `docusaurus-deploy` skill
3. Configure Kong API Gateway
4. Set up ArgoCD for GitOps

## Constitution Compliance
✅ Skills-First Development - All deployment via scripts
✅ Token Efficiency - Minimal context, execution external
✅ Autonomous - Single command deployment
✅ Event-Driven - Kafka + Dapr integration
✅ Cloud-Native - Kubernetes + containers
