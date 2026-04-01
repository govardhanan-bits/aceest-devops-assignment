# ACEest DevOps - Quick Start Guide

## 🚀 Quick Start (3 Steps)

### Option 1: Docker (Recommended)

```bash
# 1. Build and start
docker compose up --build

# 2. Access application
# Open browser: http://localhost:5000
```

### Option 2: Local Python

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run application
python app.py

# 3. Access application
# Open browser: http://localhost:5000
```

---

## 📝 Test the Application

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-flask pytest-cov

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest --cov=app --cov-report=html
```

### Test API Endpoints

```bash
# Health check
curl http://localhost:5000/health

# Get application status
curl http://localhost:5000/

# Get all clients
curl http://localhost:5000/clients

# Get programs
curl http://localhost:5000/programs

# Get statistics
curl http://localhost:5000/stats

# Create new client
curl -X POST http://localhost:5000/clients \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","program":"Fat Loss","age":30,"goal":"Fitness"}'
```

---

## 🔍 API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Application status |
| GET | `/health` | Health check |
| GET | `/clients` | List all clients |
| GET | `/clients/<id>` | Get specific client |
| POST | `/clients` | Create new client |
| GET | `/programs` | List fitness programs |
| GET | `/stats` | Application statistics |

---

## 🐳 Docker Commands

```bash
# Build image
docker build -t aceest-app .

# Run container
docker run -d -p 5000:5000 aceest-app

# Check logs
docker logs <container-id>

# Stop container
docker stop <container-id>

# With docker-compose
docker compose up -d        # Start in background
docker compose logs -f      # Follow logs
docker compose down         # Stop and remove
docker compose ps           # List services
```

---

## 🧪 Code Quality Checks

```bash
# Format code
black app.py tests/

# Lint code
flake8 app.py

# Security scan
bandit -r app.py

# Run all quality checks
black --check app.py && \
flake8 app.py && \
pylint app.py && \
bandit -r app.py
```

---

## 📊 View Test Coverage

```bash
# Generate HTML coverage report
python -m pytest --cov=app --cov-report=html

# Open report in browser
open htmlcov/index.html    # macOS
# or
xdg-open htmlcov/index.html    # Linux
```

---

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Docker Build Issues

```bash
# Clean build
docker compose down
docker system prune -a
docker compose up --build
```

### Database Permission Issues

```bash
# Fix data directory permissions
chmod -R 755 data/
```

### Module Not Found

```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── README.md             # Full documentation
├── QUICK_START.md        # This file
├── ASSIGNMENT_SUBMISSION.md  # Assignment summary
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # CI/CD pipeline
├── tests/
│   ├── __init__.py
│   └── test_app.py       # Test suite
└── data/
    └── aceest_fitness.db # SQLite database
```

---

## 🎯 Common Tasks

### Add New Test

1. Open `tests/test_app.py`
2. Add test function with `test_` prefix
3. Run tests: `python -m pytest tests/ -v`

### Modify API Endpoint

1. Edit `app.py`
2. Run tests: `python -m pytest`
3. Test manually: `curl http://localhost:5000/<endpoint>`

### Deploy Changes

1. Commit changes: `git add . && git commit -m "message"`
2. Push to GitHub: `git push origin main`
3. CI/CD pipeline runs automatically
4. Check GitHub Actions tab for status

---

## 📚 Additional Resources

- **Full Documentation**: See [README.md](README.md)
- **Assignment Details**: See [ASSIGNMENT_SUBMISSION.md](ASSIGNMENT_SUBMISSION.md)
- **Reference Implementation**: https://github.com/TSG46/aceest-devops
- **Flask Docs**: https://flask.palletsprojects.com/
- **Docker Docs**: https://docs.docker.com/

---

## ✅ Verify Installation

```bash
# Check Python version (3.10+)
python --version

# Check Docker
docker --version

# Check Docker Compose
docker compose version

# Run complete verification
python -m pytest tests/ -v && \
docker compose up -d && \
curl http://localhost:5000/health && \
docker compose down
```

If all commands succeed, your environment is ready! 🎉

---

**Need Help?** Check the full README.md or the assignment submission document for detailed information.
