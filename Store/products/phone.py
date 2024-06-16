from Store.products.product import Product


class Phone(Product):
    def __init__(self, name, model, description, price, quantity, size=None, storage=None,
                 rate=None,):
        super().__init__(name, model, description, price, quantity, rate)
        self.size = size
        self.storage = storage

    def product_to_dict(self):
        dict = {
            "size": self.size,
            "storage": self.storage,
        }

        dict = {**super().product_to_dict(), **dict}

        dict["product_type"] = "Phone"
        return dict

    def product_type(self):
        return "PHONE"
    def __str__(self):
        return f"======================================\nName: {self.name}\nModel: {self.model} Storge: {self.storage}\ndisplay size: {self.size}-Inch\nDescription: {self.description}\n{self.get_price_in_user_currency()}\n{self.rate}"
