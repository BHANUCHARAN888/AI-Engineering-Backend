from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth_common.jwt_service import verify_access_token

app = FastAPI()
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials
    payload = verify_access_token(token)
    return payload["sub"]


@app.get("/profile")
def profile(username: str = Depends(get_current_user)):
    return {
        "message": "Access granted",
        "username": username
    }