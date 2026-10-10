from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool 

@app.put('/product/{product_id}')
def update_product(
    product_id: int, 
    product: Product,
    discount:bool = False
):
    return {
        'product_id': product_id,
        'name': product.name,
        'price': product.price,
        'in_stock': product.in_stock,
        'discount': discount
    }