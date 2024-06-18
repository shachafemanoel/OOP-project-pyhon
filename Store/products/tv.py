from Store.products.product import Product


class Tv(Product):
    '''
    The Tv class represents a Tv product in the store. It inherits from the Product class
    and includes additional attributes specific to Tvs, such as size, Tv type.
    '''

    def __init__(self, name, model, description, price, quantity, size=None, tv_type=None,
                 rate=None):
        '''
        Attributes:
        -----------
        name: str
        model: str
        description: str
        price: float
        quantity: int
        size: str, optional
        tv_type: str, optional
        rate: float, optional
        '''
        super().__init__(name, model, description, price, quantity, rate)
        self.size = size
        self.tv_type = tv_type

    def product_to_dict(self):
        '''
        Saving data to JSON as dictionary
        '''
        dict = {
            "size": self.size,
            "tv_type": self.tv_type,
        }
        dict = {**super().product_to_dict(), **dict}

        dict["product_type"] = "Tv"
        return dict

    def product_type(self):
        '''
        Returns the type of product as a string.
        '''
        return "TV"

    def __str__(self):
        '''
        :return: A string representation of the object.
        '''
        return f"======================================\nName: {self.name}\nModel: {self.model}\ndisplay size: {self.size}-Inch\nDescription: {self.description}\n {self.get_price_in_user_currency()}\n{self.rate.preview_rating()}"
