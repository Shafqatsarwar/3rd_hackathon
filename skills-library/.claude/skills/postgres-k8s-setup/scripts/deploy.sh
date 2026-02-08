#!/bin/bash
# PostgreSQL Kubernetes Deployment Script

echo "Starting PostgreSQL deployment on Kubernetes..."

# Add the Bitnami Helm repository
echo "Adding Bitnami Helm repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create namespace if it doesn't exist
echo "Creating postgresql namespace..."
kubectl create namespace postgresql --dry-run=client -o yaml | kubectl apply -f -

# Deploy PostgreSQL using Helm with secure defaults
echo "Deploying PostgreSQL..."
helm install postgresql bitnami/postgresql \
  --namespace postgresql \
  --set auth.postgresPassword=securePassword123 \
  --set auth.database=learnflow \
  --set architecture=standalone \
  --set primary.persistence.enabled=true \
  --set primary.persistence.size=10Gi \
  --set primary.resources.limits.cpu=1000m \
  --set primary.resources.limits.memory=1Gi \
  --set primary.resources.requests.cpu=250m \
  --set primary.resources.requests.memory=256Mi \
  --set primary.service.ports.postgresql=5432

# Wait for pods to be ready
echo "Waiting for PostgreSQL pod to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=postgresql -n postgresql --timeout=300s

echo "✓ PostgreSQL deployed to namespace 'postgresql'"