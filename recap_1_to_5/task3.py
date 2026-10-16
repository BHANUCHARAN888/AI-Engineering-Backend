from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Job Application Tracker API")

# Request body validation
class Application(BaseModel):
    company: str
    role: str

# Temporary in-memory storage
applications = {
    1: {"company": "Google", "role": "AI Engineer"},
    2: {"company": "Microsoft", "role": "Backend Intern"}
}

# Service health check
@app.get("/")
def home():
    return {"message": "Job Application Tracker API is running"}

# Retrieve all applications
@app.get("/applications")
def get_applications():
    return applications

# Retrieve one application
@app.get("/applications/{application_id}")
def get_application(application_id: int):
    if application_id not in applications:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return {
        "application_id": application_id,
        **applications[application_id]
    }

# Create an application
@app.post("/applications", status_code=201)
def create_application(application: Application):
    application_id = max(applications.keys(), default=0) + 1

    applications[application_id] = application.model_dump()

    return {
        "application_id": application_id,
        **applications[application_id],
        "message": "Application created successfully"
    }