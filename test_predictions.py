"""
Test script to demonstrate valid rejection vs invalid input
Run with: .venv\Scripts\python.exe test_predictions.py
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("TESTING CREDIT CARD APPROVAL API")
print("=" * 60)

# Test 1: Valid input that SHOULD BE APPROVED
print("\n1️⃣  TEST: Valid input - Should be APPROVED")
print("-" * 60)
approved_data = {
    "PriorDefault": 0,
    "CreditScore": 750,
    "YearsEmployed": 5.0,
    "Income": 60000.0,
    "Employed": 1,
    "Debt": 10000.0,
    "Age": 35
}
print(f"Request: {json.dumps(approved_data, indent=2)}")
response = requests.post(f"{BASE_URL}/predict", json=approved_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Valid input that SHOULD BE REJECTED
print("\n2️⃣  TEST: Valid input - Should be REJECTED")
print("-" * 60)
rejected_data = {
    "PriorDefault": 1,  # Has prior default
    "CreditScore": 350,  # Low credit score (but valid range 300-850)
    "YearsEmployed": 0.5,
    "Income": 15000.0,
    "Employed": 0,  # Unemployed
    "Debt": 50000.0,  # High debt
    "Age": 22
}
print(f"Request: {json.dumps(rejected_data, indent=2)}")
response = requests.post(f"{BASE_URL}/predict", json=rejected_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: INVALID input - Credit score too low
print("\n3️⃣  TEST: Invalid input - Credit score below 300")
print("-" * 60)
invalid_credit = {
    "PriorDefault": 0,
    "CreditScore": 200,  # INVALID: Below 300
    "YearsEmployed": 5.0,
    "Income": 50000.0,
    "Employed": 1,
    "Debt": 10000.0,
    "Age": 35
}
print(f"Request: {json.dumps(invalid_credit, indent=2)}")
response = requests.post(f"{BASE_URL}/predict", json=invalid_credit)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 4: INVALID input - Age too young
print("\n4️⃣  TEST: Invalid input - Age below 18")
print("-" * 60)
invalid_age = {
    "PriorDefault": 0,
    "CreditScore": 700,
    "YearsEmployed": 0.5,
    "Income": 25000.0,
    "Employed": 1,
    "Debt": 5000.0,
    "Age": 15  # INVALID: Below 18
}
print(f"Request: {json.dumps(invalid_age, indent=2)}")
response = requests.post(f"{BASE_URL}/predict", json=invalid_age)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 5: INVALID input - Negative income
print("\n5️⃣  TEST: Invalid input - Negative income")
print("-" * 60)
invalid_income = {
    "PriorDefault": 0,
    "CreditScore": 700,
    "YearsEmployed": 5.0,
    "Income": -5000.0,  # INVALID: Negative
    "Employed": 1,
    "Debt": 10000.0,
    "Age": 35
}
print(f"Request: {json.dumps(invalid_income, indent=2)}")
response = requests.post(f"{BASE_URL}/predict", json=invalid_income)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("✅ 200 OK = Valid input (whether approved or rejected)")
print("❌ 400 Bad Request = Invalid input (validation failed)")
print("❌ 500 Internal Server Error = Server error")
print("=" * 60)
