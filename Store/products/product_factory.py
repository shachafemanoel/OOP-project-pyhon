from Store.products.computer import Computer
from Store.products.phone import Phone
from Store.products.product import Product
from Store.products.tv import Tv
import logging

class ProductFactory:
    def __init__(self):
        self.product_classes = {
            "Computer": Computer,
            "Phone": Phone,
            "Tv": Tv,
            "Product" : Product
        }





    @staticmethod
    def get_product_type_by_choice(choice):
        category = ""
        if choice == "1":
            category = "Tv"
        elif choice == "2":
            category = "Computer"
        elif choice == "3":
            category = "Phone"
        elif choice == "4":
            category = "Product"
        else:
            raise ValueError("Invalid choice")
        return category.upper()

    """
    if admin want to create a new product type
    """


    def create_product(self, product_type, **kwargs):
        creator = self.product_classes.get(product_type.title())
        if not creator:
            raise ValueError(f"Unknown product type: {product_type}")
        return creator(**kwargs)

