class Payment:
    def __init__(self, owner=None, info=None, payment_method=None, amount_of_payments=None):
        self.__owner = owner
        self.__info = info
        self.__payment_method = payment_method
        self.__amount_of_payments = 1


    @property
    def owner(self):
        return self.__owner

    @property
    def info(self):
        return self.__info

    @property
    def payment_method(self):
        return self.__payment_method

    @property
    def amount_of_payments(self):
        return self.__amount_of_payments

    def payment_to_dict_order(self):
        if self.__payment_method is None:
            return {}
        dict = {}
        dict['owner'] = self.__owner
        dict['info'] = self.__info
        dict['payment_method'] = self.__payment_method
        dict['amount_of_payments'] = self.__amount_of_payments
        return dict

    def payment_to_dict_user(self):
        if self.__payment_method is None:
            return {}
        dict = {}
        dict['owner'] = self.__owner
        dict['info'] = self.__info
        dict['payment_method'] = self.__payment_method
        return dict

    def check_card(self, how_much):
        if len(self.__owner) > 0 and len(self.__info) >= 8:
            self.__payment_method = "Credit Card"
            self.__amount_of_payments = how_much
            return True
        else:
            return False

    def __str__(self):
        if self.__payment_method == "Credit Card" and self.__info:
            return f"**** **** **** {self.__info[-4:]}"
        else:
            return self.__info
