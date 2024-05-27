import unittest
from Store.order import Order
from Store.product import Product
from Store.user import User
from Store.client import Client
from Store.tv import Tv
from Store.phone import Phone
from Store.computer import Computer
from Store.reporting import Reporting
from Store.store import Store


class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = Store()
        self.client = Client("2020", "Client Check", '1234', 'Address')
        self.macbook_air_13 = Computer('MacBook air 13', 'Air', "Liquid Retina display", 6000, 10, "13", "256", "M2")
        self.iphone_15_promax = Phone('Iphone 15', 'Pro max', 'The new Iphone 15 pro max', 5000, 10)
        self.store.collection = {self.macbook_air_13.get_key_name(): self.macbook_air_13, self.iphone_15_promax.get_key_name(): self.iphone_15_promax}
        self.store.users = {self.client.user_full_name: self.client}
        self.store.orders = {}
        self.store.order_number = 0
        self.store.sales = []
    def test_initialization(self):
        self.assertEqual(len(self.store.collection), 2)
        self.assertEqual(len(self.store.users), 1)
        self.assertEqual(len(self.store.orders), 0)
        self.assertEqual(self.store.order_number, 0)
        self.assertIsInstance(self.store.reporting, Reporting)

    def test_add_product(self):
        airpods_pro = Product('AirPods Pro', 'Pro', 'wireless charging - MagSafe', 1000, 10)
        response = self.store.add_product(airpods_pro)
        product_key = airpods_pro.get_key_name()
        self.assertIn(product_key, self.store.collection)
        self.assertEqual(response, "Product added successfully.")
        self.assertEqual(self.store.reporting.sold_products[airpods_pro.name], 0)

    def test_add_user(self):
        new_user = User("2021", "New User", 'password')
        self.assertTrue(self.store.add_user(new_user))
        self.assertIn("2021", self.store.users)
        self.assertIn(f" \n * A new customer has joined your store * \n customer name: {new_user.user_full_name}  ", self.store.reporting.message)
        self.assertFalse(self.store.add_user(new_user))

    def test_remove_product(self):
        product_name = self.macbook_air_13.get_key_name()
        product = self.store.collection[product_name]
        self.assertTrue(self.store.remove(product))
        self.assertNotIn(product_name, self.store.collection)

    def test_add_item_order(self):
        self.assertTrue(self.store.add_item_order(self.macbook_air_13, 3))
        self.assertFalse(self.store.add_item_order(self.macbook_air_13, 20))

    def test_place_order(self):
        order = Order(self.client, 0, {self.macbook_air_13.get_key_name(): 2}, "Credit Card")
        self.store.place_order(order)
        expected_order_number = 0  # Assuming this is the first order placed
        self.assertEqual(self.store.orders[expected_order_number], order)
        self.assertEqual(self.store.collection[self.macbook_air_13.get_key_name()].quantity, 8)  # Original 10 - 2
        self.assertEqual(self.store.collection[self.iphone_15_promax.get_key_name()].quantity, 10)  # No change

    def test_list_products(self):
        product_list = self.store.list_products()
        self.assertEqual(len(product_list), 2)
        self.assertIn(('MacBook air 13', 'Air', 'Price: 6000 ₪ ', 'Available: 10'), product_list)

    def test_list_orders(self):
        order = Order(self.client, 0, {self.macbook_air_13.get_key_name(): 2}, "Credit Card")
        self.store.place_order(order)
        order_list = self.store.list_orders()
        self.assertEqual(len(order_list), 1)
        self.assertEqual(order_list[0][1], 'Client Check')

    def test_sale_prodduct_type(self):
        self.store.sale_prodduct_type("1", 10)
        self.assertIn(" * -10% discount on all TVs * ", self.store.sales)

    def test_new_discount(self):
        self.store.new_discount([self.macbook_air_13, self.iphone_15_promax], 10)
        self.assertEqual(self.macbook_air_13.price, 5400)  # 10% discount on 6000
        self.assertEqual(self.iphone_15_promax.price, 4500)  # 10% discount on 5000

    def test_remove_discount(self):
        self.store.new_discount([self.macbook_air_13, self.iphone_15_promax], 10)
        self.store.remove_discount(self.macbook_air_13)
        self.assertEqual(self.macbook_air_13.price, 6000)  # Discount removed, price back to original


if __name__ == '__main__':
    unittest.main()
