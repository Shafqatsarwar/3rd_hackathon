---
name: kafka-k8s-setup
description: Deploy Apache Kafka on Kubernetes with proper configuration and verification
---

# Kafka Kubernetes Setup

## When to Use
- User asks to deploy Kafka on Kubernetes
- Setting up event-driven microservices architecture
- Need for message queuing and stream processing

## Instructions
1. Run deployment: `./scripts/deploy.sh`
2. Verify status: `python scripts/verify.py`
3. Confirm all pods Running before proceeding

## Validation
- [ ] All pods in Running state
- [ ] Can create test topic
- [ ] Kafka is accessible from other services

See [REFERENCE.md](./REFERENCE.md) for configuration options.