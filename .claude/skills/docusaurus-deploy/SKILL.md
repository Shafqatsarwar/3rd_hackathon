---
name: docusaurus-deploy
description: Deploy Docusaurus documentation sites on Kubernetes
---

# Docusaurus K8s Deployment

## When to Use
- Deploying documentation sites to K8s
- Scalable documentation for LearnFlow platform

## Instructions
1. Prepare: `./scripts/prepare_site.sh <site-name>`
2. Build/Push: `./scripts/build_push_docs.sh <site-name>`
3. Deploy: `./scripts/deploy_docusaurus.sh <site-name>`
4. Verify: `python scripts/verify_site.py <site-name>`

## Validation
- [x] Site is running in K8s
- [x] Pods are in Running state
- [x] Accessible via URL

See [REFERENCE.md](./REFERENCE.md).