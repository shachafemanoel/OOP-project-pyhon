class Rating:
    def __init__(self, ratings=None):
        if ratings is None:
            self.ratings = {1: [], 2: [], 3: [], 4: [], 5: []}
        else:
            self.ratings = ratings


    @property
    def rating(self):
        return self.ratings
    @rating.setter
    def rating(self, ratings):
        if isinstance(ratings, dict):
            self.ratings = ratings
    def add_review(self, stars, review=None,):
        if review is None or review.strip() == "":
            review = "No review provided"
        if stars in self.ratings:
            self.ratings[stars].append(review)
        else:
            self.ratings[stars] = [review]
        return "Thank you for your opinion"

    def weighted_average_rating(self):
        total_reviews = sum(len(v) for v in self.ratings.values())
        if total_reviews == 0:
            return 0
        weighted_sum = sum(int(star) * len(reviews) for star, reviews in self.ratings.items())
        average = weighted_sum / total_reviews
        return round(average * 2) / 2

    def __str__(self):
        review_summary = '=================Rating====================='
        if self.ratings and sum(len(v) for v in self.ratings.values()) > 0:
            for star, reviews in self.ratings.items():
                for review in reviews:
                    review_summary += f"\n{int(star) * "⭐"} review:  {review}"
            review_summary += f"\n Average Rating: {self.weighted_average_rating()} ⭐"
        else:
            review_summary += '\nThere are no reviews yet'
        return review_summary
