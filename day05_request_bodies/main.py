# understanding pydantic model properly
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    course: str

@app.post("/students")
def create_student(student: Student):
    return {
        "name":student.name,
        "age":student.age,
        "course":student.course
    }

class Employee(BaseModel):
    name: str
    age: int
    role: str

@app.post('/employee')
def employee_details(employee: Employee):
    return {
        "name":employee.name,
        "age":employee.age,
        "role":employee.role
    }