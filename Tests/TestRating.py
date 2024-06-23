import unittest
from Store.rating import Rating

class TestRating(unittest.TestCase):

    def setUp(self):
        self.rating = Rating()

    def test_initialization_empty(self):
        self.assertEqual(self.rating.ratings, {5: [], 4: [], 3: [], 2: [], 1: []})

    def test_initialization_with_data(self):
        ratings_data = {5: ["Great product!"], 4: ["Good"], 3: [], 2: [], 1: ["Bad"]}
        rating_with_data = Rating(ratings_data)
        self.assertEqual(rating_with_data.ratings, ratings_data)

    def test_add_review_with_description(self):
        self.rating.add_review(5, "Excellent")
        self.assertEqual(self.rating.ratings[5], ["Excellent"])

    def test_add_review_without_description(self):
        self.rating.add_review(5)
        self.assertEqual(self.rating.ratings[5], ["No description provided"])
        self.rating.add_review(3, "")
        self.assertEqual(self.rating.ratings[3], ["No description provided"])

    def test_precent_rating(self):
        self.rating.add_review(5, "Excellent")
        self.rating.add_review(4, "Good")
        self.assertEqual(self.rating.precent_rating(self.rating.ratings[5]), 50.0)
        self.assertEqual(self.rating.precent_rating(self.rating.ratings[4]), 50.0)

    def test_total_reviews(self):
        self.rating.add_review(5, "Excellent")
        self.rating.add_review(4, "Good")
        self.assertEqual(self.rating.total_reviews(), 2)

    def test_weighted_average_rating(self):
        self.rating.add_review(5, "Excellent")
        self.rating.add_review(4, "Good")
        self.assertEqual(self.rating.weighted_average_rating(), 4.5)

    def test_weighted_average_rating_no_reviews(self):
        self.assertEqual(self.rating.weighted_average_rating(), 0)

    def test_preview_rating_no_reviews(self):
        self.assertEqual(self.rating.preview_rating(), "No ratings provided yet")

    def test_preview_rating_with_reviews(self):
        self.rating.add_review(5, "Excellent")
        self.rating.add_review(4, "Good")
        self.assertEqual(self.rating.preview_rating(), "4.5 ⭐ of 5 stars \n * 2 global ratings * \n")

    def test_str_no_reviews(self):
        self.assertEqual(str(self.rating), '===============Customer reviews===============\nThere are no reviews yet')

    def test_str_with_reviews(self):
        self.rating.add_review(5, "Excellent")
        self.rating.add_review(4, "Good")
        result = str(self.rating)
        self.assertIn("Average Rating: 4.5 ⭐ out of 5", result)
        self.assertIn("2 global ratings", result)
        self.assertIn('===============Customer reviews===============\n *     Average Rating: 4.5 ⭐ out of 5 * \n *     2 global ratings * \n\n==== Rating: ⭐⭐⭐⭐⭐ ֿ50 % of the ratings ====\n\n1. Excellent\n\n==== Rating: ⭐⭐⭐⭐ ֿ50 % of the ratings ====\n\n1. Good\n', result)


if __name__ == "__main__":
    unittest.main()
