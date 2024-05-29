from Store.product import Product
class Tv (Product):
    def __init__(self, name=None, model=None, description=None, price=None, quantity=None, size=None, tv_type =None,rate = None):
        super().__init__(name, model, description, price, quantity,rate)
        self.size = size
        self.tv_type = tv_type
    def __str__(self):
        if self.sale >0:
            return f"======================================\nName: {self.name}\nModel: {self.model}\ndisplay size: {self.size}-Inch\nDescription: {self.description}\nPrice:-{self.sale}% Off {self.price}₪ ILS\n{self.review()}"
        else:
            return f"======================================\nName: {self.name}\nModel: {self.model}\ndisplay size: {self.size}-Inch\nDescription: {self.description}\nPrice: {self.price}₪\n{self.review()}"