# CI/CD Pipeline Setup

This document explains the CI/CD pipeline for automated testing and deployment.

## Pipeline Overview

The CI/CD pipeline is implemented using GitHub Actions and consists of two main stages:

### 1. Continuous Integration (CI)
Runs on every push and pull request to `main` or `dockerize` branches.

**Steps:**
- ✅ Checkout code
- ✅ Set up Python 3.11
- ✅ Install dependencies
- ✅ Lint code with flake8 (optional)
- ✅ Run pytest tests with coverage
- ✅ Build Docker image
- ✅ Test Docker container

### 2. Continuous Deployment (CD)
Runs automatically after CI passes on push to `main` or `dockerize` branches.

**Steps:**
- ✅ Trigger Render deployment via webhook
- ✅ Send deployment notification

## Setup Instructions

### 1. Run Tests Locally

```powershell
# Install test dependencies
pip install pytest pytest-cov httpx

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=. --cov-report=term-missing

# Run specific test file
pytest tests/test_api.py -v
```

### 2. Configure GitHub Secrets

For automatic deployment to Render, you need to add a secret to your GitHub repository:

1. **Get Render Deploy Hook URL:**
   - Go to your Render service dashboard
   - Navigate to Settings > Deploy Hook
   - Copy the deploy hook URL (looks like: `https://api.render.com/deploy/srv-xxxxx?key=yyyyy`)

2. **Add to GitHub Secrets:**
   - Go to your GitHub repository
   - Settings > Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `RENDER_DEPLOY_HOOK_URL`
   - Value: Paste your Render deploy hook URL
   - Click "Add secret"

### 3. Workflow Triggers

The pipeline automatically runs when:
- Code is pushed to `main` or `dockerize` branch
- A pull request is opened/updated targeting `main` or `dockerize`

**Deployment** only happens on direct pushes (not PRs) to `main` or `dockerize`.

## CI/CD File Location

`.github/workflows/ci-cd.yml`

## Pipeline Stages Breakdown

### Build and Test Job
```yaml
- Checkout code
- Setup Python 3.11 with pip caching
- Install dependencies from requirements.txt
- Lint with flake8 (continues on error)
- Run pytest with coverage
- Build Docker image (tagged with commit SHA and latest)
- Test Docker container health
- Display Docker image info
```

### Deploy Job
```yaml
- Runs only after successful build-and-test
- Runs only on push to main/dockerize (not PRs)
- Triggers Render deployment via webhook
- Sends deployment notification
```

## Test Coverage

Current test suite covers:
- ✅ Home endpoint accessibility
- ✅ API documentation endpoint
- ✅ Valid prediction requests (approval/rejection)
- ✅ Input validation (credit score, age, income, etc.)
- ✅ Missing field handling
- ✅ Probability/confidence in responses

## Environment Variables for Tests

Tests use the following env vars (optional):
- `LOG_LEVEL=info` - Set logging level during tests

## Monitoring Pipeline

View pipeline status:
- GitHub repository > Actions tab
- See all workflow runs, logs, and results
- Failed builds will show error details

## Manual Deployment

If you need to deploy manually without pushing code:

```powershell
# Trigger via curl (replace with your deploy hook URL)
curl -X POST https://api.render.com/deploy/srv-xxxxx?key=yyyyy
```

Or use the "Re-run workflow" button in GitHub Actions.

## Troubleshooting

### Tests fail locally but pass in CI
- Ensure you have the same Python version (3.11)
- Install all test dependencies: `pip install -r requirements.txt pytest pytest-cov httpx`

### Docker build fails in CI
- Check Dockerfile syntax
- Ensure all files are committed (model files, templates, static, etc.)

### Deployment doesn't trigger
- Verify `RENDER_DEPLOY_HOOK_URL` secret is set correctly
- Check that you pushed to `main` or `dockerize` branch (not a PR)
- Review Actions logs for webhook response

### Render deployment fails after webhook
- Check Render dashboard logs
- Verify Dockerfile path is set correctly in Render service settings
- Ensure all required files are in the repository

## Adding More Tests

Add new test files to `tests/` directory:

```python
# tests/test_new_feature.py
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_new_feature():
    response = client.get("/new-endpoint")
    assert response.status_code == 200
```

Tests are automatically discovered and run by pytest.
