import unittest
from Store.order import Order
from Store.product import Product

class TestOrder(unittest.TestCase):
    def setUp(self):
        self.product1 = Product("Laptop", "Dell XPS 15", 4500.0, 10)
        self.product2 = Product("Smartphone", "iPhone 13", 3500.0, 20)
        self.order = Order("John Doe")

    def test_initial_values(self):
        self.assertEqual(self.order.customer_name, "John Doe")
        self.assertEqual(self.order.total_amount, 0)
        self.assertEqual(self.order.status, "processing")
        self.assertEqual(self.order.product_dict, {})

    def test_change_status(self):
        self.order.change_status(1)
        self.assertEqual(self.order.status, "shipped")

        self.order.change_status(2)
        self.assertEqual(self.order.status, "delivered")

    def test_add_item_to_order(self):
        self.order.add_item_to_order(self.product1, 2)
        self.assertEqual(self.order.product_dict, {"Laptop": 2})
        self.assertEqual(self.order.total_amount, 9000.0)

        self.order.add_item_to_order(self.product2, 1)
        self.assertEqual(self.order.product_dict, {"Laptop": 2, "Smartphone": 1})
        self.assertEqual(self.order.total_amount, 12500.0)

if __name__ == "__main__":
    unittest.main()
