class Rating:
    def __init__(self, rate, description):
        self.rate = rate
        self.description = description




    def __str__(self):
        return f"Rating: {self.rate} ⭐ \nReview:{self.description}\n======================================"