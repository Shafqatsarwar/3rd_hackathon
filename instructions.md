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

If you have less than 8GB RAM, you **must** free up space before starting the cluster:

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

## 🚑 Troubleshooting

**Issue: `manifest unknown` (Image Pull Error)**
-   **Solution**: Use the AWS Public ECR registry instead of Docker Hub.
-   **Helm Settings**:
    ```bash
    --set image.registry=public.ecr.aws
    --set image.repository=bitnami/kafka (or postgresql)
    --set global.security.allowInsecureImages=true
    ```

**Issue: `context deadline exceeded` (Timeout)**
-   **Cause**: The pod is taking too long to pull or initialization is slow due to RAM pressure.
-   **Fix**: 
    1. Close high-RAM Windows apps (Chrome, etc.).
    2. Increase Helm timeout: `--timeout 900s`.
    3. Disable database persistence: `--set primary.persistence.enabled=false`.

**Issue: `exec format error`**
-   **Cause**: Docker is trying to use `docker-credential-desktop.exe`.
-   **Fix**: Run the `sed` command in Step 1 to rename the `credsStore`.
