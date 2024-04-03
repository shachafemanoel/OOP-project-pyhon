import unittest
from Store.store import Store
from Store.order import Order
from Store.product import Product
from Store.user import User

class TestStore(unittest.TestCase):
    def test_add_product(self):
        # נבדוק את פעולת ההוספה של מוצר לחנות
        store = Store()
        product = Product("Test Product", "Test Description", 10.0, 100)

        # נוסיף מוצר לחנות
        store.add_product(product)

        # נבדוק אם המוצר נוסף לחנות בהצלחה
        self.assertTrue("Test Product" in store.collection)
        self.assertEqual(store.collection["Test Product"], product)

        # נבדוק אם המוצר לא נכנס לחנות במידה והוא כבר קיים
        self.assertFalse(store.add_product(product))

    def test_add_user(self):
        # נבדוק את פעולת ההוספה של משתמש לחנות
        store = Store()
        user = User('123456789', "The User", '123456')

        # נוסיף משתמש לחנות
        store.add_user(user)

        # נבדוק אם המשתמש נוסף לחנות בהצלחה
        self.assertTrue('123456789' in store.users)
        self.assertEqual(store.users['123456789'], user)

        # נבדוק אם המשתמש לא נכנס לחנות במידה והוא כבר קיים
        self.assertFalse(store.add_user(user))

    def test_place_order(self):
        # נבדוק את פעולת ההוספה של הזמנה לחנות
        store = Store()
        order = Order("Test Customer")

        # נוסיף הזמנה לחנות
        store.place_order(order)

        # נבדוק אם ההזמנה נוספה לחנות בהצלחה
        self.assertTrue(1 in store.orders)
        self.assertEqual(store.orders[1], order)


if __name__ == '__main__':
    unittest.main()
