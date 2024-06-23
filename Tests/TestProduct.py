import unittest
from Store.products.product import Product
from Store.rating import Rating
from Store.payment_calculator import CurrencyConverter

class TestProduct(unittest.TestCase):

    def setUp(self):
        self.product = Product("Test Product","Model X","A test product",100.0,10,{5: ["Great product!"]})

    def test_initialization(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.model, "Model X")
        self.assertEqual(self.product.description, "A test product")
        self.assertEqual(self.product.original_price, 100.0)
        self.assertEqual(self.product.price, 100.0)
        self.assertEqual(self.product.sale, 0)
        self.assertEqual(self.product.quantity, 10)
        self.assertIsInstance(self.product.rate, Rating)
        self.assertEqual(self.product.currency, "₪ILS")

    def test_get_key_name(self):
        self.assertEqual(self.product.get_key_name(), "TestProduct")

    def test_get_model_name(self):
        self.assertEqual(self.product.get_model_name(), "ModelX")

    def test_buy_product(self):
        self.product.buy_product(2)
        self.assertEqual(self.product.quantity, 8)

    def test_update_price(self):
        self.product.update_price(20)
        self.assertEqual(self.product.price, 80.0)
        self.assertEqual(self.product.sale, 20)

    def test_remove_discount(self):
        self.product.update_price(20)
        self.product.remove_discount()
        self.assertEqual(self.product.price, 100.0)
        self.assertEqual(self.product.sale, 0)

    def test_change_quantity(self):
        self.product.change_quantity(15)
        self.assertEqual(self.product.quantity, 15)

    def test_get_price(self):
        self.assertEqual(self.product.get_price(2), 200.0)

    def test_get_quantity(self):
        self.assertEqual(self.product.get_quantity(), 10)

    def test_add_quantity(self):
        self.product.add_quantity(5)
        self.assertEqual(self.product.quantity, 15)

    def test_available(self):
        self.assertTrue(self.product.available(5))
        self.assertFalse(self.product.available(15))

    def test_add_review(self):
        self.product.add_review(4, "Good product")
        self.assertEqual(self.product.rate.ratings[4], ["Good product"])

    def test_product_to_dict(self):
        product_dict = self.product.product_to_dict()
        self.assertEqual(product_dict["product_type"], "Product")
        self.assertEqual(product_dict["name"], "Test Product")
        self.assertEqual(product_dict["model"], "Model X")
        self.assertEqual(product_dict["description"], "A test product")
        self.assertEqual(product_dict["price"], 100.0)
        self.assertEqual(product_dict["quantity"], 10)
        self.assertEqual(product_dict["rate"], {5: ["Great product!"]})

    def test_get_price_in_user_currency(self):
        # Ensure CurrencyConverter works as expected
        CurrencyConverter.set_exchange_rates({
            '$USD': 3.71,
            '€EUR': 4.07,
            "₪ILS": 1.00,
        })
        self.assertEqual(
            self.product.get_price_in_user_currency(1),
            "Price: 100.0 ₪ILS"
        )
        self.product.currency = "$USD"
        self.assertEqual(
            self.product.get_price_in_user_currency(1),
            "Price: 26 $USD"
        )

    def test_product_type(self):
        self.assertEqual(self.product.product_type(), "Accessories")


if __name__ == "__main__":
    unittest.main()
