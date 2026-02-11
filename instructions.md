# Infrastructure Setup Instructions (WSL)

> **Goal**: Deploy Kafka and PostgreSQL to a local Kubernetes cluster (Minikube) inside WSL.

---

## 🛑 CRITICAL PRE-REQUISITES (Do these first!)

To avoid the "exec format error" or "ImagePullBackOff" errors, follow these 2 steps **before** starting.

### 1. Fix Docker Config (WSL)
Run this command in your **Ubuntu Terminal** to remove the Windows-specific config that breaks Linux:

```bash
rm -f ~/.docker/config.json
```
*(This is safe. Docker will regenerate a compatible config if needed).*

### 2. Enable Docker Integration
1.  Open **Docker Desktop** on Windows.
2.  Go to **Settings** (Gear Icon) -> **Resources** -> **WSL Integration**.
3.  **Toggle "Ubuntu" to ON**. (Even if "Default WSL distro" is checked, toggle Ubuntu explicitly).
4.  Click **Apply & Restart**.

---

## 1. Environment Variables

Ensure your `.env` file in the project root has these added at the bottom:

```bash
# WSL Credentials
WSL_USER=shafqatsarwar
WSL_PASSWORD=shafqat
```

---

## 2. Install Tools (If missing)

Run these checks in your Ubuntu Terminal. If any command says "not found", run the install block below.

```bash
# Check existing tools
minikube version
kubectl version --client
```

**Install Script (Copy & Paste if tools are missing):**
```bash
# Install Kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

---

## 3. Start Infrastructure

### Step 1: Start Minikube
**If you had previous failures, delete the old cluster first:**

```bash
minikube delete
```

**Then start fresh:**
```bash
minikube start
```
*Wait for "Done! kubectl is now configured..."*

### Step 2: Deploy Services
Run the automated deployment script:

```bash
cd /mnt/d/Panaverse/projects/3rd_hackathon
./deploy_infra_wsl.sh
```

---

## 4. Verification

After the script finishes, check that the pods are actually running:

```bash
# Check all pods in all namespaces
kubectl get pods -A
```

**Success Criteria:**
-   Pods in `kafka` namespace are `Running`.
-   Pods in `postgresql` namespace are `Running`.

---

## 🚑 Troubleshooting

**Issue: `manifest unknown` (Image Pull Error)**
-   **Cause**: The specific Docker image tag (e.g., `3.7.0-debian-12-r1`) was removed from the registry.
-   **Fix**: Update `scripts/deploy.sh` to use a valid tag like `3.9.0` or `latest`.
    ```bash
    helm upgrade --install kafka bitnami/kafka --set image.tag=3.9.0 ...
    ```

**Issue: `Init:ImagePullBackOff` or `ErrImagePull`**
-   **Cause**: Minikube started with the bad Docker config.
-   **Fix**:
    1.  Run `rm -f ~/.docker/config.json` again.
    2.  Run `minikube delete`.
    3.  Run `minikube start`.

**Issue: `exec format error`**
-   **Cause**: Docker is trying to use `docker-credential-desktop.exe`.
-   **Fix**: Run `rm -f ~/.docker/config.json`.
