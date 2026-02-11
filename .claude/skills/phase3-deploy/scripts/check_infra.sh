#!/bin/bash
set -e

echo "🔍 Checking infrastructure..."

# Check Minikube
if ! minikube status &gt; /dev/null 2>&1; then
    echo "❌ Minikube not running. Starting..."
    minikube start --driver=docker
fi

# Check Kafka
KAFKA_PODS=$(kubectl get pods -n kafka 2&gt;/dev/null | grep -c "Running" || echo "0")
if [ "$KAFKA_PODS" -lt 1 ]; then
    echo "❌ Kafka not running. Deploy with: cd .claude/skills/kafka-k8s-setup && ./scripts/deploy.sh"
    exit 1
fi

# Check PostgreSQL
POSTGRES_PODS=$(kubectl get pods -n postgresql 2&gt;/dev/null | grep -c "Running" || echo "0")
if [ "$POSTGRES_PODS" -lt 1 ]; then
    echo "❌ PostgreSQL not running. Deploy with: cd .claude/skills/postgres-k8s-setup && ./scripts/deploy.sh"
    exit 1
fi

# Create namespace
kubectl create namespace learnflow --dry-run=client -o yaml | kubectl apply -f -

echo "✅ Infrastructure ready"
echo "   Kafka pods: $KAFKA_PODS"
echo "   PostgreSQL pods: $POSTGRES_PODS"
