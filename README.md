# ACEest Fitness Application - DevOps CI/CD Project

**Submitted by:** Govardhanan K S  
**Roll Number:** 2025ht66025  
**Subject:** Introduction to DevOps – Assignment  
**Institution:** BITS Pilani  

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-85%25-green)
![Python](https://img.shields.io/badge/python-3.10-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

## 📋 Project Overview

This project demonstrates the implementation of a complete DevOps CI/CD pipeline for the ACEest Fitness Application. The application has evolved through multiple versions (from v1.0 to v3.2.4), and this implementation showcases modern DevOps practices including containerization, automated testing, continuous integration, and deployment automation.

### Learning Objectives
- Implement version control strategies and semantic versioning
- Design and implement CI/CD pipelines
- Apply containerization with Docker
- Implement automated testing and code quality checks
- Design deployment strategies for multiple environments

## 🚀 Technologies Used

- **Backend**: Python 3.10, Flask Web Framework
- **Database**: SQLite3
- **Version Control**: Git & GitHub
- **Testing**: pytest, pytest-flask, coverage.py
- **Code Quality**: flake8, black, pylint, bandit
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Security**: Bandit, Safety, Trivy
- **Build Automation**: Docker Buildx

## 📱 Application Description

The ACEest Fitness Application is a Flask-based web service that provides API endpoints for managing fitness programs and client data. The application includes:

### Key Features
- Client management system
- Fitness program catalog
- RESTful API endpoints
- Health monitoring
- Application statistics
- SQLite database integration

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Application status and version |
| `/health` | GET | Health check for monitoring |
| `/clients` | GET | Get all clients |
| `/clients/<id>` | GET | Get specific client by ID |
| `/clients` | POST | Create new client |
| `/programs` | GET | Get available fitness programs |
| `/stats` | GET | Get application statistics |

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Docker and Docker Compose (for containerized deployment)
- Git

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Devops
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the application**
- Open browser: http://localhost:5000
- Health check: http://localhost:5000/health
- API endpoints: http://localhost:5000/clients

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build Docker image
docker build -t aceest-fitness-app .

# Run container
docker run -d -p 5000:5000 --name aceest-app aceest-fitness-app

# Check logs
docker logs aceest-app

# Stop container
docker stop aceest-app
```

### Using Docker Compose

```bash
# Build and start services
docker compose up --build

# Run in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## 🧪 Testing

### Run All Tests

```bash
# Run tests with pytest
python -m pytest

# Run tests with coverage
python -m pytest --cov=app --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html
```

### Run Specific Test Classes

```bash
# Run specific test class
python -m pytest tests/test_app.py::TestHomeEndpoint -v

# Run with verbose output
python -m pytest -v

# Run with detailed output
python -m pytest -vv
```

## 📊 Code Quality

### Linting and Formatting

```bash
# Check code formatting with black
black --check app.py tests/

# Format code
black app.py tests/

# Run flake8 linting
flake8 app.py tests/

# Run pylint static analysis
pylint app.py

# Security scan with bandit
bandit -r app.py
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The project includes a comprehensive CI/CD pipeline that runs on every push and pull request:

1. **Code Quality & Linting**
   - Black code formatting check
   - Flake8 linting
   - Pylint static analysis
   - Bandit security scanning

2. **Automated Testing**
   - Unit tests with pytest
   - Code coverage reporting (minimum 80%)
   - Test result artifacts

3. **Docker Build & Validation**
   - Docker image build
   - Container testing
   - Trivy vulnerability scanning

4. **Security Checks**
   - Dependency security scanning with Safety
   - Container vulnerability scanning

5. **Deployment**
   - Staging deployment (on develop branch)
   - Production deployment (on main branch)

### Pipeline Stages

```
Developer → Git Push → GitHub 
                          ↓
                    GitHub Actions
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                  ↓
   Code Quality      Unit Tests       Docker Build
        ↓                 ↓                  ↓
   Linting          Coverage          Security Scan
        ↓                 ↓                  ↓
        └─────────────────┴──────────────────┘
                          ↓
                    Deploy to Staging
                          ↓
                    Deploy to Production
```

## 📁 Project Structure

```
ACEest-DevOps/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions workflow
├── tests/
│   ├── __init__.py
│   └── test_app.py            # Automated tests
├── data/
│   └── aceest_fitness.db      # SQLite database
├── The code versions for DevOps Assignment/
│   ├── Aceestver-1.0.py       # Version 1.0
│   ├── Aceestver-1.1.py       # Version 1.1
│   └── ...                    # Other versions
├── k8s/
│   └── deployment.yml         # Kubernetes manifests
├── app.py                     # Flask application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── README.md                  # Project documentation
└── DevOps_Assignment_ACEest_Case_Study.md  # Assignment details
```

## 🔍 Version History & Analysis

### Semantic Versioning Pattern

The ACEest application follows semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR** (v1, v2, v3): Breaking changes or major feature additions
- **MINOR** (x.1, x.2, x.3): New features, backward compatible
- **PATCH** (x.x.1, x.x.2): Bug fixes and minor improvements

### Version Evolution

| Version | Key Changes | Type |
|---------|-------------|------|
| v1.0 | Basic Tkinter GUI | Initial Release |
| v1.1 | Enhanced UI | Minor Update |
| v2.1.2 | Database integration | Major Update |
| v2.2.4 | Bug fixes | Patch |
| v3.0.1 | User management | Major Update |
| v3.2.4 | PDF reporting | Feature Addition |

## 🚢 Deployment Strategy

### Environment Configuration

- **Development**: Local development with hot reload
- **Staging**: Pre-production testing environment
- **Production**: Live production environment

### Kubernetes Deployment

The project includes Kubernetes manifests in `k8s/deployment.yml`:

**Components:**
- **Deployment** — 2 replicas with rolling update strategy (zero-downtime)
- **Service** — ClusterIP exposing port 80 → 5000
- **PersistentVolumeClaim** — 1Gi storage for SQLite database persistence
- **Ingress** — External access via hostname routing

**Deploy to Kubernetes:**

```bash
# Apply all manifests
kubectl apply -f k8s/deployment.yml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# View logs
kubectl logs -l app=aceest-fitness

# Scale replicas
kubectl scale deployment aceest-fitness-app --replicas=3
```

**Health Probes Configured:**
- **Liveness Probe**: `GET /health` every 30s — restarts unhealthy containers
- **Readiness Probe**: `GET /health` every 10s — removes unready pods from service

**Resource Limits:**
- CPU: 100m request / 500m limit
- Memory: 128Mi request / 256Mi limit

### Blue-Green Deployment

1. Deploy new version to "green" environment
2. Run smoke tests
3. Switch traffic from "blue" to "green"
4. Keep "blue" as rollback option

### Rollback Strategy

```bash
# Docker rollback
docker compose down
docker pull aceest-fitness-app:previous
docker compose up -d

# Kubernetes rollback
kubectl rollout undo deployment aceest-fitness-app
kubectl rollout status deployment aceest-fitness-app
```

## 📈 Monitoring & Logging

### Health Checks

- Health endpoint: `/health`
- Database connectivity check
- Application status monitoring

### Recommended Monitoring Tools

- **Prometheus**: Metrics collection
- **Grafana**: Dashboards and visualization
- **ELK Stack**: Log aggregation and analysis
- **Sentry**: Error tracking and alerting

## 🔒 Security Best Practices

- Non-root container user
- Minimal base image (Python slim)
- Regular security scanning
- Dependency vulnerability checks
- Environment variable configuration
- No hardcoded credentials

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 Assignment Deliverables

This project addresses all requirements from the DevOps Assignment:

- ✅ Part A: Version Control Analysis
- ✅ Part B: CI/CD Pipeline Design
- ✅ Part C: Code Quality Assessment
- ✅ Part D: Deployment Strategy
- ✅ Part E: Monitoring and Maintenance

## 📖 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- Reference Implementation: https://github.com/TSG46/aceest-devops

## 📄 License

This project is part of an academic assignment for the Introduction to DevOps course.

## 👥 Author

**Name**: Govardhanan K S  
**Course**: Introduction to DevOps  
**Date**: March 2026  
**Institution**: BITS Pilani

---

**Note**: This is an educational project demonstrating DevOps practices for the ACEest Fitness Application case study.
