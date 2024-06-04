import unittest
from Store.product import Product
from Store.computer import Computer

class TestComputer(unittest.TestCase):

    def setUp(self):
        # Setup some common test objects
        self.computer1 = Computer("MacBook Air 13", "Air", "Liquid Retina display",
                                  6000, 10, "13", "256", "M2")
        self.computer2 = Computer("MacBook Pro 16", "Pro", "Liquid Retina XDR display",
                                  8000, 5, "16", "512", "M1 Max")

    def test_initialization(self):
        self.assertEqual(self.computer1.name, "MacBook Air 13")
        self.assertEqual(self.computer1.model, "Air")
        self.assertEqual(self.computer1.description, "Liquid Retina display")
        self.assertEqual(self.computer1.price, 6000)
        self.assertEqual(self.computer1.quantity, 10)
        self.assertEqual(self.computer1.size, "13")
        self.assertEqual(self.computer1.storage, "256")
        self.assertEqual(self.computer1.chip, "M2")

    def test_str_no_sale(self):
        expected_str = (
            "======================================\n"
            " Name: MacBook Air 13\n"
            " Model: Air Storge: 256 \n"
            " Chip: M2\n"
            " display size: 13-Inch \n"
            " Description: Liquid Retina display \n"
            " Price: 6000₪\n"
        )
        self.assertIn(expected_str, str(self.computer1))


    def test_str_with_sale(self):
        self.computer2.update_price(20)
        expected_str = (
            '======================================\n'
            ' Name: MacBook Pro 16\n'
            ' Model: Pro Storge: 512 \n'
            ' Chip: M1 Max\n'
            ' display size: 16-Inch \n'
            ' Description: Liquid Retina XDR display \n'
            ' Price:-20% Off 6400.0₪ ILS\n'
            '=================Rating=====================\n'
            'There are no reviews yet'
        )
        self.assertIn(expected_str, str(self.computer2))



if __name__ == '__main__':
    unittest.main()
