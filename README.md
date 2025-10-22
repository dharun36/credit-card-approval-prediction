# Credit Card Approval Prediction System

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A machine learning-powered web application that predicts credit card approval likelihood based on applicant information. Built with FastAPI, scikit-learn, and Docker for easy deployment.

## Features

- **Real-time Predictions**: Instant credit card approval predictions using ML model
- **Interactive Web Interface**: User-friendly form with validation
- **RESTful API**: Well-documented API endpoints with automatic Swagger docs
- **Docker Support**: Containerized application for consistent deployment
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- **Production Ready**: Deployed on Render with health checks and monitoring

## Table of Contents

- [Demo](#-demo)
- [Screenshots](#-screenshots)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Model Information](#-model-information)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## Demo

**Live Application**: [Coming Soon]

**API Documentation**: Access `/docs` endpoint for interactive Swagger UI

##  Screenshots

### Home Page
User-friendly form for entering applicant information with real-time validation.

### Prediction Results
- **Approved**: Clear indication with approval probability
- **Rejected**: Detailed rejection message with confidence score

## 🛠 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: Lightning-fast ASGI server
- **Pydantic**: Data validation using Python type annotations

### Machine Learning
- **scikit-learn**: ML model training and prediction
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **joblib**: Model serialization

### Frontend
- **HTML5/CSS3**: Responsive web interface
- **JavaScript (Vanilla)**: Form handling and API interaction
- **Jinja2**: Template engine

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD automation
- **Render**: Cloud deployment platform

### Testing
- **pytest**: Testing framework
- **httpx**: Async HTTP client for testing
- **pytest-cov**: Code coverage reporting

## Installation

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/dharun36/credit-card-approval-prediction.git
cd credit-card-approval-prediction
```

2. **Create virtual environment**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (optional)
```bash
# Copy example env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env with your settings
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
- Web Interface: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

### Docker Setup

1. **Build the Docker image**
```bash
docker build -t credit-card-approval .
```

2. **Run the container**
```bash
docker run -d -p 8000:8000 --name credit-app credit-card-approval
```

3. **Using Docker Compose** (recommended)
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 💻 Usage

### Web Interface

1. Navigate to http://127.0.0.1:8000
2. Fill in the application form:
   - **Prior Default History**: Has previous defaults (Yes/No)
   - **Credit Score**: 300-850
   - **Age**: 18-120 years
   - **Annual Income**: Total yearly income
   - **Current Debt**: Total outstanding debt
   - **Years Employed**: Employment duration
   - **Currently Employed**: Yes/No
3. Click "Predict Approval"
4. View the prediction result with confidence score

### API Usage

**Make a prediction via API:**

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "PriorDefault": 0,
    "CreditScore": 750,
    "YearsEmployed": 5.0,
    "Income": 60000.0,
    "Employed": 1,
    "Debt": 10000.0,
    "Age": 35
  }'
```

**Python example:**

```python
import requests

data = {
    "PriorDefault": 0,
    "CreditScore": 750,
    "YearsEmployed": 5.0,
    "Income": 60000.0,
    "Employed": 1,
    "Debt": 10000.0,
    "Age": 35
}

response = requests.post("http://127.0.0.1:8000/predict", json=data)
result = response.json()

print(f"Approval: {result['approval']}")
print(f"Confidence: {result['confidence']}")
```

## API Documentation

### Endpoints

#### `GET /`
Returns the main web interface (HTML page)

#### `GET /health`
Health check endpoint for monitoring
```json
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true
}
```

#### `POST /predict`
Make a credit card approval prediction

**Request Body:**
```json
{
  "PriorDefault": 0,      // 0 = No defaults, 1 = Has defaults
  "CreditScore": 750,     // 300-850
  "YearsEmployed": 5.0,   // >= 0
  "Income": 60000.0,      // >= 0
  "Employed": 1,          // 0 = No, 1 = Yes
  "Debt": 10000.0,        // >= 0
  "Age": 35               // 18-120
}
```

**Success Response (200 OK):**
```json
{
  "approval": true,
  "message": "Approved",
  "probability": 0.85,
  "confidence": "85.0%"
}
```

**Validation Error (400 Bad Request):**
```json
{
  "detail": "Credit score must be between 300 and 850"
}
```

### Validation Rules

| Field | Type | Range/Values | Description |
|-------|------|--------------|-------------|
| `PriorDefault` | int | 0 or 1 | Previous default history |
| `CreditScore` | float | 300-850 | Credit score |
| `Age` | int | 18-120 | Applicant age |
| `Income` | float | ≥ 0 | Annual income |
| `Debt` | float | ≥ 0 | Current debt |
| `Employed` | int | 0 or 1 | Employment status |
| `YearsEmployed` | float | ≥ 0 | Years of employment |

#### `GET /docs`
Interactive Swagger UI documentation

#### `GET /redoc`
Alternative ReDoc documentation

## Model Information

### Algorithm
- **Model Type**: Logistic Regression (scikit-learn)
- **Training Data**: Historical credit card application data
- **Features**: 7 input features (financial and personal information)
- **Output**: Binary classification (Approved/Rejected) with probability score

### Model Files
- `best_model.pkl`: Trained Logistic Regression model
- `scaler.pkl`: StandardScaler for feature normalization (optional)

### Performance Metrics
- Model accuracy and performance metrics available in training notebooks:
  - `credit-card-approval.ipynb`
  - `credit_card_approval_new.ipynb`

## Deployment

### Deploy to Render

1. **Fork/Clone this repository**

2. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Environment: Docker
   - Region: Choose closest to your users
   - Instance Type: Free or Starter

3. **Configure Environment Variables**
   ```
   PORT=8000
   LOG_LEVEL=info
   ALLOWED_ORIGINS=*
   ```

4. **Deploy**
   - Render will automatically build and deploy from Dockerfile
   - Health checks use `/health` endpoint
   - Auto-deploy on git push (optional)

**Detailed Deployment Guide**: See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

### Deploy with Docker

```bash
# Build image
docker build -t credit-card-approval .

# Run container
docker run -d \
  -p 8000:8000 \
  -e PORT=8000 \
  -e LOG_LEVEL=info \
  --name credit-app \
  credit-card-approval

# Check logs
docker logs credit-app

# Stop container
docker stop credit-app
```

### CI/CD Pipeline

Automated pipeline using GitHub Actions:
- Lint and code quality checks
- Run test suite with pytest
- Build Docker image
- Test Docker container
- Deploy to Render (optional)

**CI/CD Guide**: 
# CI/CD Pipeline Setup

This document explains the CI/CD pipeline for automated testing and deployment.

## Pipeline Overview

The CI/CD pipeline is implemented using GitHub Actions and consists of two main stages:

### 1. Continuous Integration (CI)
Runs on every push and pull request to `main` or `dockerize` branches.

**Steps:**
- Checkout code
- Set up Python 3.11
- Install dependencies
- Lint code with flake8 (optional)
- Run pytest tests with coverage
- Build Docker image
- Test Docker container

### 2. Continuous Deployment (CD)
Runs automatically after CI passes on push to `main` or `dockerize` branches.

**Steps:**
- Trigger Render deployment via webhook
- Send deployment notification

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
-  Home endpoint accessibility
-  API documentation endpoint
-  Valid prediction requests (approval/rejection)
-  Input validation (credit score, age, income, etc.)
-  Missing field handling
-  Probability/confidence in responses

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


## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::test_predict_valid_approval -v
```

### Test Coverage

- Unit tests for all API endpoints
- Validation testing for input data
- Integration tests for prediction pipeline
- Docker container health checks

### Test Files
- `tests/test_api.py`: API endpoint tests
- `test_predictions.py`: Manual testing script
- `quick_test.py`: Quick validation tests

## Project Structure

```
credit-card-approval-prediction/
│
├── app.py                          # Main FastAPI application
├── best_model.pkl                  # Trained ML model
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version for deployment
├── Procfile                        # Heroku deployment config
│
├── templates/                      # HTML templates
│   └── index.html                  # Main web interface
│
├── static/                         # Static files
│   └── css/
│       └── styles.css              # Application styles
│
├── tests/                          # Test suite
│   ├── __init__.py
│   └── test_api.py                 # API endpoint tests
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml               # GitHub Actions CI/CD
│
├── docker/                         # Docker configuration
│   ├── Dockerfile                  # Production Dockerfile
│   ├── .dockerignore              # Docker ignore file
│   └── docker-compose.yml         # Compose configuration
│
├── notebooks/                      # Jupyter notebooks
│   ├── credit-card-approval.ipynb
│   └── credit_card_approval_new.ipynb
│
├── data/                          # Data files
│   ├── clean_dataset.csv
│   └── data_df.csv
│
└── docs/                          # Documentation
    ├── README_DOCKER.md           # Docker setup guide
    ├── CI_CD_SETUP.md            # CI/CD documentation
    ├── DEPLOYMENT_CHECKLIST.md   # Deployment guide
    └── RENDER_TROUBLESHOOTING.md # Troubleshooting guide
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Server Configuration
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=info

# CORS Configuration - comma seperated
ALLOWED_ORIGINS=*

# Model Configuration
MODEL_PATH=best_model.pkl
SCALER_PATH=scaler.pkl

# Optional: Render Configuration
RENDER_EXTERNAL_URL=https://your-app.onrender.com
```

### Application Settings

Edit `app.py` to customize:
- CORS origins
- Model paths
- Logging level
- API configuration

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Author

**Dharun**
- GitHub: [@dharun36](https://github.com/dharun36)
- Repository: [credit-card-approval-prediction](https://github.com/dharun36/credit-card-approval-prediction)

##  Acknowledgments

- FastAPI for the excellent web framework
- scikit-learn for machine learning capabilities
- Render for cloud hosting
- GitHub Actions for CI/CD automation

## Support

If you have any questions or issues:

1. Check the [documentation](docs/)
2. Search [existing issues](https://github.com/dharun36/credit-card-approval-prediction/issues)
3. Create a [new issue](https://github.com/dharun36/credit-card-approval-prediction/issues/new)

## 🗺 Roadmap

- [ ] Add more ML models (Random Forest, XGBoost)
- [ ] Implement model retraining pipeline
- [ ] Add user authentication
- [ ] Create admin dashboard
- [ ] Implement A/B testing for models
- [ ] Add data visualization dashboard
- [ ] Support multiple languages
- [ ] Mobile app development

## 📊 Status

![Build Status](https://github.com/dharun36/credit-card-approval-prediction/workflows/CI%2FCD%20Pipeline/badge.svg)
![Deployment Status](https://img.shields.io/badge/Deployment-Active-success)
![Uptime](https://img.shields.io/badge/Uptime-99%25-brightgreen)

---



