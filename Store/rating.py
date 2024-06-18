class Rating:
    def __init__(self, ratings=None):
        if ratings is None:
            self.ratings = {5: [], 4: [], 3: [], 2: [], 1: []}
        else:
            self.ratings = ratings

    @property
    def rating(self):
        return self.ratings

    @rating.setter
    def rating(self, ratings):
        if isinstance(ratings, dict):
            self.ratings = ratings

    def add_review(self, stars, review=None, ):
        if review is None or review.strip() == "":
            review = "No description provided"
        if stars in self.ratings:
            self.ratings[stars].append(review)
        else:
            self.ratings[stars] = [review]
        return "Thank you for your opinion"

    def precent_rating(self, rating):
        return (len(rating) / self.total_reviews()) * 100

    def total_reviews(self):
        return sum(len(v) for v in self.ratings.values())

    def weighted_average_rating(self):
        total_reviews = self.total_reviews()
        if total_reviews == 0:
            return 0
        weighted_sum = sum(int(star) * len(reviews) for star, reviews in self.ratings.items())
        average = weighted_sum / total_reviews
        return round(average * 2) / 2


    def preview_rating(self):
        if self.total_reviews() == 0:
            return "No ratings provided yet"
        else:
            return f"{self.weighted_average_rating()} ⭐ of 5 stars \n * {self.total_reviews()} global ratings * \n"
    def __str__(self):
        review_summary = '===============Customer reviews==============='
        if self.total_reviews() > 0:
            review_summary += f"\n *     Average Rating: {self.weighted_average_rating()} ⭐ out of 5 * "
            review_summary += f"\n *     {self.total_reviews()} global ratings * \n"
            if self.ratings and sum(len(v) for v in self.ratings.values()) > 0:
                for star, reviews in self.ratings.items():
                    if len(reviews) > 0:
                        review_summary += f"\n==== Rating: {int(star) * "⭐"} ֿ{int(self.precent_rating(reviews))} % of the ratings ===="
                    number = 0
                    for review in reviews:
                        number += 1
                        if review != "No description provided":
                            review_summary += f"\n{number}. {review}"

        else:
            review_summary += '\nThere are no reviews yet'
        return review_summary
