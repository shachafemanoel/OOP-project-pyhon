class Payment:
    def __init__(self,owner = None,info = None,payment_method = None):
        self.owner = owner
        self.info = info
        self.payment_methood = payment_method

    def check_card(self):
        if len(self.owner) > 0 and len(self.info) >10:
            self.payment_methood = "Credit Card"
            return True
        else:
            return False
    def __str__(self):
        if self.payment_methood == "Credit Card":
            return f" Paid by:  {self.info[-4:]} Credit Card"
        else:
            return f" Paid by {self.payment_methood}"