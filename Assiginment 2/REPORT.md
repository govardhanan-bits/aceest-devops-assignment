# ACEest Fitness & Gym - CI/CD Pipeline Report

**Course:** Introduction to DevOps (CSIZG514/SEZG514) | **Assignment:** 2  
**Student:** [Your Name] | **ID:** [Your BITS ID]  
**Date:** April 2026

---

## 1. CI/CD Architecture Overview

### Pipeline Flow

```
GitHub (Push) → Jenkins (CI Server) → Pytest (Unit Tests) → SonarQube (Code Quality)
    → Docker Build → Docker Hub (Registry) → Kubernetes (Minikube) → Live Deployment
```

### Components

| Tool | Purpose |
|------|---------|
| **Git / GitHub** | Version control & source code management |
| **Jenkins** | Build automation & CI/CD orchestration |
| **Pytest** | Automated unit testing (25+ test cases) |
| **SonarQube** | Static code analysis & quality gates |
| **Docker** | Application containerization |
| **Docker Hub** | Container image registry |
| **Kubernetes (Minikube)** | Container orchestration & deployment |

### Application Architecture

The ACEest Fitness & Gym application is a **Flask web application** (converted from the original tkinter desktop app) that provides:

- **User authentication** (login/logout with role-based access)
- **Client management** (CRUD operations for fitness clients)
- **Program assignment** (Fat Loss, Muscle Gain, Beginner)
- **Progress tracking** (weekly adherence logging)
- **Workout logging** (session tracking with duration/notes)
- **REST API** (health check, client data, progress data)
- **Calorie estimation** based on weight and program type

### Version Evolution

| Version | Key Features |
|---------|-------------|
| v1.0 | Basic tkinter UI with program display |
| v1.1 | Client profile input, calorie estimation |
| v1.1.2 | CSV export, progress chart, client table |
| v2.0.1 | SQLite database persistence |
| v2.1.2 | Database-backed client management |
| v2.2.1 | Progress charting with matplotlib |
| v2.2.4 | Extended schema, BMI, workout logging |
| v3.0.1 | Tabbed UI, body metrics |
| v3.1.2 | Role-based login, AI program generator |
| v3.2.4 | Flask web app, REST API, full CI/CD pipeline |

---

## 2. Deployment Strategies Implemented

### 2.1 Rolling Update
- Pods are replaced **one at a time** with `maxSurge: 1` and `maxUnavailable: 0`
- Ensures **zero downtime** during deployment
- Rollback: `kubectl rollout undo deployment/aceest-fitness-rolling`

### 2.2 Blue-Green Deployment
- Two identical environments: **Blue** (v3.1.2) and **Green** (v3.2.4)
- Service selector switches traffic between environments
- Rollback: Change service selector from `slot: green` to `slot: blue`

### 2.3 Canary Release
- **3 stable pods** (v3.1.2) + **1 canary pod** (v3.2.4) = ~25% canary traffic
- Shared label allows the Service to route to both
- Monitor canary health; scale up if stable, delete if faulty

### 2.4 A/B Testing
- Two versions with **header-based routing** via NGINX Ingress
- Users with `X-Version: B` header get the new version
- All other users see the stable version A

### 2.5 Shadow Deployment
- Production traffic is **mirrored** to a shadow deployment using Istio
- Shadow responses are discarded; users always see the primary version
- Validates new version behavior under real production load

---

## 3. Challenges Faced and Mitigation Strategies

| Challenge | Mitigation |
|-----------|-----------|
| **Converting tkinter to Flask** | Redesigned UI as HTML templates using Bootstrap; maintained the same data model and business logic |
| **Database state in containers** | Used SQLite with volume mounts; for production, recommend migrating to PostgreSQL |
| **Jenkins-GitHub integration** | Configured webhook-based SCM polling; used credentials plugin for secure auth |
| **SonarQube quality gates** | Initially failed on code smells; refactored to pass quality gates |
| **Kubernetes health checks** | Added `/api/health` endpoint for liveness and readiness probes |
| **Docker image size** | Used `python:3.11-slim` base and `.dockerignore` to minimize image |
| **Shadow deployment** | Requires Istio service mesh; configured VirtualService for traffic mirroring |

---

## 4. Key Automation Outcomes

- **Fully automated pipeline**: A single `git push` triggers build, test, quality analysis, containerization, and deployment
- **25+ automated test cases** covering authentication, client management, progress tracking, API endpoints, and data validation
- **Zero-downtime deployments** through rolling updates and blue-green strategy
- **Instant rollback** capability via `kubectl rollout undo` or service selector change
- **Code quality enforcement** through SonarQube quality gates integrated into the pipeline
- **Containerized, reproducible builds** ensuring consistency across development, testing, and production environments
- **Multiple deployment strategies** providing flexibility for different release scenarios

---

## 5. Repository Structure

```
├── app.py                          # Flask web application
├── test_app.py                     # Pytest unit tests
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container build instructions
├── .dockerignore                   # Docker build exclusions
├── Jenkinsfile                     # CI/CD pipeline definition
├── sonar-project.properties        # SonarQube configuration
├── .gitignore                      # Git exclusions
├── templates/                      # Flask HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── add_client.html
│   ├── client.html
│   └── programs.html
├── k8s/                            # Kubernetes manifests
│   ├── namespace.yaml
│   ├── secret.yaml
│   ├── deployment.yaml             # Standard deployment
│   ├── service.yaml
│   ├── rolling-update.yaml         # Rolling update strategy
│   ├── blue-green-deployment.yaml  # Blue-green strategy
│   ├── canary-deployment.yaml      # Canary release strategy
│   ├── ab-testing.yaml             # A/B testing strategy
│   └── shadow-deployment.yaml      # Shadow deployment strategy
└── The code versions for DevOps Assignment/
    ├── Aceestver-1.0.py ... Aceestver-3.2.4.py
```
