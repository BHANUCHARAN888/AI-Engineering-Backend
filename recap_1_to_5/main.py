from fastapi import FastAPI, HTTPException, Request
app = FastAPI()

data = {
    1: {'name': 'BHANU'},
    2: {'name': 'CHARAN'}
}
@app.get("/student/{stu_id}")
def student(stu_id: int):
    if stu_id not in data:
        raise HTTPException(status_code=404, detail="Student Not Found")
    return {
        "Student_id": stu_id,
        "Name": data[stu_id]['name']
    }