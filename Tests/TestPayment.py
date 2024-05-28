import unittest
from Store.payment import Payment

class TestPayment(unittest.TestCase):

    def setUp(self):
        # Setup some common test objects
        self.payment1 = Payment("Nirel Jano", "1234567890", "Credit Card")
        self.payment2 = Payment("Shachaf Emanuel", "0987654321")

    def test_initialization(self):
        self.assertEqual(self.payment1.owner, "Nirel Jano")
        self.assertEqual(self.payment1.info, "1234567890")
        self.assertEqual(self.payment1.payment_method, "Credit Card")
        self.assertEqual(self.payment1.amount_of_payments, 1)

    def test_check_card_valid(self):
        result = self.payment2.check_card(3)
        self.assertTrue(result)
        self.assertEqual(self.payment2.payment_method, "Credit Card")
        self.assertEqual(self.payment2.amount_of_payments, 3)

    def test_check_card_invalid(self):
        invalid_payment = Payment("Nirel jano", "12453")
        result = invalid_payment.check_card(4)
        self.assertFalse(result)
        self.assertNotEqual(invalid_payment.payment_method, "Credit Card")
        self.assertEqual(invalid_payment.amount_of_payments, 1)

    def test_str_with_credit_card(self):
        expected_str = ("Payment method:  7890 Credit Card\n"
                        "Number of payments:1")
        self.assertEqual(str(self.payment1), expected_str)

    def test_str_without_credit_card(self):
        self.payment2.payment_method = "Cash"
        expected_str = ("Payment method: Cash")

        self.assertEqual(str(self.payment2), expected_str)

if __name__ == '__main__':
    unittest.main()
