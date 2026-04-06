from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend import models, crud, schemas
from backend.database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Expense API running 🚀"}


@app.post("/expenses/")
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)


@app.get("/expenses/")
def read_expenses(db: Session = Depends(get_db)):
    return crud.get_expenses(db)


@app.put("/expenses/{expense_id}/status")
def update_expense(expense_id: int, status: dict, db: Session = Depends(get_db)):
    return crud.update_status(db, expense_id, status["status"])


@app.get("/dashboard/")
def dashboard(db: Session = Depends(get_db)):
    expenses = crud.get_expenses(db)

    total = len(expenses)
    approved = len([e for e in expenses if e.status == "Approved"])
    rejected = len([e for e in expenses if e.status == "Rejected"])
    pending = len([e for e in expenses if e.status == "Pending"])

    return {
        "total": total,
        "approved": approved,
        "rejected": rejected,
        "pending": pending
    }