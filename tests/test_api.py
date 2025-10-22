"""
Tests for the Credit Card Approval API
"""
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_home_endpoint():
    """Test the home page loads successfully"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_docs_endpoint():
    """Test that API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_predict_valid_approval():
    """Test prediction with valid data that should be approved"""
    payload = {
        "PriorDefault": 0,
        "CreditScore": 750,
        "YearsEmployed": 5.0,
        "Income": 60000.0,
        "Employed": 1,
        "Debt": 10000.0,
        "Age": 35
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "approval" in data
    assert "message" in data
    assert isinstance(data["approval"], bool)


def test_predict_valid_rejection():
    """Test prediction with valid data that should be rejected"""
    payload = {
        "PriorDefault": 1,
        "CreditScore": 350,
        "YearsEmployed": 0.5,
        "Income": 15000.0,
        "Employed": 0,
        "Debt": 50000.0,
        "Age": 22
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "approval" in data
    assert "message" in data


def test_predict_invalid_credit_score():
    """Test validation fails for invalid credit score"""
    payload = {
        "PriorDefault": 0,
        "CreditScore": 200,  # Below minimum 300
        "YearsEmployed": 5.0,
        "Income": 50000.0,
        "Employed": 1,
        "Debt": 15000.0,
        "Age": 35
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400


def test_predict_invalid_age():
    """Test validation fails for invalid age"""
    payload = {
        "PriorDefault": 0,
        "CreditScore": 700,
        "YearsEmployed": 5.0,
        "Income": 50000.0,
        "Employed": 1,
        "Debt": 15000.0,
        "Age": 15  # Below minimum 18
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400


def test_predict_invalid_prior_default():
    """Test validation fails for invalid PriorDefault value"""
    payload = {
        "PriorDefault": 2,  # Must be 0 or 1
        "CreditScore": 700,
        "YearsEmployed": 5.0,
        "Income": 50000.0,
        "Employed": 1,
        "Debt": 15000.0,
        "Age": 35
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400


def test_predict_negative_income():
    """Test validation fails for negative income"""
    payload = {
        "PriorDefault": 0,
        "CreditScore": 700,
        "YearsEmployed": 5.0,
        "Income": -5000.0,  # Negative income
        "Employed": 1,
        "Debt": 15000.0,
        "Age": 35
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400


def test_predict_missing_field():
    """Test that missing required field returns error"""
    payload = {
        "PriorDefault": 0,
        "CreditScore": 700,
        # Missing YearsEmployed
        "Income": 50000.0,
        "Employed": 1,
        "Debt": 15000.0,
        "Age": 35
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Unprocessable Entity


def test_predict_probability_in_response():
    """Test that probability is included in successful predictions"""
    payload = {
        "PriorDefault": 0,
        "CreditScore": 700,
        "YearsEmployed": 5.0,
        "Income": 50000.0,
        "Employed": 1,
        "Debt": 15000.0,
        "Age": 35
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    # If model supports predict_proba, these should be present
    if "probability" in data:
        assert isinstance(data["probability"], float)
        assert 0.0 <= data["probability"] <= 1.0
    if "confidence" in data:
        assert isinstance(data["confidence"], str)
        assert "%" in data["confidence"]
