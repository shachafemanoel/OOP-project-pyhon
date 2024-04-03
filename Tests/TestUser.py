import unittest

from Store.user import User


class TestUser(unittest.TestCase):
    def test_constructor(self):
        user = User(123456789, "Nirel", 123456789)
        self.assertEqual(user.user_id, 123456789)
        self.assertEqual(user.user_full_name, 'Nirel')
        self.assertEqual(user.password, 123456789)

    def test_login(self):
        user = User('123456789', "Nirel", '123456789')
        self.assertTrue(user.login("123456789", "123456789"))
        self.assertFalse(user.login("123456782", "123456789"))
        self.assertFalse(user.login("123456789", "123456782"))

    def test_authenticate(self):
        user = User('123456789', "Nirel", '123456789')
        self.assertTrue(user.authenticate("123456789", "123456789"))
        self.assertFalse(user.authenticate("123456782", "123456789"))
        self.assertFalse(user.authenticate("123456789", "123456782"))


if __name__ == '__main__':
    unittest.main()
