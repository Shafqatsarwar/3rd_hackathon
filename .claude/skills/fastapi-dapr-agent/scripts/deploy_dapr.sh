#!/bin/bash
# Deploy FastAPI service with Dapr sidecar to Kubernetes

set -e

SERVICE_NAME=${1:-"my-service"}
NAMESPACE=${2:-"learnflow"}
SERVICE_PORT=${3:-8000}

echo "Deploying $SERVICE_NAME with Dapr to Kubernetes..."

# Ensure namespace exists
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Create Kubernetes deployment with Dapr annotations
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $SERVICE_NAME
  namespace: $NAMESPACE
  labels:
    app: $SERVICE_NAME
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $SERVICE_NAME
  template:
    metadata:
      labels:
        app: $SERVICE_NAME
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "$SERVICE_NAME"
        dapr.io/app-port: "$SERVICE_PORT"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
      - name: $SERVICE_NAME
        image: $SERVICE_NAME:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: $SERVICE_PORT
        livenessProbe:
          httpGet:
            path: /health
            port: $SERVICE_PORT
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: $SERVICE_PORT
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: $SERVICE_NAME
  namespace: $NAMESPACE
spec:
  selector:
    app: $SERVICE_NAME
  ports:
  - port: 80
    targetPort: $SERVICE_PORT
  type: ClusterIP
EOF

echo "✓ $SERVICE_NAME deployed with Dapr sidecar"
echo "  Namespace: $NAMESPACE"
echo "  Next: Run 'python scripts/verify_service.py $SERVICE_NAME' to verify"
