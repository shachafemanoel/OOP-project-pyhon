class Rating:
    def __init__(self, rate, description):
        self.rate = rate
        self.description = description

    def rate_calcu(self):
        return self.rate*"⭐"


    def __str__(self):
        return f"Rating: {self.rate_calcu()} \nReview:{self.description}\n======================================"