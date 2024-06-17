import unittest

from Store.rating import Rating


class TestRating(unittest.TestCase):

    def setUp(self):
        self.rating = Rating({5: ["Excellent product!"], 3: ["Average quality."], 1: ["Not satisfied."]})

    def test_initialization(self):
        self.assertEqual(self.rating.ratings[5], ["Excellent product!"])
        self.assertEqual(self.rating.ratings[3], ["Average quality."])
        self.assertEqual(self.rating.ratings[1], ["Not satisfied."])

    def test_add_review(self):
        self.rating.add_review(4, "Good product")
        self.assertEqual(self.rating.ratings[4], ["Good product"])

    def test_weighted_average_rating(self):
        # Test average rating calculation
        self.assertEqual(self.rating.weighted_average_rating(), 3)

    def test_str(self):
        expected_str = ('=================Rating=====================\n'
                        '⭐⭐⭐⭐⭐ review:  Excellent product!\n'
                        '⭐⭐⭐ review:  Average quality.\n'
                        '⭐ review:  Not satisfied.\n'
                        ' Average Rating: 3.0 ⭐')
        self.assertEqual(str(self.rating), expected_str)


if __name__ == '__main__':
    unittest.main()
