from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    course: str
@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: Student,
    notify: bool = False,
):
    return {
        'student_id': student_id,
        'name': student.name,
        'age': student.age,
        'course': student.course,
        'notify': notify
    }
