from Store.order import Order
from Store.product import Product
from Store.user import User
from Store.reporting import Reporting

class Store:  # מחלקה שמממשת את החנות עצמה

    def __init__(self):
        self.collection = {}  # קולקציית המוצרים שבחנות
        self.users = {1111:User(1111,"Admin",'1234'),}  # משתמשי החנות
        self.orders = {}  # הזמנות החנות
        self.order_number = 1  # מספר הזמנה
        self.reporting = Reporting()

    def add_product(self, product):
        if product.name not in self.collection:
            self.collection[product.name] = product
            self.reporting.sold_products[product.name] = 0
            return True  # במידה ונוסף למלאי ולא קיים כבר אחד
        return False

    def add_user(self, user:User):  # הוספת משתמש לחנות
        if user.user_id not in self.users:
            self.users[user.user_id] = user
            return True
        return False

    def remove (self,product):
         del self.collection[product.name]



    def add_item_order(self, product,how_many,order):
        if self.collection[product.name].available(how_many):
            new_order = order
            new_order.add_item_to_order(product,how_many)
            self.collection[product.name].buy_product(how_many)
            self.reporting.sold_products[product.name] += how_many
            self.reporting.revenue +=new_order.total_amount
            return True
        else:
            return False

    def place_order(self, order):
        self.orders[self.order_number] = order
        self.order_number += 1

    def list_products(self):
        if len(self.collection) > 0:
            return [(name, product.description, product.price, product.quantity) for name, product in
                    self.collection.items()]

    def list_orders(self):
        return [(order_number, order.customer_name, order.total_amount, order.status) for order_number, order in
                self.orders.items()]



