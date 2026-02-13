#!/bin/bash
# PostgreSQL Kubernetes Deployment Script

echo "Starting PostgreSQL deployment on Kubernetes..."

# Add the Bitnami Helm repository
echo "Adding Bitnami Helm repository..."
# Bypass Windows credential helper in WSL to avoid .exe format errors
export DOCKER_CONFIG="/tmp/helm-docker-config-$(date +%s)"
mkdir -p $DOCKER_CONFIG
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create namespace if it doesn't exist
echo "Creating postgresql namespace..."
kubectl create namespace postgresql --dry-run=client -o yaml | kubectl apply -f -

# Deploy PostgreSQL using Helm with optimized settings
echo "Deploying PostgreSQL (Deep-Dive Optimized)..."
helm upgrade --install postgresql bitnami/postgresql \
  --namespace postgresql \
  --set global.security.allowInsecureImages=true \
  --set image.registry=public.ecr.aws \
  --set image.repository=bitnami/postgresql \
  --set auth.postgresPassword=securePassword123 \
  --set auth.database=learnflow \
  --set architecture=standalone \
  --set primary.persistence.enabled=false \
  --set primary.resources.limits.cpu=500m \
  --set primary.resources.limits.memory=512Mi \
  --set primary.resources.requests.cpu=100m \
  --set primary.resources.requests.memory=256Mi \
  --set primary.service.ports.postgresql=5432 \
  --timeout 900s \
  --wait

# Wait for pods with a long timeout and verify status
echo "Waiting for PostgreSQL pod to be ready (up to 15 minutes)..."
if kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=postgresql -n postgresql --timeout=900s; then
  echo "✓ PostgreSQL successfully deployed and READY"
else
  echo "✗ PostgreSQL deployment FAILED (Timeout/State issues)"
  kubectl describe pod -l app.kubernetes.io/name=postgresql -n postgresql | tail -n 20
  exit 1
fi