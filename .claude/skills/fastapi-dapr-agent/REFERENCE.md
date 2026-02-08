# FastAPI Dapr Agent - Reference Documentation

## Overview
Creates FastAPI microservices with Dapr integration for state management, pub/sub messaging, and service-to-service invocation.

## Service Architecture
Each generated service includes:
- FastAPI application with OpenAI SDK integration
- Dapr sidecar for distributed capabilities
- Health check and readiness endpoints
- Configuration for Kubernetes deployment

## Dapr Components

### State Store
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis:6379
```

### Pub/Sub (Kafka)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: kafka:9092
```

### Service Invocation
Services can invoke each other using:
```python
async def invoke_service(service_name: str, method: str, data: dict):
    async with httpx.AsyncClient() as client:
        url = f"http://localhost:3500/v1.0/invoke/{service_name}/method/{method}"
        response = await client.post(url, json=data)
        return response.json()
```

## LearnFlow Agents

### Triage Agent
Routes queries to appropriate specialists:
- "explain" → Concepts Agent
- "error" → Debug Agent
- "review" → Code Review Agent
- "exercise" → Exercise Agent
- "progress" → Progress Agent

### Concepts Agent
Explains Python concepts with:
- Adaptive complexity based on student level
- Code examples and visualizations
- Interactive follow-up questions

### Code Review Agent
Analyzes code for:
- Correctness and logic errors
- PEP 8 style compliance
- Efficiency improvements
- Readability suggestions

### Debug Agent
Provides debugging assistance:
- Parses error messages
- Identifies root causes
- Offers hints before solutions
- Tracks common error patterns

### Exercise Agent
Generates learning exercises:
- Topic-based challenges
- Auto-grading criteria
- Progressive difficulty
- Instant feedback

### Progress Agent
Tracks student mastery:
- Mastery score calculation
- Learning path recommendations
- Struggle detection alerts
- Progress summaries

## Configuration Options

### Service Generation
- Service name and port
- AI model configuration
- Dapr component selection
- Kubernetes resource limits

### Deployment Parameters
- Namespace configuration
- Replica count
- Resource requests/limits
- Environment variables

## Security Considerations
- API key management via secrets
- Network policies for service isolation
- Rate limiting configuration
- Input validation and sanitization
