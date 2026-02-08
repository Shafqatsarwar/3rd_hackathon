---
type: governance
scope: architecture
version: 1.0
---

# Architecture Specification

> **Cloud-Native Enforcement** – Mandatory architectural patterns.

## Runtime Platform

| Requirement | Specification |
|-------------|---------------|
| Orchestration | Kubernetes (mandatory) |
| Local Development | Minikube |
| Containerization | All services must be containerized |
| Image Registry | Local or cloud registry |

---

## Communication Model

```
┌─────────────────────────────────────────────────────────┐
│                    Communication Layer                   │
├─────────────────────────────────────────────────────────┤
│  Async Events:     Apache Kafka                         │
│  Service Mesh:     Dapr                                 │
│  Coupling:         No point-to-point hard coupling      │
└─────────────────────────────────────────────────────────┘
```

### Kafka Requirements
- All async communication via Kafka topics
- Topic naming: `learnflow.<domain>.<event>`
- At-least-once delivery semantics
- Schema registry for event schemas

### Dapr Requirements
| Component | Purpose |
|-----------|---------|
| Pub/Sub | Abstract Kafka access |
| State Store | Managed state (Redis/PostgreSQL) |
| Service Invocation | Service-to-service calls |
| Secrets | Secure secret management |

---

## Service Rules

| Rule | Requirement |
|------|-------------|
| Statefulness | Services are **stateless** |
| State Management | Via Dapr or external DB only |
| Shared Memory | ❌ Forbidden |
| Shared Filesystem | ❌ Forbidden |
| Health Checks | Required for all services |

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Orchestration | Kubernetes | Container management |
| Service Mesh | Dapr | Distributed capabilities |
| Message Queue | Apache Kafka | Event streaming |
| Database | PostgreSQL (Neon) | Persistent storage |
| API Gateway | Kong | Routing, auth, rate limiting |
| CI/CD | Argo CD | GitOps deployment |
| Frontend | Next.js | UI framework |
| Backend | FastAPI | API framework |

---

## Deployment Rules

| Rule | Requirement |
|------|-------------|
| Method | Helm charts or K8s manifests |
| Manual kubectl | ❌ Forbidden (must use Skills) |
| Resource Limits | Required on all pods |
| Probes | Liveness + readiness required |
| Namespacing | Logical separation required |

---

## Deployment Skills Mapping

| Infrastructure | Skill |
|----------------|-------|
| Kafka | `kafka-k8s-setup` |
| PostgreSQL | `postgres-k8s-setup` |
| Backend Services | `fastapi-dapr-agent` |
| Frontend | `nextjs-k8s-deploy` |
| Documentation | `docusaurus-deploy` |

---

## Network Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Ingress (Kong)                      │
├──────────────────────┬──────────────────────────────────┤
│      Frontend        │           Backend APIs           │
│    (Next.js)         │         (FastAPI + Dapr)         │
├──────────────────────┴──────────────────────────────────┤
│                     Kafka (Events)                       │
├─────────────────────────────────────────────────────────┤
│               PostgreSQL (Persistence)                   │
└─────────────────────────────────────────────────────────┘
```

---

## Compliance Checklist

- [ ] All services containerized
- [ ] Running on Kubernetes
- [ ] Dapr sidecars attached
- [ ] Kafka for async events
- [ ] No manual kubectl usage
- [ ] Health probes configured
- [ ] Resource limits set

---

**Status**: Active  
**Last Updated**: 2026-02-08
