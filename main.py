

from fastapi import FastAPI
from pydantic import BaseModel
from models import Product as _AbstractProduct
from database import session , engine 
import database_models   


def _product_method(name):
    """Provide a concrete, useful default for each abstract Product method."""
    def method(self, *args, **kwargs):
        if name.startswith(("get_", "to_")):
            return self.__dict__.copy()
        return self

    method.__name__ = name
    return method


# Generate the dictionary of fallback methods for the abstract definitions
abstract_overrides = {
    name: _product_method(name)
    for name in getattr(_AbstractProduct, "__abstractmethods__", ())
}

app = FastAPI()

data_model.metadata.create_all(bind=database_models.engine)  # Create tables in the database


@app.get("/")
def greet():
    return "welcome to the first web page of Sakshi"


# This now successfully registers the Pydantic parser fields!
products = [
    _AbstractProduct(id=1, name="phone", description="vivo", price=12000.00, quantity=2),
    _AbstractProduct(id=2, name="iphone", description="iphone 18 max", price=320000, quantity=2),
    _AbstractProduct(id=3, name="charger", description="moto90", price=1200, quantity=20),
    _AbstractProduct(id=4, name="headphone", description="ipod", price=3200, quantity=29),
]
def __init__db():
    for product in products:
        db.add(database_models.Product(**product.model_dump()))  # Use model_dump() to convert Pydantic model to dictionary
    db.commit()
@app.get("/products")
def get_all_products():
    db = session()
    return products


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"error": "Product not found"} 
  
@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product  

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: _AbstractProduct):
    for index, product in enumerate(products):
        if product.id == product_id:
            products[index] = updated_product
            return updated_product
    return {"error": "Product not found"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product.id == product_id:
            deleted_product = products.pop(index)
            return deleted_product
    return {"error": "Product not found"}
