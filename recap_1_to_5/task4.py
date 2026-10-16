from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
expenses_data = {
    1: {"title": "Groceries", "amount": 370.0, "category": "Food"},
    2: {"title": "Movie Tickets", "amount": 250.0, "category": "Entertainment"}
}

class Expense(BaseModel):
    title: str
    amount: float
    category: str

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}
@app.get("/expenses")
def get_all_expenses():
    return expenses_data

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    if expense_id not in expenses_data:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    return {
        "expense_id": expense_id,
        **expenses_data[expense_id]
    }

@app.post("/expenses", status_code=201)
def create_expense(expense: Expense):
    expense_id = max(expenses_data.keys(), default=0) + 1
    expenses_data[expense_id] = expense.model_dump()
    return {
        "expense_id": expense_id,
        **expenses_data[expense_id]
    }
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    if expense_id not in expenses_data:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    expenses_data[expense_id] = expense.model_dump()
    return {
        "expense_id": expense_id,
        **expenses_data[expense_id]
    }
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    if expense_id not in expenses_data:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    del expenses_data[expense_id]
    return {"message": "Expense deleted successfully"}