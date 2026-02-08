#!/bin/bash
# Next.js Kubernetes Deployment Script

if [ $# -eq 0 ]; then
    echo "Usage: $0 <app-name> [namespace]"
    exit 1
fi

APP_NAME=$1
NAMESPACE=${2:-default}

echo "Deploying Next.js application: $APP_NAME to namespace: $NAMESPACE"

# Apply the deployment
echo "Applying deployment configuration..."
kubectl apply -f deployments/$APP_NAME/deployment.yaml

# Apply the HPA
echo "Applying Horizontal Pod Autoscaler..."
kubectl apply -f deployments/$APP_NAME/hpa.yaml

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/$APP_NAME -n $NAMESPACE --timeout=300s

# Scale to initial replica count
kubectl scale deployment $APP_NAME --replicas=2 -n $NAMESPACE

echo "✓ Next.js application $APP_NAME deployed successfully to namespace $NAMESPACE"

# Show deployment status
echo ""
echo "Deployment Status:"
kubectl get deployment $APP_NAME -n $NAMESPACE -o wide

echo ""
echo "Service Status:"
kubectl get service $APP_NAME-service -n $NAMESPACE -o wide

echo ""
echo "HPA Status:"
kubectl get hpa $APP_NAME-hpa -n $NAMESPACE -o wide