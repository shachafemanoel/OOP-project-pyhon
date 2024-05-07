class Payment:
    def __init__(self, owner=None, info=None, payment_method=None):
        self.owner = owner
        self.info = info
        self.payment_method = payment_method

    def check_card(self):
        if len(self.owner) > 0 and len(self.info) >= 10:
            self.payment_method = "Credit Card"
            return True
        else:
            return False

    def __str__(self):
        if self.payment_method == "Credit Card":
            return f"  {self.info[-4:]} Credit Card"
        else:
            return f" {self.payment_method}"