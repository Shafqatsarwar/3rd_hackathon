# Environment Variables Guide

> Complete guide for managing environment variables in the LearnFlow project.

---

## 1. Getting Variables

### Where to Get API Keys

| Variable | Source | URL |
|----------|--------|-----|
| `OPENAI_API_KEY` | OpenAI Platform | https://platform.openai.com/api-keys |
| `ANTHROPIC_API_KEY` | Anthropic Console | https://console.anthropic.com/settings/keys |
| `GEMINI_API_KEY` | Google AI Studio | https://aistudio.google.com/app/apikey |
| `DATABASE_URL` | Neon Console | https://console.neon.tech/ |
| `BETTER_AUTH_SECRET` | Generate locally | `openssl rand -base64 32` |

### Generate Secrets Locally

```bash
# Generate random secret (32 bytes, base64)
openssl rand -base64 32

# Generate random secret (hex)
openssl rand -hex 32

# Generate JWT secret
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"

# Generate using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 2. Required Variables

### Core Application

```bash
# AI/LLM Configuration
OPENAI_API_KEY=sk-...                    # Required for AI tutoring agents
OPENAI_MODEL=gpt-4o                      # Model to use (default: gpt-4o)

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db   # PostgreSQL connection
NEON_DATABASE_URL=postgresql://...       # Neon managed PostgreSQL (production)

# Authentication
BETTER_AUTH_SECRET=...                   # JWT signing secret (32+ chars)
AUTH_URL=http://localhost:3000           # Base URL for auth

# Kafka
KAFKA_BROKER=kafka:9092                  # Kafka broker address
KAFKA_TOPIC_PREFIX=learnflow             # Topic prefix
```

### Infrastructure

```bash
# Kubernetes
KUBECONFIG=~/.kube/config               # Kubeconfig path
NAMESPACE=learnflow                     # Default namespace

# Dapr
DAPR_HTTP_PORT=3500                     # Dapr sidecar HTTP port
STATE_STORE_NAME=statestore             # Dapr state store component
PUBSUB_NAME=pubsub                      # Dapr pub/sub component
```

### Development

```bash
# Ports
FRONTEND_PORT=3000                      # Next.js frontend
BACKEND_PORT=8000                       # FastAPI backend
DAPR_HTTP_PORT=3500                     # Dapr sidecar

# Debug
DEBUG=true                              # Enable debug mode
LOG_LEVEL=INFO                          # Logging level
```

---

## 3. Adding Variables

### Method 1: .env File (Recommended for Development)

```bash
# Create .env file
touch .env

# Add variables
echo "OPENAI_API_KEY=sk-..." >> .env
echo "DATABASE_URL=postgresql://..." >> .env

# Or edit directly
nano .env
```

**.env file format:**
```bash
# Comment lines start with #
OPENAI_API_KEY=sk-proj-abc123...
DATABASE_URL=postgresql://user:password@localhost:5432/learnflow
BETTER_AUTH_SECRET=my-super-secret-key-minimum-32-chars
DEBUG=true
```

### Method 2: Shell Export (Temporary)

```bash
# Export single variable
export OPENAI_API_KEY=sk-...

# Export multiple
export OPENAI_API_KEY=sk-... DATABASE_URL=postgresql://...

# Load from .env file
export $(cat .env | grep -v '^#' | xargs)

# Or use source (if .env has export statements)
source .env
```

### Method 3: Kubernetes Secrets

```bash
# Create secret from .env file
kubectl create secret generic learnflow-secrets \
  --from-env-file=.env \
  -n learnflow

# Create secret from literal values
kubectl create secret generic api-keys \
  --from-literal=OPENAI_API_KEY=sk-... \
  --from-literal=DATABASE_URL=postgresql://... \
  -n learnflow

# Create secret from file
kubectl create secret generic db-creds \
  --from-file=./secrets/db-password.txt \
  -n learnflow
```

### Method 4: Kubernetes ConfigMap (Non-sensitive)

```bash
# Create ConfigMap
kubectl create configmap learnflow-config \
  --from-literal=FRONTEND_PORT=3000 \
  --from-literal=LOG_LEVEL=INFO \
  -n learnflow
```

---

## 4. Removing Variables

### From .env File

```bash
# Remove line containing variable
sed -i '/VARIABLE_NAME/d' .env

# Or edit manually
nano .env
# Delete the line and save
```

### From Shell

```bash
# Unset single variable
unset OPENAI_API_KEY

# Unset multiple
unset OPENAI_API_KEY DATABASE_URL
```

### From Kubernetes

```bash
# Delete entire secret
kubectl delete secret learnflow-secrets -n learnflow

# Edit secret (remove specific key)
kubectl edit secret learnflow-secrets -n learnflow
# Find and remove the key from data section

# Patch to remove key
kubectl patch secret learnflow-secrets -n learnflow \
  --type=json \
  -p='[{"op": "remove", "path": "/data/OPENAI_API_KEY"}]'
```

---

## 5. Updating Variables

### Update .env File

```bash
# Replace value using sed
sed -i 's/OPENAI_API_KEY=.*/OPENAI_API_KEY=new-key/' .env

# Or edit manually
nano .env
```

### Update Kubernetes Secret

```bash
# Method 1: Delete and recreate
kubectl delete secret learnflow-secrets -n learnflow
kubectl create secret generic learnflow-secrets --from-env-file=.env -n learnflow

# Method 2: Patch specific value (base64 encoded)
kubectl patch secret learnflow-secrets -n learnflow \
  -p='{"data":{"OPENAI_API_KEY":"'$(echo -n "new-key" | base64)'"}}'

# Method 3: Edit interactively
kubectl edit secret learnflow-secrets -n learnflow
```

---

## 6. Using Variables

### In Python (FastAPI)

```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access variables
openai_key = os.getenv("OPENAI_API_KEY")
db_url = os.getenv("DATABASE_URL")

# With default value
debug = os.getenv("DEBUG", "false").lower() == "true"
```

### In JavaScript/TypeScript (Next.js)

```typescript
// Server-side (safe for secrets)
const apiKey = process.env.OPENAI_API_KEY;

// Client-side (must be prefixed with NEXT_PUBLIC_)
const publicUrl = process.env.NEXT_PUBLIC_API_URL;
```

**next.config.js:**
```javascript
module.exports = {
  env: {
    CUSTOM_VAR: process.env.CUSTOM_VAR,
  },
};
```

### In Shell Scripts

```bash
#!/bin/bash
# Load .env
source .env

# Use variable
echo "Using API key: ${OPENAI_API_KEY:0:10}..."

# With default
PORT=${FRONTEND_PORT:-3000}
```

### In Kubernetes Deployments

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        # From Secret
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: learnflow-secrets
              key: OPENAI_API_KEY
        # From ConfigMap
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: learnflow-config
              key: LOG_LEVEL
        # Direct value (avoid for secrets)
        - name: NODE_ENV
          value: "production"
```

---

## 7. Best Practices

### Security

| ✅ Do | ❌ Don't |
|-------|---------|
| Use `.env` files locally | Commit `.env` to git |
| Use K8s Secrets in production | Hardcode secrets in code |
| Rotate secrets regularly | Share secrets via chat/email |
| Use different keys per environment | Use production keys in dev |

### .gitignore

```gitignore
# Environment files
.env
.env.local
.env.*.local
*.env

# Secret files
secrets/
*.pem
*.key
```

### .env.example Template

```bash
# LearnFlow Environment Variables
# Copy this file to .env and fill in values

# AI Configuration (Required)
OPENAI_API_KEY=sk-your-key-here

# Database (Required)
DATABASE_URL=postgresql://user:password@localhost:5432/learnflow

# Authentication (Required)
BETTER_AUTH_SECRET=generate-with-openssl-rand-base64-32

# Optional
DEBUG=false
LOG_LEVEL=INFO
FRONTEND_PORT=3000
BACKEND_PORT=8000
```

---

## 8. Quick Commands Reference

```bash
# View all environment variables
printenv | sort

# View specific variable
echo $OPENAI_API_KEY

# Check if variable is set
[[ -z "$OPENAI_API_KEY" ]] && echo "Not set" || echo "Set"

# Load .env file
export $(cat .env | grep -v '^#' | xargs)

# Create .env from example
cp .env.example .env

# Validate .env has all required vars
for var in OPENAI_API_KEY DATABASE_URL BETTER_AUTH_SECRET; do
  [[ -z "${!var}" ]] && echo "Missing: $var"
done

# View K8s secret (base64 decoded)
kubectl get secret learnflow-secrets -n learnflow -o jsonpath='{.data.OPENAI_API_KEY}' | base64 -d

# List all secrets in namespace
kubectl get secrets -n learnflow
```

---

*Last Updated: 2026-02-08*
