---
name: nextjs-k8s-deploy
description: Deploy Next.js applications on Kubernetes with proper configuration and scaling
---

# Next.js Kubernetes Deployment

## When to Use
- Deploying Next.js frontend applications to Kubernetes
- Need for scalable, containerized Next.js deployments
- Production-ready Next.js application setup
- Integration with backend services in Kubernetes

## Instructions
1. Prepare deployment: `./scripts/prepare_deployment.sh <app-name>`
2. Build and push image: `./scripts/build_push_image.sh <app-name>`
3. Deploy to Kubernetes: `./scripts/deploy_nextjs.sh <app-name>`
4. Verify deployment: `python scripts/verify_deployment.py <app-name>`

## Validation
- [ ] Next.js application is running in Kubernetes
- [ ] Pods are in Running state
- [ ] Service is accessible via LoadBalancer/Ingress
- [ ] Health checks are passing

See [REFERENCE.md](./REFERENCE.md) for configuration options.
