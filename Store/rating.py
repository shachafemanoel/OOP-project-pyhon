class Rating:
    '''
    A class that represent and manage customer ratings and reviews.
    '''
    def __init__(self, ratings=None):
        '''
        Constructs rating's dict for the Rating object.
        :param ratings: dict
        '''
        if ratings is None:
            self.ratings = {5: [], 4: [], 3: [], 2: [], 1: []}
        else:
            self.ratings = ratings

    @property
    def rating(self):
        '''
        :return: current rating's dict.
        '''
        return self.ratings

    @rating.setter
    def rating(self, ratings):
        """
        Sets the current ratings if provided as a dictionary.
        ratings : dict
        """
        if isinstance(ratings, dict):
            self.ratings = ratings

    def add_review(self, stars, review=None, ):
        """
        Adds a review to the specified star rating. If no review is provided, defaults to "No description provided".

        Parameters
        ----------
        stars : int
            The star rating for the review (1 to 5)
        review : str, optional
        """
        if review is None or review.strip() == "":
            review = "No description provided"
        if stars in self.ratings:
            self.ratings[stars].append(review)
        else:
            self.ratings[stars] = [review]
        return "Thank you for your opinion"

    def precent_rating(self, rating):
        """
        Calculates the percentage of total reviews that a given star rating represents.

        Parameters
        ----------
        rating : list
            The list of reviews for a specific star rating

        :Returns: The percentage of total reviews that the given star rating represents
        -------
        """
        return (len(rating) / self.total_reviews()) * 100

    def total_reviews(self):
        """
        Returns the total number of reviews.
        """
        return sum(len(v) for v in self.ratings.values())

    def weighted_average_rating(self):
        """
        Calculates and returns the weighted average rating, rounded to the nearest half star.
        """
        total_reviews = self.total_reviews()
        if total_reviews == 0:
            return 0
        weighted_sum = sum(int(star) * len(reviews) for star, reviews in self.ratings.items())
        average = weighted_sum / total_reviews
        return round(average * 2) / 2


    def preview_rating(self):
        """
        :return: a preview string of the average rating and total number of ratings.
        """
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
                        review_summary += f"\n==== Rating: {int(star) * "⭐"} ֿ{int(self.precent_rating(reviews))} % of the ratings ====\n"
                    number = 0
                    for review in reviews:
                        number += 1
                        if review != "No description provided":
                            review_summary += f"\n{number}. {review}\n"

        else:
            review_summary += '\nThere are no reviews yet'
        return review_summary
