---
name: fastapi-dapr-agent
description: Create FastAPI services with Dapr integration for microservices architecture
---

# FastAPI Dapr Agent

## When to Use
- Creating microservices with Dapr integration
- Building stateless API services
- Need for service-to-service invocation
- Requirement for state management and pub/sub

## Instructions
1. Generate service: `./scripts/generate_service.sh <service-name>`
2. Deploy with Dapr: `./scripts/deploy_dapr.sh <service-name>`
3. Verify deployment: `python scripts/verify_service.py <service-name>`

## Validation
- [ ] Service is running in Kubernetes
- [ ] Dapr sidecar is attached and healthy
- [ ] API endpoints are accessible
- [ ] Dapr components are properly configured

See [REFERENCE.md](./REFERENCE.md) for configuration options.