import unittest

from Store.client import Client
from Store.order import Order
from Store.payment import Payment
from Store.products.product import Product


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.client = Client("1234", "Nirel Jano", "1234", "Haifa")
        self.product1 = Product("Macbook16", "Pro", "Powerful laptop", 5000, 10)
        self.product2 = Product("Iphone13", "Pro", "Latest iPhone model", 4000, 5)
        self.payment = Payment("Client Check", "1234567890", "Credit Card", 10)
        self.order = Order(self.client, 0, {'Macbook16': 3, 'Iphone13': 2}, self.payment)

    def test_initialization(self):
        self.assertEqual(self.order.customer, self.client)
        self.assertEqual(self.order.total_amount, 0)
        self.assertEqual(self.order.status, "Not paid")
        self.assertEqual(len(self.order.product_dict), 2)
        self.assertIsInstance(self.order.payment, Payment)

    def test_change_status(self):
        self.order.change_status(1)
        self.assertEqual(self.order.status, "shipped")
        self.order.change_status(2)
        self.assertEqual(self.order.status, "delivered")

    def test_converter(self):
        self.assertEqual(self.order.converter(), '\nTotal amount: 0.0 US$ \n * 0.0 US$ /mo for 10 month *')
        self.order.total_amount = 4000
        self.assertEqual(self.order.converter(), '\nTotal amount: 1063.52 US$ \n * 106.35 US$ /mo for 10 month *')

    def test_pay_order(self):
        self.order.pay_order("Credit Card")
        self.assertEqual(self.order.payment, "Credit Card")
        self.assertEqual(self.order.status, "Processing")

    def test_search(self):
        self.assertEqual(self.order.search("Iphone 13"), ['Iphone13'])

    def test_remove(self):
        self.order.remove(self.product1, 3)
        self.assertEqual(self.product1.quantity, 7)
        self.assertEqual(self.order.total_amount, 15000)
        self.assertEqual(len(self.order.product_dict), 1)
        self.assertFalse(self.order.remove(self.product1, 40))
        self.assertTrue(self.order.remove(self.product2, 0))
        self.assertEqual(len(self.order.product_dict), 0)
        self.assertEqual(self.order.total_amount, 7000)  # Total amount was 15000 and now - 2 * 4000 = 7000

    def test_add_item_to_order(self):
        self.order.add_item_to_order(self.product1, 3)
        self.assertEqual(self.order.total_amount, 15000)
        self.assertEqual(len(self.order.product_dict), 2)
        self.assertEqual(self.order.product_dict[self.product1.get_key_name()], 6)

    def test_list_products(self):
        expected = 'Macbook16 -------- quantity  3\nIphone13 -------- quantity  2\n'
        self.assertEqual(self.order.list_products(), expected)
        self.order.add_item_to_order(self.product1, 3)
        expected = 'Macbook16 -------- quantity  6\nIphone13 -------- quantity  2\n'
        self.assertEqual(self.order.list_products(), expected)


if __name__ == '__main__':
    unittest.main()
