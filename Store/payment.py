class Payment:
    def __init__(self, owner=None, info=None, payment_method=None):
        self.owner = owner
        self.info = info
        self.payment_method = payment_method







    def __str__(self):
        if self.payment_method == "Credit Card":
            return f"Payment method:  {self.info[-4:]} {self.payment_method}\n==================="
        else:
            return f"Payment method: {self.payment_method}\n=================== "