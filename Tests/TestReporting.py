import unittest
from Store.reporting import Reporting

class TestReporting(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Reporting class
        self.reporting = Reporting()

    def test_initialization(self):
        # Check if the revenue is initialized to 0
        self.assertEqual(self.reporting.revenue, 0)

        # Check if the best_sell is initialized to None
        self.assertIsNone(self.reporting.best_sell)

        # Check if the sold_products dictionary is empty initially
        self.assertEqual(len(self.reporting.sold_products), 0)

    def test_best_sell_product(self):
        # Add some products to the sold_products dictionary
        self.reporting.sold_products = {'Product1': 10, 'Product2': 15, 'Product3': 8}

        # Check if the best_sell_product method returns the correct best-selling product
        self.assertEqual(self.reporting.best_sell_product(), 'Product2 is the best selling product')

    def test_sold(self):
        # Add some products to the sold_products dictionary
        self.reporting.sold_products = {'Product1': 10, 'Product2': 15, 'Product3': 8}

        # Check if the sold method returns the correct list of sold products
        self.assertEqual(self.reporting.sold(), [('Product1', 10), ('Product2', 15), ('Product3', 8)])

    def test_total_revenue(self):
        # Add some revenue
        self.reporting.revenue = 5000

        # Check if the total_revenue method returns the correct total revenue
        self.assertEqual(self.reporting.total_revenue(), 'Total revenue of our store: 5000₪ ')

if __name__ == '__main__':
    unittest.main()
