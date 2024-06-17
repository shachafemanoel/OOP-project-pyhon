import unittest

from Store.products.tv import Tv


class TestTv(unittest.TestCase):

    def setUp(self):
        # Setup some common test objects
        self.tv1 = Tv("Samsung QLED", "Q80T", "4K UHD Smart TV", 7000, 20, "55", "QLED")
        self.tv2 = Tv("LG OLED", "CX", "4K OLED Smart TV", 9000, 15, "65", "OLED")

    def test_initialization(self):
        self.assertEqual(self.tv1.name, "Samsung QLED")
        self.assertEqual(self.tv1.model, "Q80T")
        self.assertEqual(self.tv1.description, "4K UHD Smart TV")
        self.assertEqual(self.tv1.price, 7000)
        self.assertEqual(self.tv1.quantity, 20)
        self.assertEqual(self.tv1.size, "55")
        self.assertEqual(self.tv1.tv_type, "QLED")

    def test_str_no_sale(self):
        expected_str = (
            '======================================\nName: Samsung QLED\nModel: Q80T\ndisplay size: 55-Inch\nDescription: 4K UHD Smart TV\nPrice: 7000₪\n=================Rating=====================\nThere are no reviews yet')
        self.assertIn(expected_str, str(self.tv1))

    def test_str_with_sale(self):
        self.tv2.update_price(10)
        expected_str = (
            '======================================\nName: LG OLED\nModel: CX\ndisplay size: 65-Inch\nDescription: 4K OLED Smart TV\nPrice:-10% Off 8100.0₪ ILS\n=================Rating=====================\nThere are no reviews yet')
        self.assertIn(expected_str, str(self.tv2))


if __name__ == '__main__':
    unittest.main()
