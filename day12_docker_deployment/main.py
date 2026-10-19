from fastapi import FastAPI
from config import settings

app = FastAPI(title=settings.app_name)

@app.get("/")
def home():
    return {
        "message": "My FastAPI app is running!",
        "app_name": settings.app_name,
        "environment": settings.app_env
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}