from Store.storeerror import StoreError


class Payment:
    """
    A class used to represent a Payment
    ...
    Attributes
    ----------
    owner: str
    info: str
    payment_method: str
    amount_of_payments: int
    """
    def __init__(self, owner=None, info=None, payment_method=None, amount_of_payments=None):
        '''
        Constructs all the necessary attributes for the Payment object
        '''
        self.__owner = owner
        self.__info = info
        self.__payment_method = payment_method
        self.__amount_of_payments = int(amount_of_payments) if amount_of_payments else 1

    @property
    def owner(self):
        '''
        :return: Gets the owner of the payment method.
        '''
        return self.__owner

    @owner.setter
    def owner(self, owner):
        '''
        Sets the owner of the payment method.
        :param owner:
        '''
        self.__owner = owner

    @property
    def info(self):
        '''
        :return: Gets the information about the payment method (card number or PayPal ID).
        '''
        return self.__info

    @info.setter
    def info(self, info):
        '''
        Sets the information about the payment method (card number or PayPal ID).
        :param info:
        '''
        self.__info = info

    @property
    def payment_method(self):
        '''
        :return: method of payment.
        '''
        return self.__payment_method

    @payment_method.setter
    def payment_method(self, payment_method):
        '''
        Sets the method of payment.
        :param payment_method:
        '''
        self.__payment_method = payment_method

    @property
    def amount_of_payments(self):
        '''
        :return: number of payments for the order.
        '''
        return self.__amount_of_payments

    @amount_of_payments.setter
    def amount_of_payments(self, amount_of_payments):
        '''
        Sets the number of payments for the order.
        :param amount_of_payments:
        '''
        self.__amount_of_payments = amount_of_payments

    def payment_to_dict_order(self):
        '''
        creating dict with all the arguments of payment that will be saved to Order's and User's JSON file
        :return: dict
        '''
        return {
            'owner': self.owner,
            'info': self.info,
            'payment_method': self.payment_method,
            'amount_of_payments': self.amount_of_payments
        }

    @staticmethod
    def check_card(card_nubmer, how_much):
        '''
        Checks if the card number is valid and the amount is greater than zero.
        :param card_nubmer:
        :param how_much:
        '''
        if len(card_nubmer) >= 8:
            if how_much > 0:
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
