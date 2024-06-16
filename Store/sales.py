from Store.product import Product
from Store.client import Client
class Sales:
    def __init__(self):
        pass

    def use_coupon(self):
        self.client.coupon = 0

    def update_coupon(self, amount):
        self.coupon = amount

    def update_price(self, discount):
            self.sale = discount
            self.price -= (self.product.original_price * float(discount / 100))

    def remove_discount(self):
        self.price = self.original_price
        self.sale = 0