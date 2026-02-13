---
name: nextjs-k8s-deploy
description: Deploy Next.js applications on Kubernetes
---

# Next.js K8s Deployment

## When to Use
- Deploying frontend applications to K8s
- Scalable Next.js deployments
- Integration with backend services

## Instructions
1. Prepare: `./scripts/prepare_deployment.sh <app-name>`
2. Build/Push: `./scripts/build_push_image.sh <app-name>`
3. Deploy: `./scripts/deploy_nextjs.sh <app-name>`
4. Verify: `python scripts/verify_deployment.py <app-name>`

## Validation
- [x] Application is running in K8s
- [x] Pods are in Running state
- [x] Health checks passing

See [REFERENCE.md](./REFERENCE.md).