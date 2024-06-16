from Store.products.product import Product


class Tv(Product):
    def __init__(self, name, model, description, price, quantity, size=None, tv_type=None,
                 rate=None):
        super().__init__(name, model, description, price, quantity, rate)
        self.size = size
        self.tv_type = tv_type

    def product_to_dict(self):
        dict = {
            "size": self.size,
            "tv_type": self.tv_type,
        }
        dict = {**super().product_to_dict(), **dict}

        dict["product_type"] = "Tv"
        return dict

    def product_type(self):
        return "TV"

    def __str__(self):
        return f"======================================\nName: {self.name}\nModel: {self.model}\ndisplay size: {self.size}-Inch\nDescription: {self.description}\n {self.get_price_in_user_currency()}\n{self.rate}"
