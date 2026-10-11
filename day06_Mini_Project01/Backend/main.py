
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Bookworm API",
    description="API for managing a personal book library.",
    version="1.0.0"
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

# =========================
# 1. Book schema
# =========================

ReadingStatus = Literal["Want to Read", "Reading", "Completed"]


class Book(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    author: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1, le=2100)
    status: ReadingStatus = "Want to Read"
    cover: str = ""


# =========================
# 2. Temporary storage
# =========================

books = {
    1: {
        "title": "Atomic Habits",
        "author": "James Clear",
        "year": 2018,
        "status": "Completed",
        "cover": "https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg"
    },
    2: {
        "title": "Deep Work",
        "author": "Cal Newport",
        "year": 2016,
        "status": "Reading",
        "cover": "https://covers.openlibrary.org/b/isbn/9781455586691-L.jpg"
    },
    3: {
        "title": "Avengers",
        "author": "Stephen",
        "year": 2015,
        "status": "Want to Read",
        "cover": ""
    }
}


# =========================
# 3. READ: Get all books
# =========================

@app.get("/books")
def get_books():
    return {
        "books": [
            {"id": book_id, **book}
            for book_id, book in books.items()
        ]
    }


# =========================
# 4. READ: Get one book
# =========================

@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return {"id": book_id, **books[book_id]}


# =========================
# 5. CREATE: Add a book
# =========================

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    new_id = max(books.keys(), default=0) + 1
    books[new_id] = book.model_dump()

    return {"id": new_id, **books[new_id]}


# =========================
# 6. UPDATE: Replace a book
# =========================

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    books[book_id] = book.model_dump()

    return {"id": book_id, **books[book_id]}


# =========================
# 7. DELETE: Remove a book
# =========================

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    del books[book_id]

    return {
        "message": "Book deleted successfully",
        "id": book_id
    }
