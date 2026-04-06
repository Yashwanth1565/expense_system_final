from sqlalchemy.orm import Session
from backend import models, schemas


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session):
    return db.query(models.Expense).all()


def update_status(db: Session, expense_id: int, status: str):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if expense:
        expense.status = status
        db.commit()
        db.refresh(expense)
    return expense