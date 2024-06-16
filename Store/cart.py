from Store.products.product import Product
from Store.products.computer import Computer
from Store.products.tv import Tv
from Store.products.phone import Phone
from Store.store import StoreError



class Cart:
    def __init__(self):
        """
        Initialize the Cart class with an empty product dictionary and total amount.
        """
        self.product_dict = {}
        self.total_amount = 0
        self.count_item = 0

    def add_item(self, product: Product, quantity: int):
        """
        Add an item to the cart.

        Parameters:
        product (Product): The product to add.
        quantity (int): The quantity to add.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        if product.get_key_name() in self.product_dict:
            self.product_dict[product.get_key_name()] += quantity
        else:
            self.product_dict[product.get_key_name()] = quantity
        if product.available(self.product_dict[product.get_key_name()]):
            self.total_amount += product.get_price(quantity)
            self.count_item += quantity
        else:
            raise StoreError.NotInStockError("Item not available.")

    def remove_item(self, product: Product, quantity: int):
        """
        Remove an item from the cart.

        Parameters:
        product (Product): The product to remove.
        quantity (int): The quantity to remove.
        """
        if product.get_key_name() not in self.product_dict:
            raise ValueError("Product not in cart.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        if self.product_dict[product.get_key_name()] < quantity:
            raise ValueError("Not enough quantity in cart to remove.")

        self.product_dict[product.get_key_name()] -= quantity
        self.total_amount -= product.get_price(quantity)
        self.count_item -= quantity

        if self.product_dict[product.get_key_name()] == 0:
            del self.product_dict[product.get_key_name()]



    def clear_cart(self):
        """
        Clear the cart.
        """
        self.product_dict.clear()
        self.total_amount = 0
        self.count_item = 0





    def get_product_by_key(self, key):
        """
        Retrieve a product by its key name.

        Parameters:
        key (str): The key name of the product.

        Returns:
        Product: The product associated with the key name.
        """
        for product in self.product_dict:  # Assuming self.products is a list of all available products
            if product.get_key_name() == key:
                return product
        raise ValueError("Product not found.")

    def get_cart_dict(self):
        """
        Get a dict of the cart.

        Returns:
        dict: A dictionary containing the cart summary.
        """
        return {
            "total_amount": self.total_amount,
            "product_dict": self.product_dict
        }
    def use_coupon(self,coupon):
        self.total_amount *= (1 - (coupon / 100))
    def update_item_quantity(self, product: Product, quantity: int):
        """
        Update the quantity of a specific item in the cart.

        Parameters:
        product (Product): The product to update.
        quantity (int): The new quantity.
        """
        current_quantity = self.product_dict.get(product.get_key_name(), 0)
        if quantity > current_quantity:
            self.add_item(product, quantity - current_quantity)
        elif quantity < current_quantity:
            self.remove_item(product, current_quantity - quantity)
    def __str__(self):
        """
        String representation of the cart.
        """

        return (
            f"Cart Summary\n"
            f"================\n"
            f"{self.product_dict}\n"
            f"================\n"
            f"Total amount: {self.total_amount}\n")