import unittest
from Store.client import Client
from Store.order import Order
from Store.payment import Payment
from Store.payment_calculator import CurrencyConverter, InstallmentPayment

class TestOrder(unittest.TestCase):

    def setUp(self):
        self.client = Client("1234", "John Doe", "password123", "123 Main St", 0, None, None, "₪ILS", {})
        self.payment_info = {
            "owner": "John Doe",
            "info": "1234567812345678",
            "payment_method": "Credit Card",
            "amount_of_payments": 1
        }
        self.order = Order(
            1,
            {"item1": 1, "item2": 2},
            self.payment_info,
            100,
            "₪ILS",
            "123 Main St",
            "Processing",
            self.client)

    def test_initialization(self):
        self.assertEqual(self.order.order_number, 1)
        self.assertEqual(self.order.product_dict, {"item1": 1, "item2": 2})
        self.assertIsInstance(self.order.payment, Payment)
        self.assertEqual(self.order.total_amount, 100)
        self.assertEqual(self.order.currency, "₪ILS")
        self.assertEqual(self.order.address, "123 Main St")
        self.assertEqual(self.order.status, "Processing")
        self.assertEqual(self.order.customer.user_id, "1234")

    def test_change_status(self):
        self.order.change_status(1)
        self.assertEqual(self.order.status, "Shipped")
        self.order.change_status(2)
        self.assertEqual(self.order.status, "Delivered")
        self.order.change_status(3)
        self.assertEqual(self.order.status, "Canceled")

    def test_total_amount_setter(self):
        self.order.total_amount = 200
        self.assertEqual(self.order.total_amount, 200)

    def test_payment_setter(self):
        new_payment_info = {
            "owner": "Jane Doe",
            "info": "8765432187654321",
            "payment_method": "PayPal",
            "amount_of_payments": 2
        }
        self.order.payment = new_payment_info
        self.assertEqual(self.order.payment.owner, "Jane Doe")
        self.assertEqual(self.order.payment.info, "8765432187654321")
        self.assertEqual(self.order.payment.payment_method, "PayPal")
        self.assertEqual(self.order.payment.amount_of_payments, 2)

    def test_order_to_dict(self):
        order_dict = self.order.order_to_dict()
        self.assertEqual(order_dict["order_number"], 1)
        self.assertEqual(order_dict["customer_id"], "1234")
        self.assertEqual(order_dict["total_amount"], 100)
        self.assertEqual(order_dict["payment"]["owner"], "John Doe")
        self.assertEqual(order_dict["status"], "Processing")
        self.assertEqual(order_dict["product_dict"], {"item1": 1, "item2": 2})

    def test_order_completed(self):
        self.order.order_completed()
        self.assertEqual(self.order.status, "completed")

    def test_converter(self):
        result = self.order.converter()
        expected_result = " Total amount: 100 ₪ILS"
        self.assertIn(expected_result, result)

        self.order.status = "Canceled"
        result = self.order.converter()
        self.assertIn("** Order canceled, payment method not charged **", result)

    def test_payments(self):
        self.order.payment.amount_of_payments = 2
        result = self.order.payments()
        self.assertIn("Estimated payment each month:", result)

    def test_str(self):
        result = str(self.order)
        self.assertIn("Order number: 1", result)
        self.assertIn("Customer: John Doe", result)
        self.assertIn("Shipping address: 123 Main St", result)
        self.assertIn("Status:Processing", result)

if __name__ == "__main__":
    unittest.main()
