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
echo "Deploying Kafka cluster..."
helm upgrade --install kafka bitnami/kafka \
  --namespace kafka \
  --set image.tag=3.9.0 \
  --set replicaCount=1 \
  --set zookeeper.enabled=true \
  --set zookeeper.replicaCount=1 \
  --set persistence.enabled=true \
  --set persistence.size=5Gi \
  --set resources.limits.cpu=1000m \
  --set resources.limits.memory=1Gi \
  --set resources.requests.cpu=500m \
  --set resources.requests.memory=512Mi \
  --wait

# Wait for pods to be ready
echo "Waiting for Kafka pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kafka -n kafka --timeout=300s

echo "✓ Kafka deployed to namespace 'kafka'"