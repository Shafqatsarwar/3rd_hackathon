---
type: product
scope: learnflow
version: 1.0
---

# LearnFlow Product Specification

> **Product Definition** – What LearnFlow is and does.

## Product Overview

LearnFlow is an **AI-powered Python tutoring platform** that teaches students Python programming through conversational AI tutors, interactive code execution, and adaptive learning paths.

---

## Users

| Role | Description | Capabilities |
|------|-------------|--------------|
| Student | Primary user, learning Python | Chat with AI, run code, track progress |
| Teacher | Content creator, progress reviewer | View analytics, customize curriculum |
| Admin | System administrator | Manage users, configure system |

---

## Core Capabilities

### 1. Conversational Tutoring
- Natural language Q&A with AI tutors
- Adaptive responses based on student level
- Multi-agent specialization (concepts, debugging, exercises)

### 2. Code Execution Sandbox
- Safe Python code execution
- 5s timeout, 50MB memory limit
- No network/filesystem access
- Real-time output and error feedback

### 3. Progress Tracking
- Mastery score calculation
- Topic-by-topic progress
- Historical performance data
- Learning path recommendations

### 4. Struggle Detection
- Automatic detection of student struggles
- Triggers include: repeated errors, time spent, keywords
- Proactive intervention by AI tutors

---

## Mastery Calculation

```
Mastery Score = (
    Exercises × 0.40 +
    Quizzes × 0.30 +
    Code Quality × 0.20 +
    Consistency × 0.10
)
```

### Mastery Levels
| Level | Score Range | Description |
|-------|-------------|-------------|
| Beginner | 0-40% | Just starting |
| Learning | 41-70% | Making progress |
| Proficient | 71-90% | Solid understanding |
| Mastered | 91-100% | Expert level |

---

## Struggle Detection Triggers

| Trigger | Threshold |
|---------|-----------|
| Same Error | 3+ times same error type |
| Time Stuck | >10 minutes on single problem |
| Quiz Score | <50% on topic quiz |
| Keywords | "stuck", "confused", "help" |
| Failures | 5+ consecutive code execution failures |

---

## Non-Functional Requirements

| Requirement | Specification |
|-------------|---------------|
| Architecture | Event-driven (Kafka + Dapr) |
| Scalability | Horizontal pod autoscaling |
| Build Method | Fully agent-built via Skills |
| Latency | API p95 < 500ms |
| AI Response | p95 < 2s for simple queries |
| Availability | 99.5% SLO |

---

## User Journeys

### Student: Learn Python Basics
```
1. Student logs in
2. Selects "Python Basics" topic
3. Asks: "What is a variable?"
4. Concepts Agent explains with examples
5. Student tries exercise
6. Exercise Agent grades submission
7. Progress Agent updates mastery score
```

### Student: Debug Code
```
1. Student submits code with error
2. Debug Agent detects error
3. Provides hint (not solution)
4. Student fixes code
5. Success → mastery increases
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js + Monaco Editor |
| Backend | FastAPI + OpenAI SDK |
| AI Agents | GPT-4o via OpenAI API |
| Database | PostgreSQL (Neon) |
| Events | Apache Kafka |
| Service Mesh | Dapr |
| Auth | Better Auth (JWT) |

---

**Status**: Active  
**Last Updated**: 2026-02-08
