from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from auth_common.jwt_service import verify_access_token

app = FastAPI()
bearer_scheme = HTTPBearer()


@app.get("/verify-token")
def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials

    try:
        payload = verify_access_token(token)
        return {
            "message": "Token is valid",
            "username": payload["sub"]
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )