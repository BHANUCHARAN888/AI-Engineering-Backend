from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def new():
    return {
        "msg":"Hello API"
    }

@app.post("/new")
def create_student():
    return {
        "msg":"Student created"
    }
@app.put("/new/101")
def update_student():
    return {
        "msg":"Student updated"
    }
@app.patch("/new/101")
def update_student():
    return {
        "msg":"Student course updated"
    }
@app.delete("/students/101")
def delete_student():
    return {
        "message": "Student deleted"
    }