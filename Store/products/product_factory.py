from Store.products.computer import Computer
from Store.products.phone import Phone
from Store.products.product import Product
from Store.products.tv import Tv


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
            category = None
        return category.upper()