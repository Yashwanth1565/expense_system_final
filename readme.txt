# 💰 Expense Approval System

## Overview
This is an **Expense Approval System** where employees can submit expenses, and managers can approve or reject them.  
The system ensures **status tracking**, **validation**, and **easy reporting**.

## Features
- Employees can:
  - Submit new expenses
  - View all expenses
  - Update/Delete only pending expenses
- Managers can:
  - Approve or reject expenses
- Automatic status tracking: `Pending → Approved/Rejected`
- Export data to CSV and Excel


## Tech Stack & Importance
| Technology | Role in Project |
|------------|----------------|
| **FastAPI** | Backend framework to create APIs for CRUD operations and status updates |
| **Pydantic** | Validates input data (e.g., positive amounts, required fields) to prevent invalid entries |
| **SQLAlchemy** | ORM to interact with PostgreSQL using Python objects for smooth database operations |
| **PostgreSQL** | Stores all expense data securely, enabling queries, filtering, and analytics |
| **Streamlit** | Frontend interface for employees and managers with interactive forms and dashboards |
| **Plotly Express** | Visualizes analytics (pie charts and bar charts) for expense distribution and categories |

---

## Validation Rules
- Amount must be positive
- Fields cannot be empty
- Only `Pending` expenses can be updated or deleted
- `Approved`/`Rejected` expenses are immutable






