#!/bin/bash
# Move to project root
cd /mnt/d/Panaverse/projects/3rd_hackathon

echo "Starting Phase 2 Infrastructure Deployment..."

# 1. Deploy Kafka
echo "Deploying Kafka..."
cd .claude/skills/kafka-k8s-setup
./scripts/deploy.sh
python3 scripts/verify.py > /mnt/d/Panaverse/projects/3rd_hackathon/kafka_status.txt 2>&1

# 2. Deploy PostgreSQL
echo "Deploying PostgreSQL..."
cd /mnt/d/Panaverse/projects/3rd_hackathon
cd .claude/skills/postgres-k8s-setup
./scripts/deploy.sh
./scripts/migrate.sh
python3 scripts/verify.py > /mnt/d/Panaverse/projects/3rd_hackathon/postgres_status.txt 2>&1

echo "Deployment finished."
