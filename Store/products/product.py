from abc import ABC

from Store.payment_calculator import CurrencyConverter
from Store.rating import Rating


def discount_decorator(discount):
    """
    Decorator to apply a discount to the price of a product.

    Args:
        discount (float): The discount percentage to be applied.

    Returns:
        function: The decorated function with the discount applied.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            original_price = func(*args, **kwargs)
            discounted_price = original_price - (original_price * (discount / 100))
            return discounted_price

        return wrapper

    return decorator


class Product(ABC):
    '''
        The Product class represents a general product in the store.
        Additionally, it provides methods to manage product details, pricing, and inventory.
    '''

    def __init__(self, name, model, description, price, quantity, rate=None):
        '''
        Attributes:
        -----------
        name : str
        model : str
        description : str
        original_price : float
        price : float
        sale : float
        quantity : int
        rate : Rating
        currency : str
        '''
        self.name = name
        self.model = model
        self.description = description
        self.original_price = price
        self.price = price
        self.sale = 0
        self.quantity = quantity
        self.rate = Rating(rate) if rate is not None else Rating()
        self.currency = "₪ILS"

    def get_key_name(self):
        '''
        :return: name without spaces or special characters
        '''
        return self.name.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def get_model_name(self):
        '''
        :return: model name without spaces or special characters
        '''
        return self.model.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def buy_product(self, many):
        '''
        :param many:int
        update quantity manually
        '''
        self.quantity -= many

    def update_price(self, discount):
        '''
        :param discount: float or int
        :return: updated price relating to coupon or discount
        '''
        self.sale = discount
        self.price = self.original_price
        self.price -= (self.original_price * float(discount / 100))

    def remove_discount(self):
        '''
        :return: removing discount and update price to the original price
        '''
        self.price = self.original_price
        self.sale = 0

    def change_quantity(self, new_quantity):
        '''
        :param new_quantity: int
        change the quantity of the product
        '''
        self.quantity = new_quantity

    @discount_decorator(20)
    def get_price(self, much):
        '''
        :param much: int
        :return: price of amount of products
        '''
        return self.price * much

    def get_quantity(self):
        '''
        :return quantity of product
        '''
        return self.quantity

    def add_quantity(self, quantity):
        '''
        :param quantity: int
        :return: added quantity to inventory
        '''
        self.quantity += quantity

    def available(self, how_many):
        '''
        :param how_many:int
        check if product is available
        '''
        if how_many > self.quantity:
            return False
        else:
            return True

    def add_review(self, stars, review):
        '''
        Adding review to product
        '''
        self.rate.add_review(stars, review)

    def product_to_dict(self):
        '''
        Saving data to JSON files
        '''
        dict = {}
        dict['product_type'] = "Product"
        dict['name'] = self.name
        dict["model"] = self.model
        dict['description'] = self.description
        dict['price'] = self.original_price
        dict['quantity'] = self.quantity
        dict['rate'] = self.rate.ratings
        return dict

    def get_price_in_user_currency(self, quantity=1):
        '''
        :param quantity: int
        :return the price of the product in the user's preferred currency.
        '''
        price = ""
        if self.sale > 0:
            price += f" Original price:{CurrencyConverter.convert(self.original_price, "₪ILS", self.currency) * quantity} {self.currency} \n-{self.sale}% Off "
        price += f"Price: {CurrencyConverter.convert(self.price, "₪ILS", self.currency) * quantity} {self.currency}"
        return price

    def product_type(self):
        '''
        :return: A string representation of product type
        '''
        return "PRODUCT"

    def __str__(self):
        '''
        :return: string representation of product
        '''
        return f"======================================\n Name: {self.name}\n Model: {self.model}\n Description: {self.description}\n\n {self.get_price_in_user_currency()}\n {self.rate}"
