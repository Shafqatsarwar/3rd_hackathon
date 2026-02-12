#!/bin/bash
# Phase 2 Deployment Script - LearnFlow Infrastructure

echo "🚀 Starting Phase 2 Infrastructure Recovery..."

# 1. Start Minikube if not running
if ! ./minikube-linux-amd64 status | grep -q "Running"; then
    echo "📦 Starting Minikube..."
    ./minikube-linux-amd64 start --driver=docker --memory=3072 --cpus=2
else
    echo "✅ Minikube is already running."
fi

# 2. Cleanup old namespaces
echo "🧹 Cleaning up old namespaces..."
kubectl delete ns kafka postgresql learnflow --ignore-not-found=true

# 3. Deploy Kafka
echo "🎡 Deploying Kafka..."
bash .claude/skills/kafka-k8s-setup/scripts/deploy.sh

# 4. Deploy PostgreSQL
echo "🐘 Deploying PostgreSQL..."
bash .claude/skills/postgres-k8s-setup/scripts/deploy.sh

# 5. Final Verification
echo "🔍 Verifying Infrastructure Health..."
python3 .claude/skills/kafka-k8s-setup/scripts/verify.py
python3 .claude/skills/postgres-k8s-setup/scripts/verify.py

echo "✨ Phase 2 Infrastructure is READY!"
