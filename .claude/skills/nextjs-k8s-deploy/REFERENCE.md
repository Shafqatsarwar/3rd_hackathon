# Next.js Kubernetes Deployment Reference

## Overview
This reference guide provides detailed information about deploying Next.js applications on Kubernetes with optimal configuration for production use.

## Deployment Configuration

### Environment Variables
```yaml
NEXT_PUBLIC_API_URL: "http://backend-service:8000"
NEXT_TELEMETRY_DISABLED: "1"
PORT: "3000"
```

### Resource Requirements
- CPU: Minimum 250m, Limit 1000m
- Memory: Minimum 256Mi, Limit 1Gi
- Storage: For static assets and build cache

### Scaling Configuration
```yaml
# Horizontal Pod Autoscaler
minReplicas: 2
maxReplicas: 10
targetCPUUtilizationPercentage: 70
targetMemoryUtilizationPercentage: 80
```

## Advanced Configuration Options

### Dockerfile Template
```dockerfile
FROM node:18-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS builder
WORKDIR /app
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
COPY --from=base /app/node_modules ./node_modules
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

### Kubernetes Manifests
The deployment includes:
- Deployment with proper resource limits
- Service for internal communication
- Ingress for external access
- ConfigMap for environment variables
- Horizontal Pod Autoscaler for scaling

## Best Practices
- Use multi-stage Docker builds for smaller images
- Implement proper health checks
- Configure appropriate resource limits
- Use persistent volumes for build cache
- Enable gzip compression for static assets
- Set up proper CORS policies
- Implement SSL termination at ingress level