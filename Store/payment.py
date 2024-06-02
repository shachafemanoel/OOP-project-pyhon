class Payment:
    def __init__(self, owner=None, info=None, payment_method=None,amount_of_payments = None):
        self.owner = owner
        self.info = info
        self.payment_method = payment_method
        self.amount_of_payments = 1




    def payment_to_dict_order(self):
        if self.payment_method is None:
            return {}
        dict = {}
        dict['owner'] = self.owner
        dict['info'] = self.info
        dict['payment_method'] = self.payment_method
        dict['amount_of_payments'] = self.amount_of_payments
        return dict

    def payment_to_dict_user(self):
        if self.payment_method is None:
            return {}
        dict = {}
        dict['owner'] = self.owner
        dict['info'] = self.info
        dict['payment_method'] = self.payment_method
        return dict
    def check_card(self,how_much):
        if len(self.owner) > 0 and len(self.info) >= 8:
            self.payment_method = "Credit Card"
            self.amount_of_payments = how_much
            return True
        else:
            return False

    def __str__(self):
        if self.payment_method == "Credit Card":
            return f"Payment method:  {self.info[-4:]} "

        else:
            return f"Payment method: {self.payment_method}"
