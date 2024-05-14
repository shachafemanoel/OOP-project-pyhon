import unittest

from Store.product import Product


class TestProduct(unittest.TestCase):
    def test_constructor(self):
        self.product = Product("Tablet", "13 MAX", "The new model", 10000, 100, [2,4,3,5])
        self.assertEqual(self.product.name, "Tablet")
        self.assertEqual(self.product.model, "13 MAX")
        self.assertEqual(self.product.description, "The new model")
        self.assertEqual(self.product.price, 10000)
        self.assertEqual(self.product.quantity, 100)
        self.assertEqual(self.product.rate, [2,4,3,5])

