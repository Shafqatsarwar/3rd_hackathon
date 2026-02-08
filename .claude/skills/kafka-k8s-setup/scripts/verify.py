#!/usr/bin/env python3
# Kafka Verification Script

import subprocess
import json
import sys

def check_kafka_status():
    """Verify Kafka pods are running and accessible"""
    try:
        # Get pods in kafka namespace
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", "kafka", "-o", "json"],
            capture_output=True, text=True, check=True
        )
        pods = json.loads(result.stdout)["items"]

        # Count running pods
        running = sum(1 for pod in pods if pod["status"]["phase"] == "Running")
        total = len(pods)

        if running == total and total > 0:
            print(f"✓ All {total} Kafka pods running")

            # Test topic creation
            try:
                create_topic_result = subprocess.run([
                    "kubectl", "run", "test-producer", "--image=bitnami/kafka",
                    "-n", "kafka", "--rm", "-it", "--restart=Never",
                    "--", "kafka-topics.sh", "--create", "--topic", "test-topic",
                    "--bootstrap-server", "kafka:9092", "--partitions", "1", "--replication-factor", "1"
                ], capture_output=True, text=True, timeout=30)

                if create_topic_result.returncode == 0 or "already exists" in create_topic_result.stderr:
                    print("✓ Kafka is accessible and can create topics")
                    sys.exit(0)
                else:
                    print(f"✗ Kafka topic creation failed: {create_topic_result.stderr}")
                    sys.exit(1)
            except subprocess.TimeoutExpired:
                print("✗ Kafka topic creation timed out")
                sys.exit(1)
        else:
            print(f"✗ {running}/{total} Kafka pods running")
            for pod in pods:
                name = pod["metadata"]["name"]
                status = pod["status"]["phase"]
                print(f"  - {name}: {status}")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to check Kafka status: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error checking Kafka: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_kafka_status()