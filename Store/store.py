from Store.order import Order
from Store.product import Product
from Store.user import User
from Store.reporting import Reporting
from Store.client import Client

class Store:  # מחלקה שמממשת את החנות עצמה

    def __init__(self):
        macbook_air_13 = Product('MacBook Air 13”', "256 gb,M2 chip Liquid Retina display  ", "13",6000, 10)
        iphone_15_promax = Product('Iphone 15 pro max', "256 GB ", "4000",5000, 10)

        self.collection = {'MacBook Air 13”':macbook_air_13,'Iphone 15 pro max':iphone_15_promax,}  # קולקציית המוצרים שבחנות
        self.users = {1111:User(1111,"Admin",'1234'),2020:Client(2020,"Client Check",'1234','Address'),}  # משתמשי החנות
        self.orders = {}  # הזמנות החנות
        self.order_number = 1  # מספר הזמנה
        self.reporting = Reporting()

    def add_product(self, product):

        if product.name  in self.collection:
            if product.model == self.collection[product.name]:
                self.collection[product.name] += product.quantity
                return "Product quantity updated successfully."
            else:
                self.collection[product.name] = product
                self.reporting.sold_products[product.name] = 0
                return "Product added successfully."

    def add_user(self, user:User):  # הוספת משתמש לחנות
        if user.user_id not in self.users:
            user = Client(user.user_id, user.user_full_name, user.password)
            self.users[user.user_id] = user
            return True
        return False

    def remove(self, product_name):
        if product_name in self.collection:
            del self.collection[product_name]
            return True
        else:
            return False

    def add_item_order(self, product, how_many, order):
        if self.collection[product.name].available(how_many):
            new_order = order
            new_order.add_item_to_order(product, how_many)
            self.collection[product.name].buy_product(how_many)
            self.reporting.sold_products[product.name] += how_many
            self.reporting.revenue += new_order.total_amount
            return True
        else:
            return False

    def place_order(self, order):
        self.orders[self.order_number] = order
        self.order_number += 1

    def list_products(self):
        if len(self.collection) > 0:
            return [(name, product.description, f"Price: {product.price} ₪ ", f"Available: {product.quantity}") for name, product in
                    self.collection.items()]

    def list_orders(self):
        return [(order_number, order.customer_name, order.total_amount, order.status) for order_number, order in
                self.orders.items()]




