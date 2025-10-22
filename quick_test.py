import requests

# Test rejection with VALID input (should get 200 OK)
print("Testing REJECTION with valid input...")
data = {
    "PriorDefault": 1,
    "CreditScore": 350,
    "YearsEmployed": 0.5,
    "Income": 15000.0,
    "Employed": 0,
    "Debt": 50000.0,
    "Age": 22
}
r = requests.post("http://127.0.0.1:8000/predict", json=data)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}\n")

# Test with INVALID input (should get 400)
print("Testing with INVALID credit score...")
data2 = {
    "PriorDefault": 0,
    "CreditScore": 200,  # Invalid!
    "YearsEmployed": 5.0,
    "Income": 50000.0,
    "Employed": 1,
    "Debt": 10000.0,
    "Age": 35
}
r2 = requests.post("http://127.0.0.1:8000/predict", json=data2)
print(f"Status: {r2.status_code}")
print(f"Response: {r2.json()}")
