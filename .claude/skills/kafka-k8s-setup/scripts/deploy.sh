#!/bin/bash
# Kafka Kubernetes Deployment Script

echo "Starting Kafka deployment on Kubernetes..."

# Add the Bitnami Helm repository
echo "Adding Bitnami Helm repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create namespace if it doesn't exist
echo "Creating kafka namespace..."
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# Deploy Kafka using Helm
echo "Deploying Kafka cluster (Deep-Dive Optimized)..."
helm upgrade --install kafka bitnami/kafka \
  --namespace kafka \
  --set global.security.allowInsecureImages=true \
  --set image.registry=public.ecr.aws \
  --set image.repository=bitnami/kafka \
  --set replicaCount=1 \
  --set controller.replicaCount=1 \
  --set zookeeper.enabled=false \
  --set persistence.enabled=false \
  --set resources.limits.cpu=500m \
  --set resources.limits.memory=600Mi \
  --set resources.requests.cpu=100m \
  --set resources.requests.memory=384Mi \
  --timeout 900s \
  --wait

# Wait for pods with a long timeout and verify status
echo "Waiting for Kafka pod to be ready (up to 15 minutes)..."
if kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kafka -n kafka --timeout=900s; then
  echo "✓ Kafka successfully deployed and READY"
else
  echo "✗ Kafka deployment FAILED (Timeout/State issues)"
  kubectl describe pod -l app.kubernetes.io/name=kafka -n kafka | tail -n 20
  exit 1
fi