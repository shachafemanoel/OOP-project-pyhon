from Store.product import Product
class Phone (Product):
    def __init__(self, name =None, model=None, description=None, price=None, quantity=None, size=None, storage=None,rate =None):
        super().__init__(name, model, description, price,quantity,rate)
        self.size = size
        self.storage = storage

    def __str__(self):
        if self.sale > 0:
            return f"======================================\nName: {self.name}\nModel: {self.model} Storge: {self.storage}\ndisplay size: {self.size}-Inch\nDescription: {self.description}\nPrice:-{self.sale}% Off {self.price}₪ ILS\n{self.review()}"
        else:

            return f"======================================\nName: {self.name}\n Model: {self.model} Storge: {self.storage} \ndisplay size: {self.size}-Inch  \nDescription: {self.description} \n Price: {self.price}₪\n{self.review()}"