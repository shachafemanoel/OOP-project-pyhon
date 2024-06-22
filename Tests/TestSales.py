import unittest
from Store.sales import Sales
from Store.products.product import Product
from Store.products.computer import Computer
from Store.storeerror import StoreError


class TestSales(unittest.TestCase):
    def setUp(self):
        self.sales = Sales()
        self.product = Computer(name="Product1", model="model", description="description", price=200, quantity=1)

    def test_add_coupon(self):
        self.sales.add_coupon("customer1", 10)
        self.assertEqual(self.sales.get_coupon_discount("customer1"), 10)

    def test_add_invalid_coupon(self):
        with self.assertRaises(StoreError.InvalidInputError):
            self.sales.add_coupon("customer1", 110)

    def test_use_coupon(self):
        self.sales.add_coupon("customer1", 10)
        self.sales.use_coupon_discount("customer1")
        self.assertEqual(self.sales.get_coupon_discount("customer1"), 0)

    def test_add_promotion(self):
        self.sales.add_promotion("TestProduct", 0.15)
        self.assertEqual(self.sales.get_promotion_discount("TestProduct"), 0.15)

    def test_remove_promotion(self):
        self.sales.add_promotion("TestProduct", 0.15)
        self.sales.remove_promotion("TestProduct")
        self.assertEqual(self.sales.get_promotion_discount("TestProduct"), 0)

    def test_update_promotion(self):
        self.sales.add_promotion("TestProduct", 0.15)
        self.sales.update_promotion("TestProduct", 0.25)
        self.assertEqual(self.sales.get_promotion_discount("TestProduct"), 0.25)

    def test_add_category_discount(self):
        self.sales.add_category_discount("Electronics", 0.20)
        self.assertEqual(self.sales.get_category_discount("Electronics"), 0.20)

    def test_remove_category_discount(self):
        self.sales.add_category_discount("Electronics", 0.20)
        self.sales.remove_category_discount("Electronics")
        self.assertEqual(self.sales.get_category_discount("Electronics"), 0)

    def test_update_category_discount(self):
        self.sales.add_category_discount("Electronics", 0.20)
        self.sales.update_category_discount("Electronics", 0.30)
        self.assertEqual(self.sales.get_category_discount("Electronics"), 0.30)

    def test_apply_coupon(self):
        self.sales.add_coupon("customer1", 0.1)
        price_after_discount = self.sales.apply_coupon("customer1", 100.0)
        self.assertEqual(price_after_discount, 90.0)

    def test_apply_promotion(self):
        self.sales.add_promotion("TestProduct", 0.2)
        price_after_discount = self.sales.apply_promotion("TestProduct", 100.0)
        self.assertEqual(price_after_discount, 80.0)

    def test_apply_category_discount(self):
        self.sales.add_category_discount("Electronics", 0.25)
        price_after_discount = self.sales.apply_category_discount("Electronics", 100.0)
        self.assertEqual(price_after_discount, 75.0)

    def test_get_product_discount(self):
        self.sales.add_category_discount("Computer", 25)
        self.sales.add_promotion(self.product.get_key_name(), 20)
        self.assertEqual(self.sales.get_product_discount(self.product), 25)

    def test_sales_to_dict(self):
        self.sales.add_coupon("customer1", 10)
        self.sales.add_promotion("TestProduct", 0.15)
        self.sales.add_category_discount("Electronics", 0.20)
        sales_dict = self.sales.sales_to_dict()
        self.assertIn("coupons", sales_dict)
        self.assertIn("promotions", sales_dict)
        self.assertIn("category_discounts", sales_dict)




if __name__ == '__main__':
    unittest.main()
