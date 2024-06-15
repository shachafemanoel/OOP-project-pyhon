from Store.storeerror import StoreError
class Payment:
    def __init__(self, owner=None, info=None, payment_method=None, amount_of_payments=None):
        self.__owner = owner
        self.__info = info
        self.__payment_method = payment_method
        self.__amount_of_payments = int(amount_of_payments) if amount_of_payments  else 1

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, owner):
        self.__owner = owner

    @property
    def info(self):
       return self.__info

    @info.setter
    def info(self, info):
        self.__info = info

    @property
    def payment_method(self):
        return self.__payment_method

    @payment_method.setter
    def payment_method(self, payment_method):
        self.__payment_method = payment_method

    @property
    def amount_of_payments(self):
        return self.__amount_of_payments

    @amount_of_payments.setter
    def amount_of_payments(self, amount_of_payments):
        self.__amount_of_payments = amount_of_payments

    def payment_to_dict_order(self):
        return {
            'owner': self.owner,
            'info': self.info,
            'payment_method': self.payment_method,
            'amount_of_payments': self.amount_of_payments
        }

    def payment_to_dict_user(self):
        return {
            'owner': self.owner,
            'info': self.info,
            'payment_method': self.payment_method
        }
    @staticmethod
    def check_card(self,card_nubmer, how_much):
            if len(card_nubmer) >= 8:
                if how_much >0 :
                    return True
                else:
                    raise StoreError.InvalidInputError
            else:
                raise StoreError.InvalidCardNumberError

    def __str__(self):
        if self.__payment_method == "Credit Card":
            return f" Amount of payments: {self.__amount_of_payments}\n ******* {self.__info[:4]} {self.payment_method}"
        elif self.__payment_method == "PayPal":
            return f"{self.__info} {self.payment_method}"
        else:
            return f"{self.payment_method}"