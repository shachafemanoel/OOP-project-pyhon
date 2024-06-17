import unittest

from Store.payment import Payment
from Store.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.payment = Payment("Client Check", "1234567890", "Credit Card", 10)
        self.user = User("1234", "Nirel Jano", '1234', 0, 'Haifa', self.payment)

    def test_initialization(self):
        self.assertEqual(self.user.user_id, "1234")
        self.assertEqual(self.user.user_full_name, "Nirel Jano")
        self.assertEqual(self.user.password, '1234')
        self.assertEqual(self.user.online, 0)
        self.assertEqual(self.user.address, 'Haifa')
        self.assertEqual(self.payment.payment_method, 'Credit Card')

    def test_login(self):
        self.assertFalse(self.user.login("12345"))
        self.assertEqual(self.user.online, 0)
        self.assertTrue(self.user.login("1234"))
        self.assertEqual(self.user.online, 1)

    def test_logout(self):
        self.user.online = 1
        self.assertEqual(self.user.logout(), True)
        self.assertEqual(self.user.online, 0)

    def test_change_address(self):
        self.user.change_address('ISRAEL')
        self.assertEqual(self.user.address, 'ISRAEL')

    def test_change_name(self):
        self.user.change_name("new_name")
        self.assertEqual(self.user.user_full_name, "new_name")

    def test_change_user_password(self):
        self.user.change_user_password("1234567")
        self.assertEqual(self.user.password, "1234567")

    def test_str(self):
        self.assertEqual(str(self.user), "User: Nirel Jano\nID: 1234")


if __name__ == '__main__':
    unittest.main()
