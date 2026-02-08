#!/bin/bash
# Docusaurus Site Preparation Script

if [ $# -eq 0 ]; then
    echo "Usage: $0 <site-name> [namespace]"
    exit 1
fi

SITE_NAME=$1
NAMESPACE=${2:-default}

echo "Preparing Docusaurus site deployment for: $SITE_NAME in namespace: $NAMESPACE"

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Create deployment directory structure
mkdir -p deployments/$SITE_NAME

# Create Dockerfile template
cat > deployments/$SITE_NAME/Dockerfile << EOF
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
EOF

# Create nginx configuration
cat > deployments/$SITE_NAME/nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Enable gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    server {
        listen 80;
        root /usr/share/nginx/html;
        index index.html;

        # Serve static files with proper caching
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Handle client-side routing for SPA
        location / {
            try_files \$uri \$uri/ /index.html;
        }
    }
}
EOF

# Create Kubernetes deployment manifest
cat > deployments/$SITE_NAME/deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $SITE_NAME
  namespace: $NAMESPACE
  labels:
    app: $SITE_NAME
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $SITE_NAME
  template:
    metadata:
      labels:
        app: $SITE_NAME
    spec:
      containers:
      - name: $SITE_NAME
        image: $SITE_NAME:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "250m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: $SITE_NAME-service
  namespace: $NAMESPACE
spec:
  selector:
    app: $SITE_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: $SITE_NAME-ingress
  namespace: $NAMESPACE
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: $SITE_NAME-service
            port:
              number: 80
EOF

# Create HPA manifest
cat > deployments/$SITE_NAME/hpa.yaml << EOF
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: $SITE_NAME-hpa
  namespace: $NAMESPACE
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: $SITE_NAME
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 75
EOF

echo "✓ Docusaurus site preparation completed for $SITE_NAME"
echo "✓ Created Dockerfile in deployments/$SITE_NAME/"
echo "✓ Created nginx configuration in deployments/$SITE_NAME/"
echo "✓ Created Kubernetes manifests in deployments/$SITE_NAME/"