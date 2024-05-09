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
            return f"Payment method:  {self.info[-4:]} {self.payment_method}"
        else:
            return f"Payment method: {self.payment_method} "