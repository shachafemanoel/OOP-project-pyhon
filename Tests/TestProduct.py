import unittest

from Store.product import Product


class TestProduct(unittest.TestCase):
    def test_constructor(self):
        # נבדוק את פעולת הבנאי
        product = Product("Test Product", "Test Description", 10.0, 100)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Test Description")
        self.assertEqual(product.price, 10.0)
        self.assertEqual(product.quantity, 100)

    def test_buy_product(self):
        # נבדוק את פעולת הקנייה
        product = Product("Test Product", "Test Description", 10.0, 100)
        self.assertTrue(product.buy_product(50))  # על פי ההנחה יש לקנות 50
        self.assertEqual(product.quantity, 50)  # על פי ההנחה נשארו 50
        self.assertFalse(product.buy_product(100))  # לא מספיק מוצרים, כך שאמור להחזיר False

    # נוסיף פונקציות בדיקה נוספות ככל הצורך...


if __name__ == '__main__':
    unittest.main()
