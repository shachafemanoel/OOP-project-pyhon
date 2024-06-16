import unittest
from Store.products.phone import Phone

class TestPhone(unittest.TestCase):

    def setUp(self):
        # Setup some common test objects
        self.phone1 = Phone('Iphone 15', 'Pro max', "The new Iphone 15 pro max ", 5000, 10, "5.9", '256')
        self.phone2 = Phone("Samsung Galaxy S21", "Ultra", "The latest Galaxy with Snapdragon 888", 4500, 10, "6.8", "256")

    def test_initialization(self):
        self.assertEqual(self.phone1.name, "Iphone 15")
        self.assertEqual(self.phone1.model, "Pro max")
        self.assertEqual(self.phone1.description, "The new Iphone 15 pro max ")
        self.assertEqual(self.phone1.price, 5000)
        self.assertEqual(self.phone1.quantity, 10)
        self.assertEqual(self.phone1.size, "5.9")
        self.assertEqual(self.phone1.storage, '256')

    def test_str_no_sale(self):
        expected_str = ('======================================\nName: Iphone 15\n Model: Pro max Storge: 256 \ndisplay size: 5.9-Inch  \nDescription: The new Iphone 15 pro max  \n Price: 5000₪\n=================Rating=====================\nThere are no reviews yet')
        self.assertIn(expected_str, str(self.phone1))

    def test_str_with_sale(self):
        self.phone2.update_price(15)
        expected_str = ('======================================\nName: Samsung Galaxy S21\nModel: Ultra Storge: 256\ndisplay size: 6.8-Inch\nDescription: The latest Galaxy with Snapdragon 888\nPrice:-15% Off 3825.0₪ ILS\n=================Rating=====================\nThere are no reviews yet'
)
        self.assertIn(expected_str, str(self.phone2))

if __name__ == '__main__':
    unittest.main()
