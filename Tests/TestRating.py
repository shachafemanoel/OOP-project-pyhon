import unittest
from Store.rating import Rating

class TestRating(unittest.TestCase):

    def setUp(self):
        # Setup some common test objects
        self.rating1 = Rating(5, "Excellent product!")
        self.rating2 = Rating(3, "Average quality.")
        self.rating3 = Rating(1, "Not satisfied.")

    def test_initialization(self):
        self.assertEqual(self.rating1.rate, 5)
        self.assertEqual(self.rating1.description, "Excellent product!")
        self.assertEqual(self.rating2.rate, 3)
        self.assertEqual(self.rating2.description, "Average quality.")
        self.assertEqual(self.rating3.rate, 1)
        self.assertEqual(self.rating3.description, "Not satisfied.")

    def test_rate_calcu(self):
        self.assertEqual(self.rating1.rate_calcu(), "⭐⭐⭐⭐⭐")
        self.assertEqual(self.rating2.rate_calcu(), "⭐⭐⭐")
        self.assertEqual(self.rating3.rate_calcu(), "⭐")

    def test_str(self):
        expected_str1 = ("Rating: ⭐⭐⭐⭐⭐ \nReview:Excellent product!\n======================================")
        expected_str2 = ("Rating: ⭐⭐⭐ \nReview:Average quality.\n======================================")
        expected_str3 = ("Rating: ⭐ \nReview:Not satisfied.\n======================================")

        self.assertEqual(str(self.rating1), expected_str1)
        self.assertEqual(str(self.rating2), expected_str2)
        self.assertEqual(str(self.rating3), expected_str3)

if __name__ == '__main__':
    unittest.main()
