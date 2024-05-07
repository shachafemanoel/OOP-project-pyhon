from Store.product import Product
class Computer(Product):
    def __init__(self, name =None,model=None,description=None, price=None, quantity=None,size=None,storge=None,chip=None):
        super().__init__(name,model,description,price,quantity)
        self.size = size
        self.storge = storge
        self.chip = chip

    def __str__(self):
        return super().__str__() +f" Screen Size: {self.size}\n Storage: {self.storge}\n Chip: {self.chip}\n quantity:{self.quantity}\n Price:{self.price}₪ֿ"