from Store.product import Product
class Tv (Product):
    def __init__(self, name=None, model=None, description=None, price=None, quantity=None, size=None, tv_type =None,rate = None,sale = 0):
        super().__init__(name, model, description, price, quantity,rate,sale)
        self.size = size
        self.tv_type = tv_type


    def product_to_dict(self):
        dict = {
            "size": self.size,
            "tv_type": self.tv_type,
        }
        dict={**super().product_to_dict(),**dict}

        dict["product_type"] = "Tv"
        return dict
    def __str__(self):
        if self.sale >0:
            return f"======================================\nName: {self.name}\nModel: {self.model}\ndisplay size: {self.size}-Inch\nDescription: {self.description}\nPrice:-{self.sale}% Off {self.get_price(1)}₪ ILS\n{self.review()}"
        else:
            return f"======================================\nName: {self.name}\nModel: {self.model}\ndisplay size: {self.size}-Inch\nDescription: {self.description}\nPrice: {self.price}₪\n{self.review()}"