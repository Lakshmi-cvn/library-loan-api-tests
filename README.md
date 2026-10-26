# library-loan-api-tests

Automated test suite for a small library loan REST API, written in Python with pytest.

## What is in this repo

- `app.py` - the API under test (FastAPI, in-memory data).
- `test_library.py` - pytest tests that call the API with `requests`.
- `test_first.py` - my first pytest practice file.

## Business rules tested

1. A member must be aged 12 to 120 (inclusive) to register.
2. A member can have at most 3 active loans.
3. A book already on loan cannot be borrowed again until it is returned.

## How to run

1. Install: `pip install fastapi uvicorn requests pytest`
2. Start the API in one terminal: `uvicorn app:app --reload --port 8000`
3. Run the tests in a second terminal: `pytest -v`

## Defects found

| ID | Title | Steps to reproduce | Expected | Actual | Severity | Priority | Status |
|----|-------|--------------------|----------|--------|----------|----------|--------|
| D-01 | Same book can be loaned to two members at once | 1. Register member A. 2. Register member B. 3. A borrows book "x" (201). 4. B borrows book "x". | B's request rejected with 400 (book already on loan, rule 3) | B's request accepted with 201; both members hold the same book | Medium | Medium | Fixed |

**Cause of D-01:** the code only checked the borrowing member's own loans, not all loans. **Fix:** added a global set of loaned books (`all_loaned_books`) that is checked on loan and updated on return. **Verified:** `test_same_book_cannot_be_loaned_to_two_members` failed before the fix and passes after it, and the other tests still pass (regression check).

## Still to do

- Tests for rule 2 (maximum 3 active loans) and the return endpoint.
- Run the tests automatically on every push (CI).
