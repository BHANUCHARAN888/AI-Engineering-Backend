from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth_common.jwt_service import verify_access_token

app = FastAPI()
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    try:
        payload = verify_access_token(credentials.credentials)
        return payload["sub"]
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


@app.get("/users/{username}/profile")
def get_profile(
    username: str,
    current_user: str = Depends(get_current_user)
):
    if username != current_user:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's profile"
        )

    return {
        "message": "Access granted",
        "profile": {
            "username": current_user
        }
    }