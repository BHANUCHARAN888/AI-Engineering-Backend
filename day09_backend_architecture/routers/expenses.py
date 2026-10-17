from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_connection

router = APIRouter(prefix="/expenses", tags=["Expenses"])


class Expense(BaseModel):
    title: str
    amount: float
    category: str


@router.get("/")
def get_all_expenses():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM expenses")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

@router.get("/summary")
def get_expense_summary():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                COUNT(*) AS total_expenses,
                COALESCE(SUM(amount), 0) AS total_amount
            FROM expenses
        """)

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()

@router.get("/{expense_id}")
def get_expense(expense_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM expenses WHERE expense_id = %s",
            (expense_id,)
        )
        expense = cursor.fetchone()

        if expense is None:
            raise HTTPException(status_code=404, detail="Expense not found")

        return expense
    finally:
        cursor.close()
        connection.close()


@router.post("/", status_code=201)
def create_expense(expense: Expense):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO expenses (title, amount, category)
            VALUES (%s, %s, %s)
        """
        values = (expense.title, expense.amount, expense.category)

        cursor.execute(query, values)
        connection.commit()

        return {
            "expense_id": cursor.lastrowid,
            **expense.model_dump()
        }
    finally:
        cursor.close()
        connection.close()


@router.put("/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE expenses
            SET title = %s, amount = %s, category = %s
            WHERE expense_id = %s
            """,
            (expense.title, expense.amount, expense.category, expense_id)
        )
        connection.commit()

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT expense_id FROM expenses WHERE expense_id = %s",
                (expense_id,)
            )
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Expense not found")

        return {"expense_id": expense_id, **expense.model_dump()}
    finally:
        cursor.close()
        connection.close()


@router.delete("/{expense_id}")
def delete_expense(expense_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_id = %s",
            (expense_id,)
        )
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Expense not found")

        return {"message": "Expense deleted successfully"}
    finally:
        cursor.close()
        connection.close()

