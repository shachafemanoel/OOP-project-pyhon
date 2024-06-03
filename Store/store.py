from Store.order import Order
from Store.product import Product
from Store.user import User
from Store.reporting import Reporting
from Store.client import Client
from Store.tv import Tv
from Store.phone import Phone
from Store.computer import Computer
from Store.rating import Rating
from Store.json import DataManager
from Store.rating import Rating

class Store:  # מחלקה שמממשת את החנות עצמה

    def __init__(self):

        self.collection = {}
        self.users = {}  # משתמשי החנות
        self.orders = {}  # הזמנות החנות
        self.order_number = 1  # מספר הזמנה
        self.reporting = Reporting()
        self.sales = []


    def add_review(self,product, stars, review=None):
        self.collection[product].add_review(stars,review)


    def load_files(self):
        self.users = DataManager.load_users()
        self.collection = DataManager.load_products()
        self.orders = DataManager.load_orders(self.users)
        self.reporting = DataManager.load_reporting()
        self.sales = DataManager.load_sales()
        self.order_number = len(self.orders) +1
        for order in self.orders.values():
            self.reporting.revenue+=order.total_amount

    def user_order_history(self, user):
        user_orders_dict = {}
        for order in self.orders.values():
            if order.customer == user:
                user_orders_dict[order.order_number] = order
        return user_orders_dict

    def save_files(self):
        DataManager.save_users(self.users)
        DataManager.save_orders(self.orders)
        DataManager.save_products(self.collection)
        DataManager.save_reporting(self.reporting,self.sales)


    def use_coupon(self,user):
        self.users[user.user_id].use_coupon()

    def sale_prodduct_type(self, product_type, discount):
        if product_type == "1":
               self.sales.append(f" * -{discount}% discount on all TVs * ")
        elif product_type == "2":
            self.sales.append(f" * -{discount}% discount on all Computers * ")
        elif product_type == "3":
            self.sales.append(f" * -{discount}% discount on all Phones * ")
        elif product_type == "4":
            self.sales.append(f" * -{discount}% discount on all Accessories * ")

    def new_discount(self, lst, discount):
        if 0 < discount < 100:
            if isinstance(lst, list):   # הנחה על מחלקה שלמה
                for product in self.collection.values():
                    if product in lst:
                        product.update_price(discount)

            if isinstance(lst, Product) or isinstance(lst, Tv) or isinstance(lst, Computer) or isinstance(lst, Phone) :#הנחה על מוצר ספציפי
                    product = lst
                    product.update_price(discount)
                    self.collection[product.get_key_name()] = product

    def remove_discount(self, item=None):
        if item:
            self.sales = []
            for product in self.collection.values():
               if isinstance(product, Product):
                    product.remove_discount()

        elif isinstance(item, Product):
            item.remove_discount()

        else:
            print("Invalid item.")


    def lst_search(self,order):
        temp = []
        for key in order.product_dict.keys():
           temp.append(self.collection[key])

        return temp
    def search(self, name=None, product_type=None, model=None):
        if name is not None:
            cleaned_name = name.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if model is not None:
            cleaned_model = model.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        found = []
        for key, value in self.collection.items():
            if name is not None:     # חיפוש לפי שם
                if value.get_key_name().casefold()[0:len(cleaned_name)] == cleaned_name.casefold():
                    if model is not None and cleaned_model.casefold() == value.get_model_name()[0:len(cleaned_model)].casefold():# חיפוש לפי שם ומודל
                        found.append(value)
                    else:
                        found.append(value)

            if product_type is not None and name is None:
                if product_type == "1":
                    if isinstance(value, Tv):
                        found.append(value)
                elif product_type == "2":
                    if isinstance(value, Computer):
                        found.append(value)
                elif product_type == "3":
                    if isinstance(value, Phone):
                        found.append(value)
                elif product_type == "4":
                    if type(value) != Tv and type(value) != Phone and type(value) != Computer:
                        found.append(value)

        return found


    def add_product(self, product):
        self.collection[product.get_key_name()] = product
        return "Product added successfully."



    def add_user(self, user:User):  # הוספת משתמש לחנות
        if user.user_id not in self.users:
            self.users[user.user_id.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))] = user
            self.reporting.message.append(f" \n * A new customer has joined your store * \n customer name: {user.user_full_name}  ")
            self.reporting.new_update += 1
            return True
        return False

    def remove(self, product):
        if product in self.collection.values():
           self.collection.pop(product.get_key_name())
           self.reporting.remove(product.get_key_name())
           return True
        else:
            return False

    def add_item_order(self, product, how_many):
        if self.collection[product.get_key_name()].available(how_many):
            return True
        else:
            return False

    def place_order(self, order):
        if order.payment is not None:
            order.order_number = self.order_number
            self.orders[self.order_number] = order
            for name, quant in order.product_dict.items():
               if self.collection[name].available(quant):
                    self.collection[name].buy_product(quant)
                    self.reporting.new_sold(name,quant)
                    if self.collection[name].get_quantity() <4:
                        self.reporting.message.append(f"\n * Warning:Less than {self.collection[name].get_quantity()} left in stock {self.collection[name].name} *\n")
            self.reporting.new_order(order)
            self.order_number += 1


    def list_products(self):
        if len(self.collection) > 0:
            return [(product.name, product.model, f"Price: {product.price} ₪ ", f"Available: {product.quantity}") for name, product in
                    self.collection.items()]
        else:
            return " No products in inventory yet!"

    def list_orders(self):
        return [[order_number, order.customer.user_full_name, order.total_amount, order.status] for order_number, order in
                self.orders.items()]

    def log(self, user_id, password):
        login = user_id.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if login in self.users and self.users[login].login(password):
            if type(self.users[login]) == User:
                return self.users[login]
            else:
                history = self.user_order_history(self.users[login])
                self.users[login].order_history = history
                return self.users[login]
        else:
            return None

    def change_order(self, order_number, choice):
        self.orders[order_number].change_status(choice)
        order = self.orders[order_number]
        user_id = order.customer.user_id
        self.users[user_id].new_status(order)







