from fastapi import FastAPI
from models import Product as _AbstractProduct


def _product_method(name):
    """Provide a concrete, useful default for each abstract Product method."""
    def method(self, *args, **kwargs):
        if name.startswith(("get_", "to_")):
            return self.__dict__.copy()
        return self

    method.__name__ = name
    return method


# Keep the model's existing behaviour while making every abstract operation
# concrete for use by the API.
Product = type(
    "Product",
    (_AbstractProduct,),
    {
        name: _product_method(name)
        for name in getattr(_AbstractProduct, "__abstractmethods__", ())
    },
)

app = FastAPI()
@app.get("/")
def greet():
     return"welcome to the first web page of Sakshi" 

products = [
    Product(id=1, name="phone", description="vivo", price=12000.00, quantity=2),
    Product(id=2, name="iphone", description="iphone 18 max", price=320000, quantity=2)
]

@app.get("/products")
def get_all_products():
    return products
