import json
import logging
from Store.order import Order
from Store.product import Product
from Store.user import User
from Store.client import Client
from Store.payment import Payment
from Store.reporting import Reporting
from Store.tv import Tv
from Store.phone import Phone
from Store.computer import Computer
from Store.rating import Rating

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - LEVEL - %(message)s')

class DataManager:
    @staticmethod
    def load_data(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                print(f"Loaded data from {filename}:")
                return data
        except FileNotFoundError:
            logging.warning(f"File {filename} not found.")
            return []
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from file {filename}: {e}")
            return []
        except Exception as e:
            logging.error(f"An error occurred while reading file {filename}: {e}")
            return []

    @staticmethod
    def save_data(data, filename):
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            logging.info(f"Data successfully saved to {filename}.")
        except IOError as e:
            logging.error(f"Error saving data to file {filename}: {e}")

    @staticmethod
    def load_orders(users):
        orders = {}
        orders_data = DataManager.load_data('Store/orders_logg.JSON')
        for order_data in orders_data:
            customer = users.get(order_data.pop('customer_id',None))
            if customer is not None:
                order = Order(**order_data)
                order.customer = customer
                order.currency = customer.currency
                order.payment = Payment(**order_data.get('payment')) if order_data.get('payment') else None
                orders[order.order_number] = order
                customer.order_history[order.order_number] = order
        return orders

    @staticmethod
    def save_orders(orders):
        orders_data = [
            order.order_to_dict()
            for order in orders.values()
        ]
        DataManager.save_data(orders_data, 'Store/orders_logg.JSON')

    @staticmethod
    def load_products():
        return  DataManager.load_data('Store/products_logg.JSON')




    @staticmethod
    def save_products(products):
        products_data = []
        for product in products.values():
            products_data.append(product.product_to_dict())
        DataManager.save_data(products_data, 'Store/products_logg.JSON')

    @staticmethod
    def load_users():
        users = {}
        users_data = DataManager.load_data('Store/users_logg.JSON')
        for user_data in users_data:
            user_type = user_data.pop('user_type')
            if user_type == 'Admin':
                user = User(**user_data)
            elif user_type == 'Client':
                user = Client(**user_data)
            else:
                logging.warning(f"Unknown user type: {user_type}")
                continue
            users[user.user_id] = user
        return users

    @staticmethod
    def save_users(users: dict):
        users_data = []
        for user in users.values():
            users_data.append(user.to_dict())
        DataManager.save_data(users_data, 'Store/users_logg.JSON')
    @staticmethod
    def load_reporting():
        reporting_data = DataManager.load_data('Store/reporting_logg.JSON')
        reporting = Reporting()
        if reporting_data:
            reporting.best_sell = reporting_data['best_sell']
            reporting.sold_products = reporting_data['sold_products']
            reporting.message = reporting_data['message']
            reporting.new_update = reporting_data['new_update']
            reporting.total_update = reporting_data['total_update']
        return reporting

    @staticmethod
    def save_reporting(reporting,sales):
        reporting_data =reporting.repoting_do_dict(sales)
        DataManager.save_data(reporting_data, 'Store/reporting_logg.JSON')

    @staticmethod
    def load_sales():
        sales_data = DataManager.load_data('Store/reporting_logg.JSON')
        sales = []
        if sales_data:
            sales = sales_data['sales']
        return sales
