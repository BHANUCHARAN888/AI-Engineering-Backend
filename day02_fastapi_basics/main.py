from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, AI Engineer!"}

@app.get("/about")
def about():
    return {"message": "About pages:-)"}

@app.get("/status")
def status():
    return {"status": "API is running"}

@app.get("/ml")
def ml():
    return {"ml": "Machine Learning..."}

@app.get("/student/{student_id}")
def get_stu(student_id: int):
    return {
             "student_id": student_id,
             "name": "Bhanu charan kalla"
           }

@app.get("/courses/{course_id}")
def course(course_id: str):
    return {
        "course_id": course_id,
        "course": "Machine Learning"
    }
