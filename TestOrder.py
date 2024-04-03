import unittest
from Store.order import Order
from Store.product import Product


class TestOrder(unittest.TestCase):
    def test_constructor(self):
        # נבדוק את פעולת הבנאי
        order = Order("Test Customer")
        self.assertEqual(order.customer_name, "Test Customer")
        self.assertEqual(order.total_amount, 0)
        self.assertEqual(order.status, "processing")
        self.assertEqual(order.product_dict, {})

    def test_add_item_to_order(self):
        # נבדוק את פעולת ההוספה של מוצר להזמנה
        order = Order("Test Customer")
        product = Product("Test Product", "Test Description", 10.0, 100)

        # נוסיף מוצר להזמנה
        order.add_item_to_order(product, 5)

        # נבדוק אם המוצר נוסף בהצלחה
        self.assertTrue("Test Product" in order.product_dict)
        self.assertEqual(order.product_dict["Test Product"], 5)

        # נבדוק את העדכון בכמות הכוללת ובסכום הכולל
        self.assertEqual(order.total_amount, 50)

        # נבדוק אם המוצר נכנס להזמנה בכמות תקינה
        self.assertTrue(order.add_item_to_order(product, 10))

        # נבדוק אם המוצר אינו נכנס להזמנה בכמות שאינה תקינה
        self.assertFalse(order.add_item_to_order(product, 150))


if __name__ == '__main__':
    unittest.main()
