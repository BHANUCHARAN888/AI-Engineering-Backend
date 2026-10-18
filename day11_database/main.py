from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from database import SessionLocal
from models import User
from schemas import UserCreate, UserResponse

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user.username) |
        (User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )

    new_user = User(
        username=user.username,
        email=str(user.email)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@app.get("/users", response_model=list[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    username: str | None = None,
    email: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if username:
        query = query.filter(User.username == username)

    if email:
        query = query.filter(User.email == email)

    users = query.offset(skip).limit(limit).all()
    return users



@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    updated_data: UserCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    duplicate = db.query(User).filter(
        ((User.username == updated_data.username) |
         (User.email == str(updated_data.email))) &
        (User.id != user_id)
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )

    user.username = updated_data.username
    user.email = str(updated_data.email)

    db.commit()
    db.refresh(user)

    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}