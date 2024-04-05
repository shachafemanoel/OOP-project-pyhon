import unittest
from Store.reporting import Reporting

class TestReporting(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Reporting class
        self.reporting = Reporting()

    def test_best_sell_product(self):
        self.reporting.sold_products = {'Product1': 10, 'Product2': 15, 'Product3': 8}
        self.assertEqual(self.reporting.best_sell_product(), 'Product2 is the best selling product')

    def test_sold(self):
        self.reporting.sold_products = {'Product1': 10, 'Product2': 15, 'Product3': 8}
        self.assertEqual(self.reporting.sold(), [('Product1', 10), ('Product2', 15), ('Product3', 8)])

    def test_total_revenue(self):
        self.reporting.revenue = 5000
        self.assertEqual(self.reporting.total_revenue(), 'Total revenue of our store: 5000 ₪')

if __name__ == '__main__':
    unittest.main()
