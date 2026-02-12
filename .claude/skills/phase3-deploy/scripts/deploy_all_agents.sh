#!/bin/bash
set -e

AGENTS=("triage-agent" "concepts-agent" "debug-agent" "exercise-agent" "progress-agent" "code-review-agent")
NAMESPACE="learnflow"

echo "🚀 Deploying 6 AI Agents to Kubernetes (Optimized)..."

# Ensure namespace exists
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Deploy each agent
for AGENT in "${AGENTS[@]}"; do
    echo ""
    echo "📦 Deploying $AGENT..."
    
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $AGENT
  namespace: $NAMESPACE
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "$AGENT"
    dapr.io/app-port: "8000"
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $AGENT
  template:
    metadata:
      labels:
        app: $AGENT
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "$AGENT"
        dapr.io/app-port: "8000"
    spec:
      containers:
      - name: $AGENT
        image: learnflow-backend:latest
        imagePullPolicy: IfNotPresent
        env:
        - name: AGENT_NAME
          value: "$AGENT"
        - name: KAFKA_BOOTSTRAP
          value: "kafka.kafka.svc.cluster.local:9092"
        - name: DATABASE_URL
          value: "postgresql://postgres:securePassword123@postgresql.postgresql.svc.cluster.local:5432/learnflow"
        resources:
          requests:
            memory: "128Mi"
            cpu: "50m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: $AGENT
  namespace: $NAMESPACE
spec:
  selector:
    app: $AGENT
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
EOF
    
    echo "✅ $AGENT deployed"
done

echo ""
echo "⏳ Waiting for pods to stabilize..."
sleep 5

kubectl get pods -n $NAMESPACE

echo ""
echo "✅ All 6 agents deployed!"
echo "   Run: kubectl get pods -n learnflow"
