from Store.product import Product
class Computer(Product):
    def __init__(self, name =None, model=None, description=None, price=None, quantity=None, size=None, storage=None, chip=None,rate = None,sale=0):
        super().__init__(name, model, description, price, quantity,rate,sale)
        self.size = size
        self.storage = storage
        self.chip = chip

    def product_to_dict(self):
        dict = {
            "size": self.size,
            "storge": self.storage,
            "chip": self.chip,
        }

        dict={**super().product_to_dict(),**dict}

        dict["product_type"] = "Computer"
        return dict
    def __str__(self):
        if self.sale > 0:
            return f"======================================\n Name: {self.name}\n Model: {self.model} Storge: {self.storage} \n Chip: {self.chip}\n display size: {self.size}-Inch \n Description: {self.description} \n Price:-{self.sale}% Off {self.get_price(1)}₪ ILS\n{self.rate}"
        else:
            return f"======================================\n Name: {self.name}\n Model: {self.model} Storge: {self.storage} \n Chip: {self.chip}\n display size: {self.size}-Inch \n Description: {self.description} \n Price: {self.price}₪\n{self.rate}"