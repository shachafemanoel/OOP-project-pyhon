from Store.client import Client
from Store.json import DataManager
from Store.order import Order
from Store.payment_calculator import CurrencyConverter
from Store.products.computer import Computer
from Store.products.phone import Phone
from Store.products.product import Product
from Store.products.product_factory import ProductFactory
from Store.products.tv import Tv
from Store.reporting import Reporting
from Store.sales import Sales
from Store.storeerror import StoreError
from Store.user import User


class Store:
    """
    A class to implement the store itself.

    Attributes
    ----------
    collection : dict
    users : dict
    orders : dict
    order_number : int
    reporting : Reporting
    sales : Sales
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the Store object.
        """
        self.collection = {}
        self.users = {}
        self.orders = {}
        self.order_number = 1
        self.reporting = Reporting()
        self.sales = Sales()
        self.currency = "₪ILS"
        self.factory = ProductFactory()

    def add_review(self, product, stars, review=None):
        """
        Adds a review for a product.

        Parameters
        ----------
        product : str
        stars : int
        review : str, optional

        Return True or False
        """
        if product in self.collection:
            self.collection[product].add_review(stars, review)
            return True
        return False

    def load_files(self):
        """
        Loads data from files into the store.
        """
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


    def save_files(self):
        """
        Saves data from the store to files.
        """
        DataManager.save_users(self.users)
        DataManager.save_orders(self.orders)
        DataManager.save_products(self.collection)
        DataManager.save_reporting(self.reporting, self.sales)

    def use_coupon(self, user):
        """
        Uses a coupon for a user.

        Parameters
        ----------
        user : User
        """
        self.users[user.user_id].use_coupon()

    def apply_discount_to_category(self, category, discount_percent):
        """
        Applies a discount to all products in a category.

        Parameters
        ----------
        category : str
        discount_percent : int or float
        """
        for product in self.collection.values():
            if product.product_type().casefold() == category.casefold():
                product.update_price(discount_percent)

    def remove_discount_to_category(self, category):
        """
        Removes a discount from all products in a category.

        Parameters
        ----------
        category : str
        """
        for product in self.collection.values():
            if product.product_type().casefold() == category.casefold():
                product.remove_discount()

    def remove_product_sale(self, choice):
        """
        Removes a sale from a product category.

        Parameters
        ----------
        choice : int
        """
        category = ProductFactory.get_product_type_by_choice(choice)
        if category is None:
            raise StoreError("Invalid Choice")
        try:
            self.sales.remove_category_discount(category)
            return category
        except StoreError:
            raise StoreError.InvalidInputError()

    def sale_prodduct_type(self, choice, discount):
        """
        Adds a sale to a product category.

        Parameters
        ----------
        choice : int
        discount : float
        """
        category = ProductFactory.get_product_type_by_choice(choice)
        if category is None:
            raise StoreError("Invalid Choice")
        try:
            self.sales.add_category_discount(category,discount)
            return category
        except ValueError as e:
            raise e

    def new_promotion(self, product, discount):
        """
        Adds a new discount to a product.

        Parameters
        ----------
        product : Product
        discount : float
        """
        try:
            self.sales.add_promotion(product.get_key_name(), discount)
            self.collection[product.get_key_name()].update_price(
                self.sales.get_product_discount(self.collection[product.get_key_name()]))
        except ValueError:
            raise ValueError

    def remove_promotion(self, item):
        """
        Removes a discount from a product.

        Parameters
        ----------
        item : Product
        """
        try:
            self.collection[item.get_key_name()].remove_discount()
            self.sales.remove_promotion(item.get_key_name())
        except ValueError:
            raise StoreError.InvalidInputError

    def change_currency(self, currency):
        """
        Changes for client the store's currency and updates product prices accordingly.

        Parameters
        ----------
        currency : str
        """
        if currency != self.currency:
            self.currency = currency
            for product in self.collection.values():
                if product.currency != self.currency:
                    product.currency = self.currency

    def lst_search(self, item_dict):
        """
        Searches for products in the store's collection and return a list of products.

        Parameters
        ----------
        item_dict : dict

        """
        temp = []
        for key in item_dict.keys():
            temp.append(self.collection[key])

        return temp

    def search(self, name=None, product_type=None, model=None):
        """
        Searches for products by name, type, or model.

        Parameters
        ----------
        name : str, optional
        product_type : str, optional
        model : str, optional

        Returns a list of found products.
        """
        if name is not None:
            cleaned_name = name.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if model is not None:
            cleaned_model = model.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        found = []
        for key, value in self.collection.items():
            if name is not None and value.get_key_name().casefold()[ 0:len(cleaned_name)] == cleaned_name.casefold():
                found.append(value)

            elif model is not None and cleaned_model.casefold() == value.get_model_name()[
                                                                   0:len(cleaned_model)].casefold():
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
        if found:
            return found
        else:
            raise StoreError.ProductNotFoundError

    def add_product(self, product_dict):
        """
        Adds a product to the store's collection.

        Parameters
        ----------
        product_dict : dict

        """
        if product_dict.get("name") is not None and product_dict.get("price") is not None and product_dict.get(
                "quantity") is not None:
            product_type = product_dict.pop("product_type", None)
            try:
                new_product = self.factory.create_product(product_type, **product_dict)
            except ValueError as e:
                raise ValueError(f"An error occurred while creating the product: {e}")

            discount = self.sales.get_product_discount(new_product)
            if discount > 0:
                new_product.update_price(discount)

            self.collection[new_product.get_key_name()] = new_product

    def client_list(self):
        """
        Returns a list of clients or str message.
        """
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

    def add_user(self, user: dict):
        """
        Adds a user to the store.

        Parameters
        ----------
        user : dict
        """
        if user.get("user_id") not in self.users:
            try:
                User.valid_user(user)
                user_type = user.pop("user_type", "Client").upper()
                if user_type == 'ADMIN':
                    new_user = User(**user)
                elif user_type == 'CLIENT':
                    new_user = Client(**user)
                self.sales.add_coupon(new_user.user_id, 5)
                new_user.user_id.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
                self.users[new_user.user_id] = new_user
                self.reporting.new_user(user_type, new_user.user_full_name)
                return new_user.login(new_user.password)
            except StoreError as e:
                raise e
        else:
            raise StoreError(" * user already exists * ")

    def remove_client(self, client_id):
        """
        Removes a client from the store.

        Parameters
        ----------
        client_id : str
        """
        if client_id in self.users:
            del self.users[client_id]
            return True
        else:
            return False

    def remove(self, product):
        """
        Removes a product from the store's collection.

        Parameters
        ----------
        product : Product (object)
        """
        if not isinstance(product, Product):
            raise StoreError.InvalidInputError("No product selected")
        if product.get_key_name() in self.collection:
            self.collection.pop(product.get_key_name())
            self.reporting.best_sell_product()
        else:
            raise StoreError.ProductNotFoundError(f"Product '{product.name}' not found in the collection.")

    def add_item_order(self, product, how_many):
        """
        Checks the availability of a product in the desired quantity.

        Parameters
        ----------
        product : Product
        how_many : int
        """
        return self.collection[product.get_key_name()].available(how_many)

    def place_order(self, order: dict):
        """
        Places a new order.

        Parameters
        ----------
        order : dict
        """
        if order.get("payment", None) is not None:
            order["order_number"] = self.order_number
            customer = order.get("customer", None)
            order.pop("count_item", None)
            order["total_amount"] = 0
            for name, quant in order["product_dict"].items():
                if self.collection[name].available(quant):
                    self.collection[name].buy_product(quant)
                    order["total_amount"] += self.collection[name].get_price(quant)
                    self.reporting.new_sold(name, quant)
                    if self.collection[name].get_quantity() < 4:
                        self.reporting.product_warning(self.collection[name].get_quantity(), self.collection[name].name)
            try:
                order = Order(**order)
                self.users[customer.user_id].new_order(order)
                self.orders[self.order_number] = order
                self.reporting.new_order(order)
                self.order_number += 1
            except ValueError as e:
                raise StoreError.InvalidInputError(f"Invalid order: {e}")

    def cancel_order(self, order_number):
        """
        Cancels an existing order.

        Parameters
        ----------
        order_number : int
        """
        for name, amount in self.orders[order_number].product_dict.items():
            if int(self.collection[name].quantity) >= 0:
                self.collection[name].add_quantity(int(amount))
            self.reporting.return_products(name, amount)
            price = self.collection[name].get_price(amount)
            self.reporting.order_canceled(str(order_number), price)
            self.reporting.best_sell_product()

    def list_products(self):
        """
        Returns string represent products collection
        """
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
        """
        Returns string represent all store's orders
        """
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
        """
        Logs a user into the store.

        Parameters
        ----------
        user_id : str
        password : str

        Returns User or Client logged in
        """
        login = user_id.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if login in self.users:
            try:
                self.users[login].login(password)
            except StoreError.AuthenticationError as e:
                raise e
            if type(self.users[login]) == User:
                return self.users[login]
            else:
                self.change_currency(self.users[login].currency)
                return self.users[login]
        else:
            raise StoreError.AuthenticationError("\n* User ID does not exist * ")

    def change_order(self, order_number, choice):
        """
        Changes the status of an order.

        Parameters
        ----------
        order_number : int
        choice : str
        """
        self.orders[order_number].change_status(choice)
        order = self.orders[order_number]
        user_id = order.customer.user_id
        self.users[user_id].new_status(order)

    def rate_search(self, low, high):
        """
        Searches for products within a given rating range.

        Parameters
        ----------
        low : float
        high : float

        Return: A list of products within the specified rating range.
        """
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

    def price_search(self, low, high, currency):
        """
        Searches for products within a given price range.

        Parameters
        ----------
        low : float
        high : float
        currency : str
        Return: A list of products within the specified price range.
        """
        products = []
        try:
            low, high = float(low), float(high)
            if currency != "₪ILS":
                low = CurrencyConverter.convert(low, currency, "₪ILS")
                high = CurrencyConverter.convert(high, currency, "₪ILS")
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
        """
        Sets the address for a user.

        Parameters
        ----------
        user_id : str
        address : str
        """
        if user_id in self.users:
            self.users[user_id].change_address(address)
            return True
        else:
            return False
