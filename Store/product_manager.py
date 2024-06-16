from Store.json import DataManager
from Store.products.computer import Computer
from Store.products.phone import Phone
from Store.products.product import Product
from Store.products.tv import Tv


class ProductManager:
    def __init__(self):
        self.collection = {}
        self.sales = {"TV":0,"Computer":0,"Phone":0,"Accessories":0}
        self.currency = "ILS"
        self.sold_product ={}
        self.best_sell = None
        self.message = []
        self.new_update = 0
    def load_products(self):
        collection = DataManager.load_products()
        for product in collection:
            self.add_product(product)
        self.sales = DataManager.load_sales()
    def save_products(self):
        DataManager.save_products(self.collection)

    def add_product(self, product_dict):
        if product_dict.get("name") and product_dict.get("price") and product_dict.get("quantity"):
            product_type = product_dict.pop("product_type", None)
            if product_type == "Tv":
                new_product = Tv(**product_dict)
            elif product_type == "Computer":
                new_product = Computer(**product_dict)
            elif product_type == "Phone":
                new_product = Phone(**product_dict)
            else:
                new_product = Product(**product_dict)
            self.collection[new_product.get_key_name()] = new_product
            return True
        return False

    def remove_product(self, product):
        if product in self.collection.values():
            self.collection.pop(product.get_key_name())
            return True
        return False

    def search(self, name=None, product_type=None, model=None):
        found = []
        if name:
            cleaned_name = name.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if model:
            cleaned_model = model.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        for value in self.collection.values():
            if name:
                if value.get_key_name().casefold().startswith(cleaned_name.casefold()):
                    if model and value.get_model_name().casefold().startswith(cleaned_model.casefold()):
                        found.append(value)
                    else:
                        found.append(value)
            if product_type and not name:
                if (product_type == "1" and isinstance(value, Tv)) or \
                   (product_type == "2" and isinstance(value, Computer)) or \
                   (product_type == "3" and isinstance(value, Phone)) or \
                   (product_type == "4" and not isinstance(value, (Tv, Computer, Phone))):
                    found.append(value)
        return found

    def change_currency(self, currency):
        if currency != self.currency:
            self.currency = currency
            for product in self.collection.values():
                if product.currency != self.currency:
                    product.currency = self.currency

    def add_review(self, product, stars, review=None):
        if product in self.collection:
            self.collection[product].add_review(stars, review)
            return True
        return False




    def new_discount(self, items, discount):
        if 0 < discount < 100:
            if isinstance(items, list):
                for product in self.collection.values():
                    if product in items:
                        product.update_price(discount)
            elif isinstance(items, (Product, Tv, Computer, Phone)):
                items.update_price(discount)
                self.collection[items.get_key_name()] = items

    def remove_discount(self, item=None):
        if item:
            if isinstance(item, Product):
                item.remove_discount()
            else:
                for product in self.collection.values():
                    if isinstance(product, Product):
                        product.remove_discount()
            return True
        return False

    def list_products(self):
        if self.collection:
            return [(product.name, product.model, f"Price: {product.price} ₪", f"Available: {product.quantity}") for product in self.collection.values()]
        return "No products in inventory yet!"
