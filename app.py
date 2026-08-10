from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- In-memory "database" (resets when the app restarts) ---
members = {}      # member_id -> {"name", "age"}
loans = {}        # member_id -> set of book ids currently on loan
next_member_id = 1


# --- Request shapes ---
class MemberIn(BaseModel):
    name: str
    age: int

class LoanIn(BaseModel):
    member: int
    book: str


# --- Rule 1: age must be 12–120 inclusive to register ---
@app.post("/members", status_code=201)
def create_member(m: MemberIn):
    global next_member_id
    if m.age < 12 or m.age > 120:
        raise HTTPException(status_code=400, detail="Age must be 12-120 inclusive")
    member_id = next_member_id
    members[member_id] = {"name": m.name, "age": m.age}
    loans[member_id] = set()
    next_member_id += 1
    return {"id": member_id, "name": m.name, "age": m.age}


# --- Rule 2: max 3 active loans.  Rule 3: a book on loan can't be re-borrowed ---
@app.post("/loans", status_code=201)
def create_loan(l: LoanIn):
    if l.member not in members:
        raise HTTPException(status_code=404, detail="Member not found")
    if len(loans[l.member]) >= 3:
        raise HTTPException(status_code=400, detail="Max 3 active loans")
    if l.book in loans[l.member]:
        raise HTTPException(status_code=400, detail="Book already on loan")
    loans[l.member].add(l.book)
    return {"member": l.member, "book": l.book, "status": "on_loan"}


# --- Return a book (Rule 3: makes it available again) ---
@app.post("/returns", status_code=201)
def return_book(l: LoanIn):
    if l.member not in members:
        raise HTTPException(status_code=404, detail="Member not found")
    if l.book not in loans[l.member]:
        raise HTTPException(status_code=400, detail="That book is not on loan")
    loans[l.member].discard(l.book)
    return {"member": l.member, "book": l.book, "status": "returned"}


@app.get("/members/{member_id}/loans")
def list_loans(member_id: int):
    if member_id not in members:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"member": member_id, "active_loans": sorted(loans[member_id])}