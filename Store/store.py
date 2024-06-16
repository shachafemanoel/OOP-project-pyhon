from Store.client import Client
from Store.json import DataManager
from Store.order import Order
from Store.products.computer import Computer
from Store.products.phone import Phone
from Store.products.product import Product
from Store.products.tv import Tv
from Store.reporting import Reporting
from Store.storeerror import StoreError
from Store.user import User
from Store.sales import Sales

class Store:  # מחלקה שמממשת את החנות עצמה

    def __init__(self):

        self.collection = {}
        self.users = {}  # משתמשי החנות
        self.orders = {}  # הזמנות החנות
        self.order_number = 1  # מספר הזמנה
        self.reporting = Reporting()
        self.sales = Sales()
        self.currency = "₪ILS"
    def add_review(self,product, stars, review=None):
        if product in self.collection:
            self.collection[product].add_review(stars,review)
            return True
        return False

    def load_files(self):
        self.users = DataManager.load_users()
        collection = DataManager.load_products()
        self.sales = DataManager.load_sales()
        for product in collection:
            self.add_product(product)
        self.orders = DataManager.load_orders(self.users)
        self.reporting = DataManager.load_reporting()

        self.order_number = len(self.orders) + 1
        for order in self.orders.values():
            if order.status != "Canceled":
                self.reporting.revenue += order.total_amount

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



    def remove_product_sale(self,choice):
        category = ""
        if choice == "1":
            category = "Tv"
        elif choice == "2":
            category = "Computer"
        elif choice == "3":
            category = "Phone"
        elif choice == "4":
            category = "Product"
        try:
            self.sales.remove_category_discount(category.upper())
        except ValueError:
            raise StoreError.InvalidInputError

    def sale_prodduct_type(self, choice, discount):
        category = ""
        if choice == "1":
            category = "Tv"
        elif choice == "2":
            category = "Computer"
        elif choice == "3":
            category = "Phone"
        elif choice == "4":
            category = "Product"
        try:
            self.sales.add_category_discount(category.upper(), discount)
        except ValueError:
            raise StoreError.InvalidInputError

    def new_promotion(self, product,discount):
        try:
            self.collection[product.get_key_name()].update_price(discount)
            self.sales.add_promotion(product.get_key_name(),discount)
        except ValueError :
            raise ValueError
    def remove_promotion(self,item):
        try:
            self.collection[item.get_key_name()].remove_discount()
            self.sales.remove_promotion(item.get_key_name())
        except ValueError:
            raise StoreError.InvalidInputError
    def change_currency(self,currency):
        if currency != self.currency:
            self.currency = currency
            for product in self.collection.values():
                if product.currency != self.currency:
                    product.currency = self.currency


    def lst_search(self,item_dict):
        temp = []
        for key in item_dict.keys():
           temp.append(self.collection[key])

        return temp
    def search(self, name=None, product_type=None, model=None):
        if name is not None:
            cleaned_name = name.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if model is not None:
            cleaned_model = model.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        found = []
        for key, value in self.collection.items():
            if name is not None and value.get_key_name().casefold()[0:len(cleaned_name)] == cleaned_name.casefold():     # חיפוש לפי שם
                    found.append(value)

            elif model is not None and cleaned_model.casefold() == value.get_model_name()[0:len(cleaned_model)].casefold():# חיפוש לפי שם ומודל
                    found.append(value)


            elif product_type is not None and name is None:
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


    def add_product(self, product_dict):
        if product_dict.get("name",None) is not None and product_dict.get("price",None) is not None and product_dict.get("quantity",None) is not None:
            product_type = product_dict.pop("product_type",None)
            if product_type == "Tv":
                new_product = Tv(**product_dict)
            elif product_type == "Computer":
                new_product = Computer(**product_dict)
            elif product_type == "Phone":
                new_product = Phone(**product_dict)
            else:
                new_product = Product(**product_dict)
            discount = self.sales.get_product_discount(new_product)
            if discount > 0:
                new_product.update_price(discount)
            self.collection[new_product.get_key_name()] = new_product


    def client_list(self):
        if len(self.users) > 0:
            table = "\n            Users    \n"
            table += "-----------------------------------------\n"
            for user_id, details in self.users.items():
                if isinstance(details, Client):
                    table += f"ID:{user_id:<12} | Full name:{details.user_full_name} \n Orders Quantity: {len(details.order_history)}\n"
                    table += "-----------------------------------------\n"
            return table
        else:
            return "\n* No clients yet *"


    def add_user(self, user:dict):  # הוספת משתמש לחנות
        if user.get("user_id") not in self.users:
            user_type = user.pop("user_type","Client").upper()
            if user_type == 'ADMIN':
                new_user = User(**user)
            elif user_type == 'CLIENT':
                new_user = Client(**user)
                self.sales.add_coupon(new_user.user_id,5)
            new_user.user_id.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
            self.users[new_user.user_id] = new_user
            self.reporting.new_user(user_type,new_user.user_full_name)
            return True
        return False

    def remove_client(self, client_id):
        if client_id in self.users:
            del self.users[client_id]
            return True
        else:
            return False

    def remove(self,product):
        if not isinstance(product, Product):
            raise StoreError.InvalidInputError("No product selected")
        if product.get_key_name() in self.collection:
            self.collection.pop(product.get_key_name())
            self.reporting.best_sell_product()
        else:
            raise StoreError.ProductNotFoundError(f"Product '{product.name}' not found in the collection.")

    def add_item_order(self, product, how_many):
        return self.collection[product.get_key_name()].available(how_many)


    def place_order(self, order:dict):
        if order.get("payment", None) is not None:
            order["order_number"] = self.order_number
            customer = order.get("customer",None)
            order.pop("count_item", None)
            order["total_amount"] = 0
            for name, quant in order["product_dict"].items():
               if self.collection[name].available(quant):
                    self.collection[name].buy_product(quant)
                    order["total_amount"] += self.collection[name].get_price(quant)
                    self.reporting.new_sold(name, quant)
                    if self.collection[name].get_quantity() < 4:
                        self.reporting.product_warning(self.collection[name].get_quantity(),self.collection[name].name)
            order = Order(**order)
            self.reporting.new_order(order)
            self.users[customer.user_id].new_order(order)
            self.orders[self.order_number] = order
            self.order_number += 1

    def cancel_order(self, order_number):
        for name, amount in self.orders[order_number].product_dict.items():
            if int(self.collection[name].quantity) >= 0:
                self.collection[name].add_quantity(int(amount))
            self.reporting.return_products(name, amount)
            price = self.collection[name].get_price(amount)
            self.reporting.order_canceled(order_number, price)
            self.reporting.best_sell_product()


    def list_products(self):
        if self.collection:
            table = "\n            Inventory    \n"
            table += "-----------------------------------------\n"
            for key, value in self.collection.items():
                table += f"Name:{key:<12}  \nPrice:{value.price} ILS           | Quantity: {value.quantity}\n"
                table += "-----------------------------------------\n"
        else:
            table = "\n * There are no products *\n"
        return table

    def list_orders(self):
        if self.orders:
            table = "\n            Orders History    \n"
            table += "-----------------------------------------\n"
            for key, value in self.orders.items():
                table += f"Order number:{key:<12}  \n{value.converter():<18} | Status: {value.status}\n"
                table += "-----------------------------------------\n"
        else:
            table = "\n * There are no orders *\n"
        return table

    def log(self, user_id, password):
        login = user_id.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if login in self.users and self.users[login].login(password):
            if type(self.users[login]) == User:
                return self.users[login]
            else:
                self.change_currency(self.users[login].currency)
                return self.users[login]
        else:
            return None

    def change_order(self, order_number, choice):
        self.orders[order_number].change_status(choice)
        order = self.orders[order_number]
        user_id = order.customer.user_id
        self.users[user_id].new_status(order)

    def rate_search(self, low, high):
        products = []
        try:
            low, high = float(low), float(high)
            if high < low:
                raise StoreError.InvalidInputError("High rating must be higher than low rating.")
            if not (0 <= low <= 5 and 0 <= high <= 5):
                raise StoreError.InvalidInputError("Ratings must be between 0 and 5.")
            for name, product in self.collection.items():
                if low <= product.rate.weighted_average_rating() <= high:
                    products.append(product)
            if not products:
                raise StoreError.ProductNotFoundError("No products found in this rating range.")
            return products
        except ValueError:
            raise StoreError.InvalidInputError("\nLow rating and high rating must be numbers.")

    def price_search(self, low, high):
        products = []
        try:
            low, high = float(low), float(high)
            if high < low:
                raise StoreError.InvalidInputError("\nHigh price must be higher than low price.")
            if not (0 <= low and 0 <= high):
                raise StoreError.InvalidInputError("\nprices must be higher than 0.")
            for name, product in self.collection.items():
                if low <= product.price <= high:
                    products.append(product)
            if not products:
                raise StoreError.ProductNotFoundError("\nNo products found in this price range.")
            return products
        except ValueError:
            raise StoreError.InvalidInputError("\nInvalid credentials. low price and high price must be digit.")

    def set_address(self, user_id, address):
        if user_id in self.users:
            self.users[user_id].change_address(address)
            return True
        else:
            return False



