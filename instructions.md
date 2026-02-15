# Infrastructure Setup Instructions (WSL)

> **Goal**: Deploy Kafka and PostgreSQL to a local Kubernetes cluster (Minikube) inside WSL.

---

## 🛑 CRITICAL PRE-REQUISITES (Do these first!)

To avoid the "exec format error" or "ImagePullBackOff" errors on Windows/WSL, follow these steps:

### 1. Fix Docker Config (WSL)
Renaming the Windows credential store prevents WSL from hanging on `.exe` files:

```bash
sed -i 's/"credsStore": "desktop.exe"/"_credsStore": "desktop.exe"/' ~/.docker/config.json
```

---

## 2. Resource Cleanup (Free up RAM)

If you have less than 2200MB limit RAM, you **must** free up space before starting the cluster:

```bash
# Clear all unused images/containers
docker system prune -a --volumes -f

# Clear Linux buffer cache
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

---

## 3. Start Infrastructure (RAM Optimized)

### Step 1: Start Minikube
For a 3.7GB RAM host, use these specific limits:

```bash
# Delete old cluster if it exists
minikube delete

# Start with optimized memory (3072MB)
minikube start --driver=docker --memory=3072 --cpus=2
# To avoide space issues (2200MB)
minikube start --driver=docker --memory=2200 --cpus=2

**Problem**: System has only 3.7GB RAM. High limits (3GB+) freeze the host.
-   **Solution**: 
    1.  Run `wsl --shutdown` in Windows PowerShell.
    2.  Run `minikube delete` in Ubuntu.
    3.  Restart with a safe limit: `minikube start --driver=docker --memory=2200 --cpus=2`
```

### Step 2: Deploy Services
Our scripts are now optimized to use **Public ECR** (to avoid Docker Hub pull errors) and **No-Persistence** (to save RAM).

```bash
cd /mnt/d/Panaverse/projects/3rd_hackathon

# 1. Deploy Kafka
bash .claude/skills/kafka-k8s-setup/scripts/deploy.sh

# 2. Deploy PostgreSQL
bash .claude/skills/postgres-k8s-setup/scripts/deploy.sh
```

---

## 5. Phase 4: Frontend Development Variables

To deploy the frontend successfully, you need to populate these variables in your `.env` file. 

### API Keys & Secrets
1.  **OpenAI API Key**: Used by AI agents.
    -   Get it from: [OpenAI Platform](https://platform.openai.com/api-keys)
2.  **NextAuth Secret**: Used for session encryption.
    -   Generate it in Ubuntu: `openssl rand -base64 32`
3.  **Database URL**: Connection string for PostgreSQL.
    -   Use the K8s service URL: `postgresql://postgres:securePassword123@postgresql.postgresql.svc.cluster.local:5432/learnflow`

### Setting up Kubernetes Secrets
Once your `.env` is ready, push it to the cluster:

```bash
# Create the secret (re-creates if exists)
kubectl delete secret learnflow-secrets -n learnflow --ignore-not-found
kubectl create secret generic learnflow-secrets \
  --from-env-file=.env \
  -n learnflow
```

---

## 🚑 Troubleshooting

**Issue: `exec format error` (WSL vs Windows Docker/Helm)**
-   **Problem**: WSL tries to use Windows `docker-credential-desktop.exe`.
-   **Method 1: The "One-Off" Fix (Safest)**: 
    Bypass it by setting a temporary empty Docker config for the specific command:
    ```bash
    # For Helm/Deploy
    DOCKER_CONFIG=/tmp/empty-docker-config bash .claude/skills/kafka-k8s-setup/scripts/deploy.sh

    # For Docker Build
    DOCKER_CONFIG=/tmp/empty-docker-config docker build -t learnflow-backend:latest .
    ```
-   **Method 2: The "Global" Fix (Permanent)**:
    Open your Docker config in WSL and remove the `credsStore` line:
    ```bash
    nano ~/.docker/config.json
    ```
    Find and delete this line: `"credsStore": "desktop.exe"`. Save and exit.

**Issue: WSL / Minikube Hangs (RAM Exhaustion)**
-   **Problem**: System has only 3.7GB RAM. High limits (3GB+) freeze the host.
-   **Solution**: 
    1.  Run `wsl --shutdown` in Windows PowerShell.
    2.  Run `minikube delete` in Ubuntu.
    3.  Restart with a safe limit: `minikube start --driver=docker --memory=2200 --cpus=2`

**Issue: `manifest unknown` (Image Pull Error)**
-   **Solution**: Use the AWS Public ECR registry instead of Docker Hub.
-   **Scripts**: Already updated in `.claude/skills/`.
-   **Helm Settings**:
    ```bash
    --set image.registry=public.ecr.aws
    --set image.repository=bitnami/kafka (or postgresql)
    --set global.security.allowInsecureImages=true

**Issue: `context deadline exceeded` (Timeout)**
-   **Cause**: The pod is taking too long to pull or initialization is slow due to RAM pressure.
-   **Fix**: 
    1. Close high-RAM Windows apps (Chrome, etc.).
    2. Increase Helm timeout: `--timeout 900s`.
    3. Disable database persistence: `--set primary.persistence.enabled=false`.

**Issue: `exec format error`**
-   **Cause**: Docker is trying to use `docker-credential-desktop.exe`.
-   **Fix**: Run the `sed` command in Step 1 to rename the `credsStore`.
