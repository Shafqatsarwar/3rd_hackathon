#!/bin/bash
set -e

echo "🔄 Monitoring Minikube status..."

# Wait for Minikube to be ready
until minikube status | grep -q "Running"; do
    echo "⏳ Minikube is not running. Starting..."
    minikube start --driver=docker
    sleep 10
done

echo "✅ Minikube is UP!"

echo "🚀 Deploying Phase 3 (AI Agents)..."
cd .claude/skills/phase3-deploy/
./scripts/deploy_all_agents.sh || echo "⚠️ Phase 3 deploy warning (check logs)"

echo "🏗️ Building & Deploying Phase 4 (Frontend)..."
cd ../nextjs-k8s-deploy/
./scripts/prepare_deployment.sh learnflow-frontend learnflow
./scripts/build_push_image.sh learnflow-frontend local latest
./scripts/deploy_nextjs.sh learnflow-frontend learnflow

echo "✅ All Deployments Complete!"
echo "Check pods with: kubectl get pods -A"
