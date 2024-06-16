import unittest
from Store.products.product import Product
from Store.rating import Rating

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Tablet", "13 MAX", "The new model", 10000, 100, {4: ["Great product!"]})
        self.rating = Rating({4: ["Great product!"]})

    def test_initialization(self):
        self.assertEqual(self.product.name, "Tablet")
        self.assertEqual(self.product.model, "13 MAX")
        self.assertEqual(self.product.description, "The new model")
        self.assertEqual(self.product.original_price, 10000)
        self.assertEqual(self.product.price, 10000)
        self.assertEqual(self.product.quantity, 100)
        self.assertEqual(self.product.rate.weighted_average_rating(), 4)
        self.assertEqual(self.product.sale, 0)

    def test_buy_product(self):
        self.assertTrue(self.product.buy_product(10))
        self.assertEqual(self.product.quantity, 90)
        self.assertFalse(self.product.buy_product(200))
        self.assertEqual(self.product.quantity, 90)

    def test_update_and_remove_discount(self):
        self.product.update_price(10)  # 10% discount
        self.assertEqual(self.product.sale, 10)
        self.assertEqual(self.product.price, 9000)
        self.product.remove_discount()
        self.assertEqual(self.product.sale, 0)
        self.assertEqual(self.product.price, 10000)

    def test_change_quantity(self):
        self.product.change_quantity(1000)
        self.assertEqual(self.product.quantity, 1000)

    def test_add_quantity(self):
        self.product.add_quantity(20)
        self.assertEqual(self.product.quantity, 120)

    def test_get_quantity(self):
        self.assertEqual(self.product.get_quantity(), 100)

    def test_available(self):
        self.assertTrue(self.product.available(100))
        self.assertFalse(self.product.available(2000))

    def test_add_review(self):
        self.product.add_review(4, 'Great product!')
        self.assertEqual(self.product.rate.weighted_average_rating(), 4)
        self.assertEqual(self.product.rate.ratings[4][0], "Great product!")


if __name__ == '__main__':
    unittest.main()
