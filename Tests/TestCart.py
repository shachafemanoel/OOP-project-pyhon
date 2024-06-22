import unittest
from Store.cart import Cart
from Store.products.product import Product

class TestCart(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.product1 = Product(name="Product1", model="model",description="description",price=200,quantity=1)
        self.product2 = Product(name="Product2", model="model",description="description",price=200,quantity=1)

    def test_add_product(self):
        self.cart.add_item(self.product1,1)
        self.assertIn(self.product1.get_key_name(), self.cart.product_dict)

    def test_remove_product(self):
        self.cart.add_item(self.product1,1)
        self.cart.change_item_quantity(self.product1,0)
        self.assertNotIn(self.product1.get_key_name(), self.cart.product_dict)

    def test_total_price(self):
        self.cart.add_item(self.product1,1)
        self.cart.add_item(self.product2,1)
        self.assertEqual(self.cart.total_amount, 400.0)

if __name__ == '__main__':
    unittest.main()
