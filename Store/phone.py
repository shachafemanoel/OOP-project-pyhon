from Store.product import Product
class Phone (Product):
    def __init__(self, name =None,model=None,description=None, price=None, quantity=None,size=None,storge=None):
        super().__init__(name, model, description, price,quantity)
        self.size = size
        self.storge = storge

    def __str__(self):
        return super().__str__() + f"Display size:{self.size}-Inch\n Phone  Storge is {self.storge} GB\nPrice:{self.price}₪"