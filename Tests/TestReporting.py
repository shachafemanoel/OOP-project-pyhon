import unittest
from Store.reporting import Reporting
from Store.order import Order
from Store.sales import Sales

class TestReporting(unittest.TestCase):

    def setUp(self):
        self.reporting = Reporting()
        self.sales = Sales()

    def test_initialization(self):
        self.assertEqual(self.reporting.revenue, 0)
        self.assertEqual(self.reporting.sold_products, {})
        self.assertIsNone(self.reporting.best_sell)
        self.assertEqual(self.reporting.message, {"orders": [], "products": [], "users": []})
        self.assertEqual(self.reporting.new_update, {"orders": 0, "products": 0, "users": 0})
        self.assertEqual(self.reporting.total_update, 0)

    def test_new_sold(self):
        self.reporting.new_sold("Product A", 10)
        self.assertEqual(self.reporting.sold_products["Product A"], 10)
        self.reporting.new_sold("Product A", 5)
        self.assertEqual(self.reporting.sold_products["Product A"], 15)

    def test_return_products(self):
        self.reporting.new_sold("Product A", 10)
        self.reporting.return_products("Product A", 3)
        self.assertEqual(self.reporting.sold_products["Product A"], 7)

    def test_new_user(self):
        self.reporting.new_user("Client", "John Doe")
        self.assertIn("John Doe", self.reporting.message["users"][0])
        self.assertEqual(self.reporting.new_update["users"], 1)
        self.assertEqual(self.reporting.total_update, 1)

    def test_new_order(self):
        order = Order(1, {}, {"owner": "John Doe", "info": "12345678", "payment_method": "Credit Card", "amount_of_payments": 1}, 100)
        self.reporting.new_order(order)
        self.assertEqual(self.reporting.revenue, 100)
        self.assertIn("Order number: 1", self.reporting.message["orders"][0])
        self.assertEqual(self.reporting.new_update["orders"], 1)
        self.assertEqual(self.reporting.total_update, 1)

    def test_order_canceled(self):
        self.reporting.revenue = 200
        self.reporting.order_canceled(1, 100)
        self.assertEqual(self.reporting.revenue, 100)
        self.assertIn("order has been canceled", self.reporting.message["orders"][0])
        self.assertEqual(self.reporting.new_update["orders"], 1)
        self.assertEqual(self.reporting.total_update, 1)

    def test_best_sell_product(self):
        top_sellers = self.reporting.best_sell_product()
        self.assertIn("No products have been sold yet.",top_sellers)
        self.reporting.new_sold("Product A", 10)
        self.reporting.new_sold("Product B", 20)
        self.reporting.new_sold("Product C", 15)
        self.reporting.new_sold("Product D", 5)
        top_sellers = self.reporting.best_sell_product()
        self.assertIn("1. Product B", top_sellers)
        self.assertIn("2. Product C", top_sellers)
        self.assertIn("3. Product A", top_sellers)

    def test_get_sales_report_string(self):
        self.reporting.new_sold("Product A", 10)
        self.reporting.new_sold("Product B", 5)
        report = self.reporting.get_sales_report_string()
        self.assertIn("Product sold  table", report)
        self.assertIn("Product A", report)
        self.assertIn("Product B", report)
        self.assertIn("Store revenue", report)

    def test_repoting_do_dict(self):
        self.reporting.new_sold("Product A", 10)
        report_dict = self.reporting.repoting_do_dict(self.sales)
        self.assertIn('sold_products', report_dict)
        self.assertIn('best_sell', report_dict)
        self.assertIn('message', report_dict)
        self.assertIn('new_update', report_dict)
        self.assertIn('total_update', report_dict)
        self.assertIn('sales', report_dict)

    def test_product_warning(self):
        self.reporting.product_warning(3, "Product A")
        self.assertIn("Warning:Less than 3 left in stock Product A", self.reporting.message["products"][0])
        self.assertEqual(self.reporting.new_update["products"], 1)
        self.assertEqual(self.reporting.total_update, 1)

    def test_nofiction(self):
        self.reporting.new_update = {"orders": 1, "products": 1, "users": 1}
        self.reporting.total_update = 3
        notifications = self.reporting.nofiction()
        self.assertIn("orders Manager * 1 new notification *", notifications)
        self.assertIn("products Manager * 1 new notification *", notifications)
        self.assertIn("users Manager * 1 new notification *", notifications)

    def test_str(self):
        self.reporting.new_sold("Product A", 10)
        report_str = str(self.reporting)
        self.assertIn("**** Reporting summary ****", report_str)
        self.assertIn("Top selling products", report_str)
        self.assertIn("Product A", report_str)

if __name__ == "__main__":
    unittest.main()
