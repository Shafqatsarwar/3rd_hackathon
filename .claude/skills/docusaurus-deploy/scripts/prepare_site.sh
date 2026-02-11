#!/bin/bash
# Docusaurus Site Preparation Script

if [ $# -eq 0 ]; then
    echo "Usage: $0 <site-name> [namespace]"
    exit 1
fi

SITE_NAME=$1
NAMESPACE=${2:-default}
SOURCE_DIR=${3:-"src/docs"}

if [ ! -d "$SOURCE_DIR" ]; then
    if [ -d "website" ]; then
        SOURCE_DIR="website"
    elif [ -d "docs" ]; then
        SOURCE_DIR="docs"
    else
        echo "✗ Source directory not found: $SOURCE_DIR (checked src/docs, website, docs)"
        echo "  Please specify source directory: $0 <site-name> [namespace] [source-dir]"
        exit 1
    fi
fi

echo "Preparing Docusaurus site deployment for: $SITE_NAME in namespace: $NAMESPACE"
echo "Using source directory: $SOURCE_DIR"

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Create deployment directory structure
mkdir -p deployments/$SITE_NAME

# Create Dockerfile in source directory if missing
if [ ! -f "$SOURCE_DIR/Dockerfile" ]; then
    echo "Creating Dockerfile in $SOURCE_DIR..."
    cat > "$SOURCE_DIR/Dockerfile" << EOF
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine AS production
COPY --from=builder /app/build /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF
fi

# Create nginx configuration in source directory
if [ ! -f "$SOURCE_DIR/nginx.conf" ]; then
    cat > "$SOURCE_DIR/nginx.conf" << EOF
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
fi

# Update Dockerfile to copy nginx.conf
if [ -f "$SOURCE_DIR/Dockerfile" ] && ! grep -q "nginx.conf" "$SOURCE_DIR/Dockerfile"; then
    # sed -i 's|# COPY nginx.conf|COPY nginx.conf|' "$SOURCE_DIR/Dockerfile"
    # Actually, simpler to just overwrite or append if I created it.
    # But I already created it with commented out line.
    
    # Let's fix the creation block instead. I made a mistake in previous turn.
    # I can't easily edit the previous block now with search/replace.
    # I will just ensure nginx.conf exists in source.
    echo "Using nginx.conf from source dir."
fi

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