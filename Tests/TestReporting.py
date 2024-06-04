import unittest
from Store.reporting import Reporting
from Store.order import Order
from Store.client import Client
from Store.product import Product


class TestReporting(unittest.TestCase):
    def setUp(self):
        self.reporting = Reporting()
        self.client = Client("1234", "Nirel Jano", "1234", "Haifa")
        self.product1 = Product("Macbook16", "Pro", "Powerful laptop", 5000, 10)
        self.product2 = Product("Iphone13", "Pro", "Latest iPhone model", 4000, 5)
        self.order1 = Order(self.client, 1, {'Macbook16': 2}, "Credit Card")
        self.order1.total_amount = 10000
        self.order2 = Order(self.client, 2, {'Iphone13': 3}, "Credit Card")
        self.order2.total_amount = 12000

    def test_initialization(self):
        self.assertEqual(self.reporting.revenue, 0)
        self.assertIsNone(self.reporting.best_sell)
        self.assertEqual(self.reporting.sold_products, {})
        self.assertEqual(self.reporting.message, [])
        self.assertEqual(self.reporting.new_update, 0)

    def test_new_order(self):
        self.reporting.new_order(self.order1)
        self.assertEqual(self.reporting.revenue, 10000)
        self.assertEqual(self.reporting.new_update, 1)
        self.assertIn("Order number: 1", self.reporting.message[0])
        self.reporting.new_order(self.order2)
        self.assertEqual(self.reporting.revenue, 22000)
        self.assertEqual(self.reporting.new_update, 2)
        self.assertIn("Order number: 2", self.reporting.message[1])

    def test_new_sold(self):
        self.reporting.new_sold("Macbook16", 5)
        self.assertEqual(self.reporting.sold_products["Macbook16"], 5)
        self.reporting.new_sold("Macbook16", 3)
        self.assertEqual(self.reporting.sold_products["Macbook16"], 3)
        self.reporting.new_sold("Iphone13", 2)
        self.assertEqual(self.reporting.sold_products["Iphone13"], 2)

    def test_best_sell_product(self):
        self.reporting.sold_products = {'Macbook16': 5, 'Iphone13': 3}
        self.reporting.best_sell_product()
        self.assertEqual(self.reporting.best_sell, 'Macbook16')

    def test_get_sales_report_string(self):
        self.reporting.sold_products = {'Macbook16': 5, 'Iphone13': 3}
        self.reporting.revenue = 4000
        expected_report = (
            '------------------------------\n'
            '     Product sold  table      \n'
            '------------------------------\n'
            '| Product       |       Sold |\n'
            '------------------------------\n'
            '| Macbook16     |          5 |\n'
            '| Iphone13      |          3 |\n'
            '| Store revenue | 4000 ₪ILS  |\n'
            '------------------------------'
        )
        self.assertEqual(self.reporting.get_sales_report_string(), expected_report)


    def test_seen(self):
        self.reporting.new_update = 2
        self.reporting.message = ["Message 1", "Message 2"]
        self.reporting.seen()
        self.assertEqual(self.reporting.new_update, 0)
        self.assertEqual(self.reporting.message, [])


if __name__ == '__main__':
    unittest.main()
