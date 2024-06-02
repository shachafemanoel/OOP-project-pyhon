class Rating:
    def __init__(self, rate, description):
        self.rate = rate
        self.description = description

    def rate_to_dict(self):
        dictionary = {}
        dictionary['rate'] = self.rate
        dictionary['description'] = self.description
        return dictionary

    def rate_calcu(self):
        return self.rate*"⭐"


    def __str__(self):
        return f"Rating: {self.rate} \nReview:{self.description}\n======================================"