import unittest
from Store.payment import Payment
from Store.storeerror import StoreError

class TestPayment(unittest.TestCase):

    def setUp(self):
        self.payment = Payment( "John Doe", "1234567812345678","Credit Card",1)

    def test_initialization(self):
        self.assertEqual(self.payment.owner, "John Doe")
        self.assertEqual(self.payment.info, "1234567812345678")
        self.assertEqual(self.payment.payment_method, "Credit Card")
        self.assertEqual(self.payment.amount_of_payments, 1)

    def test_owner_setter(self):
        self.payment.owner = "Jane Doe"
        self.assertEqual(self.payment.owner, "Jane Doe")

    def test_info_setter(self):
        self.payment.info = "8765432187654321"
        self.assertEqual(self.payment.info, "8765432187654321")

    def test_payment_method_setter(self):
        self.payment.payment_method = "PayPal"
        self.assertEqual(self.payment.payment_method, "PayPal")

    def test_amount_of_payments_setter(self):
        self.payment.amount_of_payments = 3
        self.assertEqual(self.payment.amount_of_payments, 3)

    def test_payment_to_dict_order(self):
        payment_dict = self.payment.payment_to_dict_order()
        self.assertEqual(payment_dict["owner"], "John Doe")
        self.assertEqual(payment_dict["info"], "1234567812345678")
        self.assertEqual(payment_dict["payment_method"], "Credit Card")
        self.assertEqual(payment_dict["amount_of_payments"], 1)

    def test_check_card_valid(self):
        self.assertTrue(Payment.check_card("1234567812345678", 100))

    def test_check_card_invalid_number(self):
        with self.assertRaises(StoreError.InvalidCardNumberError):
            Payment.check_card("1234", 100)

    def test_check_card_invalid_amount(self):
        with self.assertRaises(StoreError.InvalidInputError):
            Payment.check_card("1234567812345678", -100)

    def test_str_credit_card(self):
        self.assertEqual(
            str(self.payment),
            " Amount of payments: 1\n ******* 1234 Credit Card"
        )

    def test_str_paypal(self):
        self.payment.payment_method = "PayPal"
        self.payment.info = "john.doe@example.com"
        self.assertEqual(str(self.payment), "john.doe@example.com PayPal")

    def test_str_other_method(self):
        self.payment.payment_method = "Bank Transfer"
        self.assertEqual(str(self.payment), "Bank Transfer")

if __name__ == "__main__":
    unittest.main()
