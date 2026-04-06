from sqlalchemy import Column, Integer, String, Float, Date
from backend.database import Base
from datetime import date


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, index=True)
    amount = Column(Float)
    category = Column(String)
    description = Column(String)
    status = Column(String, default="Pending")
    date = Column(Date, default=date.today)