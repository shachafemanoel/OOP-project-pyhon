import unittest
from Store.client import Client
from Store.order import Order
from Store.payment_calculator import CurrencyConverter

class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client("1234","John Doe","password123","123 Main St",0,None,None,"₪ILS",{})
        self.order = Order(1, None, {
            "owner": "John Doe",
            "info": "1234567812345678",
            "payment_method": "Credit Card",
            "amount_of_payments": 1}, None, "₪ILS","123 Main St")
    def test_initialization(self):
        self.assertEqual(self.client.user_id, "1234")
        self.assertEqual(self.client.user_full_name, "John Doe")
        self.assertEqual(self.client.password, "password123")
        self.assertEqual(self.client.address, "123 Main St")
        self.assertEqual(self.client.online, 0)
        self.assertEqual(self.client.currency, "₪ILS")
        self.assertEqual(self.client.order_history, {})
        self.assertEqual(self.client.message, [])
        self.assertEqual(self.client.new_message, 0)

    def test_set_message(self):
        self.client.message = ["New message"]
        self.assertEqual(self.client.message, ["New message"])

    def test_update_client_no_notifications(self):
        result = self.client.update_client()
        self.assertEqual(result, "\n * There are no new notifications *\n ")

    def test_update_client_with_notifications(self):
        self.client.message = ["New message"]
        self.client.new_message = 1
        result = self.client.update_client()
        self.assertIn("New message", result)
        self.assertEqual(self.client.new_message, 0)
        self.assertEqual(self.client.message, [])

    def test_currency_setter(self):
        self.client.currency = "$USD"
        self.assertEqual(self.client.currency, "$USD")

    def test_new_status(self):
        order = self.order
        self.client.new_status(order)
        self.assertIn(order.order_number, self.client.order_history)
        self.assertEqual(self.client.order_history[order.order_number], order)
        self.assertEqual(self.client.new_message, 1)

    def test_new_order(self):
        order = self.order
        self.client.new_order(order)
        self.assertIn("Thank you for your purchase!", self.client.message[0])
        self.assertEqual(self.client.new_message, 1)

    def test_list_orders_client_no_orders(self):
        result = self.client.list_orders_client()
        self.assertEqual(result, "\n * There are no orders *\n")

    def test_list_orders_client_with_orders(self):
        order = self.order
        self.client.order_history[1] = order
        result = self.client.list_orders_client()
        self.assertIn("Orders History", result)
        self.assertIn("Order number:1", result)
        self.assertIn("Orders History    \n-----------------------------------------\nOrder number:1             \n Total amount: None ₪ILS | Status: Processing\n-----------------------------------------\n", result)

    def test_to_dict(self):
        self.client.message = ["New message"]
        result = self.client.to_dict()
        self.assertEqual(result["message"], ["New message"])
        self.assertEqual(result["currency"], "₪ILS")
        self.assertEqual(result["user_type"], "Client")

    def test_str(self):
        result = str(self.client)
        self.assertIn("User:", result)
        self.assertIn("Order quantity: 0 orders", result)

if __name__ == "__main__":
    unittest.main()
