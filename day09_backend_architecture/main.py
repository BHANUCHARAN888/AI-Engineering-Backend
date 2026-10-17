from fastapi import FastAPI
from routers.expenses import router as expenses_router

app = FastAPI(title="Expense Tracker API")



@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}


app.include_router(expenses_router)
