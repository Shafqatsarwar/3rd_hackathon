# Docusaurus Kubernetes Deployment Reference

## Overview
This reference guide provides detailed information about deploying Docusaurus documentation sites on Kubernetes with optimal configuration for production use.

## Deployment Configuration

### Environment Variables
```yaml
NODE_ENV: "production"
GENERATE_SOURCEMAP: "false"
BUILD_DIR: "/app/build"
```

### Resource Requirements
- CPU: Minimum 128m, Limit 512m
- Memory: Minimum 256Mi, Limit 512Mi
- Storage: For static assets and build cache

### Scaling Configuration
```yaml
# Horizontal Pod Autoscaler
minReplicas: 1
maxReplicas: 5
targetCPUUtilizationPercentage: 75
```

## Advanced Configuration Options

### Dockerfile Template
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine AS production
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Kubernetes Manifests
The deployment includes:
- Deployment with proper resource limits
- Service for internal communication
- Ingress for external access
- ConfigMap for nginx configuration
- Horizontal Pod Autoscaler for scaling

## Best Practices
- Pre-build documentation in the container image
- Use nginx for serving static content efficiently
- Implement proper caching headers
- Configure gzip compression for assets
- Set up custom domain and SSL certificates
- Monitor site availability and performance
- Implement proper error pages