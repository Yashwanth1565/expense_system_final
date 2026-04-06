from pydantic import BaseModel
from datetime import date


class ExpenseCreate(BaseModel):
    employee_name: str
    amount: float
    category: str
    description: str


class Expense(BaseModel):
    id: int
    employee_name: str
    amount: float
    category: str
    description: str
    status: str
    date: date

    class Config:
        orm_mode = True