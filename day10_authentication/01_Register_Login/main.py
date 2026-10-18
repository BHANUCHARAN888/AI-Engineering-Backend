from fastapi import FastAPI, HTTPException
from .schemas import UserRegister, UserLogin
from .security import hash_password, verify_password
from auth_common.jwt_service import create_access_token

app = FastAPI()

# Temporary storage for learning purposes
users = {}


@app.post("/register")
def register(user: UserRegister):
    if user.username in users:
       raise HTTPException(
        status_code=409,
        detail="Username already exists"
    )

    hashed_password = hash_password(user.password)

    users[user.username] = {
        "username": user.username,
        "hashed_password": hashed_password
    }

    return {
        "message": "User registered successfully",
        "username": user.username
    }

@app.post("/login")
def login(user: UserLogin):
    stored_user = users.get(user.username)

    if stored_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user.password,
        stored_user["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(user.username)
    return {
    "access_token": access_token,
    "token_type": "bearer"
}
