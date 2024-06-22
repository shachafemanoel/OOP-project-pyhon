import json
import logging

from Store.client import Client
from Store.order import Order
from Store.payment import Payment
from Store.reporting import Reporting
from Store.sales import Sales
from Store.user import User

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - LEVEL - %(message)s')


class DataManager:
    '''
    An object that manage all the data of the project
    '''
    @staticmethod
    def load_data(filename):
        '''
        General function that reading all the data of files
        :param filename:
        '''
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
        '''
        General function that saves all data to the files
        :param data:
        :param filename:
        '''
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            logging.info(f"Data successfully saved to {filename}.")
        except IOError as e:
            logging.error(f"Error saving data to file {filename}: {e}")

    @staticmethod
    def load_orders(users):
        '''
        Function for loading orders data
        :param users:
        :return:
        '''
        orders = {}
        orders_data = DataManager.load_data('Store/orders_logg.JSON')
        for order_data in orders_data:
            customer = users.get(order_data.pop('customer_id', None))
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
        '''
        Fucntion for saving orders data
        :param orders:
        '''
        orders_data = [
            order.order_to_dict()
            for order in orders.values()
        ]
        DataManager.save_data(orders_data, 'Store/orders_logg.JSON')

    @staticmethod
    def load_products():
        '''
        Function for loading products data
        '''
        return DataManager.load_data('Store/products_logg.JSON')

    @staticmethod
    def save_products(products):
        '''
        Function for saving products data
        :param products:
        '''
        products_data = []
        for product in products.values():
            products_data.append(product.product_to_dict())
        DataManager.save_data(products_data, 'Store/products_logg.JSON')

    @staticmethod
    def load_users():
        '''
        Function for loading users data
        '''
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
        '''
        Function for saving users data
        :param users:
        '''
        users_data = []
        for user in users.values():
            users_data.append(user.to_dict())
        DataManager.save_data(users_data, 'Store/users_logg.JSON')

    @staticmethod
    def load_reporting():
        """
        Load reporting data from a JSON file and create a Reporting object.
        """
        reporting_data = DataManager.load_data('Store/reporting_logg.JSON')
        reporting = Reporting()
        if reporting_data:
            reporting.best_sell = reporting_data['best_sell']
            reporting.sold_products = reporting_data['sold_products']
            reporting.message["orders"] = reporting_data['message']["orders"]
            reporting.message["users"] = reporting_data['message']["users"]
            reporting.message["products"] = reporting_data['message']["products"]
            reporting.new_update["orders"] = reporting_data['new_update']["orders"]
            reporting.new_update["products"] = reporting_data['new_update']["products"]
            reporting.new_update["users"] = reporting_data['new_update']["users"]
            reporting.total_update = reporting_data['total_update']
        return reporting

    @staticmethod
    def save_reporting(reporting, sales):
        '''
        Function for saving reporting data
        :param reporting:
        :param sales:
        '''
        reporting_data = reporting.repoting_do_dict(sales)
        DataManager.save_data(reporting_data, 'Store/reporting_logg.JSON')

    @staticmethod
    def load_sales():
        '''
        Function that loading the sales data
        The data of sales are in reporting
        :return:
        '''
        sales_data = DataManager.load_data('Store/reporting_logg.JSON')
        sales = Sales()
        if sales_data.get("sales"):
            sales.coupons = sales_data["sales"]["coupons"]
            sales.promotions = sales_data["sales"]["promotions"]
            sales.category_discounts = sales_data["sales"]["category_discounts"]
        return sales
