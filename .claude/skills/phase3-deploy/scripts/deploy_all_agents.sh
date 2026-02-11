#!/bin/bash
set -e

AGENTS=("triage-agent" "concepts-agent" "debug-agent" "exercise-agent" "progress-agent" "code-review-agent")
NAMESPACE="learnflow"
BACKEND_DIR="$(cd "$(dirname "$0")/../../.." && pwd)/src/backend"

echo "🚀 Deploying 6 AI Agents to Kubernetes..."

# Create ConfigMap from backend code
kubectl create configmap backend-code \
  --from-file=main.py="$BACKEND_DIR/main.py" \
  -n $NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy each agent
for AGENT in "${AGENTS[@]}"; do
    echo ""
    echo "📦 Deploying $AGENT..."
    
    # Create deployment manifest
    cat &lt;&lt;EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $AGENT
  namespace: $NAMESPACE
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "$AGENT"
    dapr.io/app-port: "8000"
    dapr.io/log-level: "info"
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
        image: python:3.12-slim
        command: ["/bin/bash", "-c"]
        args:
          - |
            pip install --no-cache-dir fastapi uvicorn pydantic python-dotenv httpx openai aiokafka dapr &gt; /dev/null 2&gt;&1
            cd /app
            exec uvicorn main:app --host 0.0.0.0 --port 8000
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: code
          mountPath: /app
        env:
        - name: AGENT_NAME
          value: "$AGENT"
        - name: KAFKA_BOOTSTRAP
          value: "kafka.kafka.svc.cluster.local:9092"
        - name: DATABASE_URL
          value: "postgresql://postgres:postgres@postgresql.postgresql.svc.cluster.local:5432/learnflow"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      volumes:
      - name: code
        configMap:
          name: backend-code
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
echo "⏳ Waiting for pods to be ready..."
sleep 10

kubectl get pods -n $NAMESPACE

echo ""
echo "✅ All 6 agents deployed!"
echo "   Run: kubectl get pods -n learnflow"
