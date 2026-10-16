from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

class Registration(BaseModel):
    student_name: str
    age: int
    course: str
    is_paid: bool = False

@app.post("/register")
def register_student(registration: Registration):
    if registration.age < 18:
        raise HTTPException(status_code=400, detail="Student must be at least 18 years old to register.")
    return {
        'student_name': registration.student_name,
        'age': registration.age,
        'course': registration.course,
        'is_paid': registration.is_paid
    }