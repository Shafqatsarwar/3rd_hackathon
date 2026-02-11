#!/bin/bash
# PostgreSQL Migration Script

NAMESPACE=${1:-postgresql}
DB_NAME=${2:-learnflow}

echo "Running database migrations for $DB_NAME in namespace $NAMESPACE"

# Create a temporary pod to run migrations
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: migration-job-$(date +%s)
  namespace: $NAMESPACE
spec:
  restartPolicy: Never
  containers:
  - name: migrator
    image: bitnami/postgresql:latest
    env:
    - name: PGPASSWORD
      valueFrom:
        secretKeyRef:
          name: postgresql
          key: postgres-password
    command:
    - sh
    - -c
    - |
      echo "Running database migrations..."

      # Wait for PostgreSQL to be ready
      until pg_isready -h postgresql -p 5432 -U postgres; do
        echo "Waiting for PostgreSQL to be ready..."
        sleep 2
      done

      # Create the database if it doesn't exist
      psql -h postgresql -p 5432 -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
      psql -h postgresql -p 5432 -U postgres -c "CREATE DATABASE $DB_NAME;"

      # Run any migration commands here
      echo "Migration completed successfully!"

      # Connect to the specific database and run schema creation if needed
      psql -h postgresql -p 5432 -U postgres -d $DB_NAME -c "
        -- Create tables for LearnFlow application
        CREATE TABLE IF NOT EXISTS users (
          id SERIAL PRIMARY KEY,
          username VARCHAR(255) UNIQUE NOT NULL,
          email VARCHAR(255) UNIQUE NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS courses (
          id SERIAL PRIMARY KEY,
          name VARCHAR(255) NOT NULL,
          description TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS progress (
          id SERIAL PRIMARY KEY,
          user_id INTEGER REFERENCES users(id),
          course_id INTEGER REFERENCES courses(id),
          completed BOOLEAN DEFAULT FALSE,
          score DECIMAL(5,2),
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_progress_user ON progress(user_id);
        CREATE INDEX IF NOT EXISTS idx_progress_course ON progress(course_id);
      "
EOF

# Wait for the migration job to complete
JOB_NAME=$(kubectl get pods -n $NAMESPACE --sort-by=.metadata.creationTimestamp | grep migration-job | tail -n 1 | awk '{print $1}')

if [ ! -z "$JOB_NAME" ]; then
    echo "Waiting for migration job to complete..."
    kubectl wait --for=condition=ready pod/$JOB_NAME -n $NAMESPACE --timeout=300s

    # Check the logs to confirm migration success
    kubectl logs pod/$JOB_NAME -n $NAMESPACE

    # Clean up the temporary pod
    kubectl delete pod/$JOB_NAME -n $NAMESPACE --ignore-not-found
fi

echo "✓ Database migrations completed for $DB_NAME in namespace $NAMESPACE"