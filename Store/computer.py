from Store.product import Product
class Computer(Product):
    def __init__(self, name =None,model=None,description=None, price=None, quantity=None,size=None,storge=None,chip=None):
        super().__init__(name,model,description,price,quantity)
        self.size = size
        self.storge = storge
        self.chip = chip

    def __str__(self):
        return f"======================================\nName: {self.name}\n Model: {self.model} Storge: {self.storge} \n Chip: {self.chip}\n display size: {self.size}-Inch \n Description: {self.description} \n Price: {self.price}₪\n{self.review()}"