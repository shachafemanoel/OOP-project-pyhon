from Store.products.product import Product


class Computer(Product):
    '''
        The Computer class represents a computer product in the store. It inherits from the Product class
        and includes additional attributes specific to computers, such as size, storage, and chip type.
    '''

    def __init__(self, name, model, description, price, quantity, size=None, storage=None,
                 chip=None, rate=None):
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
        chip: str, optional
        rate: float, optional
        '''
        super().__init__(name, model, description, price, quantity, rate)
        self.size = size
        self.storage = storage
        self.chip = chip

    def product_to_dict(self):
        '''
        Saving data to JSON as dictionary
        '''
        dict = {
            "size": self.size,
            "storage": self.storage,
            "chip": self.chip,
        }
        dict = {**super().product_to_dict(), **dict}
        dict["product_type"] = "Computer"
        return dict

    def product_type(self):
        '''
        Returns the type of product as a string.
        '''
        return "COMPUTER"

    def __str__(self):
        '''
        :return: A string representation of the computer's details.
        '''
        return f"======================================\n Name: {self.name}\n Model:{self.model}   |  Storge: {self.storage} \n Chip: {self.chip}\n display size: {self.size}-Inch \n Description: {self.description} \n {self.get_price_in_user_currency()}\n {self.rate}"
