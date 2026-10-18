from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from auth_common.jwt_service import create_access_token, verify_access_token
from pwdlib import PasswordHash

app = FastAPI()
bearer_scheme = HTTPBearer()
password_hash = PasswordHash.recommended()

# Temporary storage for learning only
users = {}


class UserRegister(BaseModel):
    username: str
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    try:
        payload = verify_access_token(credentials.credentials)
        username = payload.get("sub")

        if not username:
            raise ValueError("Missing username")

        return username
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.post("/register")
def register(user: UserRegister):
    if user.username in users:
        raise HTTPException(status_code=409, detail="Username already exists")

    users[user.username] = {
        "username": user.username,
        "hashed_password": password_hash.hash(user.password),
    }
    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: UserLogin):
    stored_user = users.get(user.username)

    if stored_user is None or not password_hash.verify(
        user.password, stored_user["hashed_password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "access_token": create_access_token(user.username),
        "token_type": "bearer",
    }


@app.get("/me")
def read_my_profile(current_user: str = Depends(get_current_user)):
    return {"username": current_user, "message": "Access granted"}


@app.get("/users/{username}/profile")
def read_user_profile(
    username: str,
    current_user: str = Depends(get_current_user),
):
    if username != current_user:
        raise HTTPException(status_code=403, detail="Access denied")

    return {"username": current_user, "message": "Access granted"}