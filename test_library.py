import requests

BASE = "http://127.0.0.1:8000"


# Boundary Value Analysis on registration age (Rule 1: 12-120 inclusive)
# 11 = just below (invalid), 12 = lower boundary (valid),
# 120 = upper boundary (valid), 121 = just above (invalid)
def test_age_11_rejected():
    r = requests.post(f"{BASE}/members", json={"name": "Low", "age": 11})
    assert r.status_code == 400

def test_age_12_accepted():
    r = requests.post(f"{BASE}/members", json={"name": "LowEdge", "age": 12})
    assert r.status_code == 201

def test_age_120_accepted():
    r = requests.post(f"{BASE}/members", json={"name": "HighEdge", "age": 120})
    assert r.status_code == 201

def test_age_121_rejected():
    r = requests.post(f"{BASE}/members", json={"name": "High", "age": 121})
    assert r.status_code == 400