from Store.product import Product
class Computer(Product):
    def __init__(self, name =None, model=None, description=None, price=None, quantity=None, size=None, storage=None, chip=None,rate = None):
        super().__init__(name, model, description, price, quantity,rate)
        self.size = size
        self.storage = storage
        self.chip = chip

    def __str__(self):
        if self.sale > 0:
            return f"======================================\n Name: {self.name}\n Model: {self.model} Storge: {self.storage} \n Chip: {self.chip}\n display size: {self.size}-Inch \n Description: {self.description} \n Price:-{self.sale}% Off {self.price}₪ ILS\n{self.review()}"
        else:
            return f"======================================\n Name: {self.name}\n Model: {self.model} Storge: {self.storage} \n Chip: {self.chip}\n display size: {self.size}-Inch \n Description: {self.description} \n Price: {self.price}₪\n{self.review()}"