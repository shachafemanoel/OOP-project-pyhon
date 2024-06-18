from Store.products.product import Product


class Phone(Product):
    '''
        The Phone class represents a Phone product in the store. It inherits from the Product class
        and includes additional attributes specific to Phones, such as size, storage.
    '''

    def __init__(self, name, model, description, price, quantity, size=None, storage=None,
                 rate=None, ):
        '''
        Attributes:
        -----------
        name: str
        model: str
        description: str
        price: float
        quantity: int
        size: str, optional
        storage: str, optional
        rate: float, optional
        '''
        super().__init__(name, model, description, price, quantity, rate)
        self.size = size
        self.storage = storage

    def product_to_dict(self):
        '''
        Saving data to JSON as dictionary
        '''
        dict = {
            "size": self.size,
            "storage": self.storage,
        }

        dict = {**super().product_to_dict(), **dict}

        dict["product_type"] = "Phone"
        return dict

    def product_type(self):
        '''
        Returns the type of product as a string.
        '''
        return "PHONE"

    def __str__(self):
        '''
        :return: A string representation of the object.
        '''
        return f"======================================\nName: {self.name}\nModel: {self.model} Storge: {self.storage}\ndisplay size: {self.size}-Inch\nDescription: {self.description}\n{self.get_price_in_user_currency()}\n{self.rate.preview_rating()}"
