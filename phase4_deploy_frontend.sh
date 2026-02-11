#!/bin/bash
set -e

APP_NAME="learnflow-frontend"
NAMESPACE="learnflow"

echo "🏗️ Phase 4: Deploying Frontend ($APP_NAME)..."

# Ensure we are in Minikube's Docker env
eval $(minikube -p minikube docker-env)

# Build Image directly in Minikube
echo "🔨 Building Docker image (this may take a few minutes)..."
cd src/frontend
docker build -t $APP_NAME:latest .
cd ../..

# Configure Deployment
echo "⚙️ Preparing Manifests..."
.claude/skills/nextjs-k8s-deploy/scripts/prepare_deployment.sh $APP_NAME $NAMESPACE

# Update deployment to use local image (Never pull)
sed -i 's/imagePullPolicy: IfNotPresent/imagePullPolicy: Never/g' deployments/$APP_NAME/deployment.yaml

# Deploy
echo "🚀 Deploying to Kubernetes..."
kubectl apply -f deployments/$APP_NAME/deployment.yaml
kubectl apply -f deployments/$APP_NAME/hpa.yaml

# Wait
echo "⏳ Waiting for rollout..."
kubectl rollout status deployment/$APP_NAME -n $NAMESPACE --timeout=300s

echo "✅ Frontend Deployed Successfully!"
kubectl get pods -n $NAMESPACE -l app=$APP_NAME
kubectl get svc -n $NAMESPACE $APP_NAME-service
