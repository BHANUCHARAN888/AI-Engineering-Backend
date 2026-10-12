
import os
import mysql.connector
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

app = FastAPI(
    title="Bookworm API",
    description="API for managing a personal book library.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ReadingStatus = Literal["Want to Read", "Reading", "Completed"]


class Book(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    author: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1, le=2100)
    status: ReadingStatus = "Want to Read"
    cover: str = ""


# Connect to MySQL using credentials from .env
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "bookworm_db"),
    )


# READ: Get all books
@app.get("/books")
def get_books():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, title, author, year, status, cover
            FROM books
            ORDER BY id
        """)

        result = cursor.fetchall()
        return {"books": result}

    except mysql.connector.Error as error:
         print("MYSQL ERROR:", repr(error))
         raise HTTPException(
             status_code=500,
             detail="Database error while fetching books"
    )

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()


# READ: Get one book
@app.get("/books/{book_id}")
def get_book(book_id: int):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, title, author, year, status, cover
            FROM books
            WHERE id = %s
            """,
            (book_id,)
        )

        book = cursor.fetchone()

        if book is None:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        return book

    except mysql.connector.Error:
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching book"
        )

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()


# CREATE: Add a book
@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO books (title, author, year, status, cover)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                book.title,
                book.author,
                book.year,
                book.status,
                book.cover,
            )
        )

        connection.commit()
        new_id = cursor.lastrowid

        return {"id": new_id, **book.model_dump()}

    except mysql.connector.Error:
        if "connection" in locals() and connection.is_connected():
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error while creating book"
        )

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()


# UPDATE: Replace a book
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE books
            SET title = %s,
                author = %s,
                year = %s,
                status = %s,
                cover = %s
            WHERE id = %s
            """,
            (
                book.title,
                book.author,
                book.year,
                book.status,
                book.cover,
                book_id,
            )
        )

        # Check existence separately, including when values are unchanged.
        cursor.execute(
            "SELECT id FROM books WHERE id = %s",
            (book_id,)
        )

        exists = cursor.fetchone()

        if exists is None:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        connection.commit()

        return {"id": book_id, **book.model_dump()}

    except mysql.connector.Error:
        if "connection" in locals() and connection.is_connected():
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error while updating book"
        )

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()


# DELETE: Remove a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM books WHERE id = %s",
            (book_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        connection.commit()

        return {
            "message": "Book deleted successfully",
            "id": book_id
        }

    except mysql.connector.Error:
        if "connection" in locals() and connection.is_connected():
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error while deleting book"
        )

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()
