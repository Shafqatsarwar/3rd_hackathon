#!/bin/bash
# Docusaurus Kubernetes Deployment Script

if [ $# -eq 0 ]; then
    echo "Usage: $0 <site-name> [namespace]"
    exit 1
fi

SITE_NAME=$1
NAMESPACE=${2:-default}

echo "Deploying Docusaurus site: $SITE_NAME to namespace: $NAMESPACE"

# Apply the deployment
echo "Applying deployment configuration..."
kubectl apply -f deployments/$SITE_NAME/deployment.yaml

# Apply the HPA
echo "Applying Horizontal Pod Autoscaler..."
kubectl apply -f deployments/$SITE_NAME/hpa.yaml

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/$SITE_NAME -n $NAMESPACE --timeout=300s

echo "✓ Docusaurus site $SITE_NAME deployed successfully to namespace $NAMESPACE"

# Show deployment status
echo ""
echo "Deployment Status:"
kubectl get deployment $SITE_NAME -n $NAMESPACE -o wide

echo ""
echo "Service Status:"
kubectl get service $SITE_NAME-service -n $NAMESPACE -o wide

echo ""
echo "HPA Status:"
kubectl get hpa $SITE_NAME-hpa -n $NAMESPACE -o wide