from Store.product import Product
class Tv (Product):
    def __init__(self, name=None, model=None, description=None, price=None, quantity=None, size=None, type =None):
        super().__init__(name, model, description, price,quantity)
        self.size = size
        self.type = type
    def __str__(self):
        return super().__str__() + f" Display size:{self.size}-Inch\n  {self.type}\n {self.price}₪"