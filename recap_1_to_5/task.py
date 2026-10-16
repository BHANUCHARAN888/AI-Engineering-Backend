from fastapi import FastAPI

app = FastAPI()

data = {
    1: {"name": "BHANU", "department": "CSE"},
    2: {"name": "CHARAN", "department": "ECE"},
    3: {"name": "RAHUL", "department": "CSE"},
    4: {"name": "PRIYA", "department": "ECE"},
    5: {"name": "Pooji", "department": "CSD"}
}


@app.get("/student")
def get_all_stu(dept: str | None = None):
    if dept is None:
        return data

    filtered_students = {
        stu_id: student
        for stu_id, student in data.items()
        if student["department"].lower() == dept.lower()
    }

    return filtered_students