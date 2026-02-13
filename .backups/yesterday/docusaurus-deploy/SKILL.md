---
name: docusaurus-deploy
description: Deploy Docusaurus documentation sites on Kubernetes with proper configuration and scaling
---

# Docusaurus Kubernetes Deployment

## When to Use
- Deploying Docusaurus documentation sites to Kubernetes
- Need for scalable, containerized documentation deployments
- Production-ready documentation site setup
- Auto-generated documentation for LearnFlow platform

## Instructions
1. Prepare deployment: `./scripts/prepare_site.sh <site-name>`
2. Build and push image: `./scripts/build_push_docs.sh <site-name>`
3. Deploy to Kubernetes: `./scripts/deploy_docusaurus.sh <site-name>`
4. Verify deployment: `python scripts/verify_site.py <site-name>`

## Validation
- [ ] Docusaurus site is running in Kubernetes
- [ ] Pods are in Running state
- [ ] Site is accessible via LoadBalancer/Ingress
- [ ] All documentation pages are loading correctly

See [REFERENCE.md](./REFERENCE.md) for configuration options.
