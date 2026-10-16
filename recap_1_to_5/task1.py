from fastapi import FastAPI
app = FastAPI()

products = {
    1: {"name": "Keyboard", "category": "electronics", "price": 1200},
    2: {"name": "Notebook", "category": "stationery", "price": 80},
    3: {"name": "Mouse", "category": "electronics", "price": 600}
}

@app.get("/product")
def get_product(category: str | None = None):
    if category is None:
        return products

    filtered_products = {
        p_id: product
        for p_id, product in products.items()
        if product["category"].lower() == category.lower()
    }

    return filtered_products