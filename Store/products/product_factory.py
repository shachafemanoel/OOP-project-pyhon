from Store.products.product import Product
from Store.products.tv import Tv
from Store.products.computer import Computer
from Store.products.phone import Phone

class ProductFactory:
    @staticmethod
    def create_product(product_type, name, model, description, price, quantity, **kwargs):
        if product_type.lower() == "tv":
            return Tv(name, model, description, price, quantity, **kwargs)
        elif product_type.lower() == "computer":
            return Computer(name, model, description, price, quantity, **kwargs)
        elif product_type.lower() == "phone":
            return Phone(name, model, description, price, quantity, **kwargs)
        else:
            return Product(name, model, description, price, quantity, **kwargs)
