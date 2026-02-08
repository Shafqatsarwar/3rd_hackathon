---
name: postgres-k8s-setup
description: Deploy PostgreSQL on Kubernetes with proper configuration and verification
---

# PostgreSQL Kubernetes Setup

## When to Use
- User asks to deploy PostgreSQL on Kubernetes
- Need for persistent data storage
- Setting up database for microservices

## Instructions
1. Run deployment: `./scripts/deploy.sh`
2. Verify status: `python scripts/verify.py`
3. Run migrations: `./scripts/migrate.sh` if needed
4. Confirm database is ready before proceeding

## Validation
- [ ] All pods in Running state
- [ ] Database is accessible
- [ ] Connection test successful

See [REFERENCE.md](./REFERENCE.md) for configuration options.