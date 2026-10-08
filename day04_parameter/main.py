from fastapi import FastAPI
app = FastAPI()

@app.get('/student/{student_id}')
def get_student(student_id: int):
    return {
        "student_id": student_id
    }

@app.get('/products/{product_id}')
def get_product(product_id: int):
    return {
        "product_id": product_id,
        "product": "Laptop"
    }   

@app.get('/products')
def geta_products(category: str):
    return {
        "category": category
    }

@app.get('/course')
def get_course(cname: str, level: str="beginner"):
    return {
        "Course": cname,
        "level": level
    }