import requests

BASE = "http://127.0.0.1:8000"


def register(name, age):
    return requests.post(f"{BASE}/members", json={"name": name, "age": age})


# Rule 1: age must be 12-120 inclusive (boundary value analysis, 2-value)
def test_age_11_is_rejected():
    assert register("Test", 11).status_code == 400


def test_age_12_is_accepted():
    assert register("Test", 12).status_code == 201


def test_age_120_is_accepted():
    assert register("Test", 120).status_code == 201


def test_age_121_is_rejected():
    assert register("Test", 121).status_code == 400


# Rule 3: a book already on loan to ONE member must not be borrowable by ANOTHER member.
# This test found defect D-01 (see README).
def test_same_book_cannot_be_loaned_to_two_members():
    m1 = register("Alice", 30).json()["id"]
    m2 = register("Bob", 30).json()["id"]

    r1 = requests.post(f"{BASE}/loans", json={"member": m1, "book": "shared-1"})
    assert r1.status_code == 201

    r2 = requests.post(f"{BASE}/loans", json={"member": m2, "book": "shared-1"})
    assert r2.status_code == 400
