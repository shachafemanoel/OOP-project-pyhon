from Store.payment import Payment
from Store.user import User
from Store.order import Order
from Store.payment_calculator import CurrencyConverter

class Client(User):
    def __init__(self, user_id, user_full_name, password, address=None, online=0, payment=None, coupon=None, message = None,currency =None,order_history=None):
        super().__init__(user_id, user_full_name, password, online, address, payment)
        if order_history is None:
            self.order_history = {}
        else:
            self.order_history = order_history
        if message is not None:
            self.__message = message
            self.new_message = len(message)
        else:
            self.__message = []
            self.new_message = 0

        if coupon is not None:
            self.__coupon = coupon
        else:
            self.__coupon = 0

        if currency is not None:
            self.__currency = currency
        else:
            self.__currency = "₪ILS"
    @property
    def coupon(self):
        return self.__coupon

    @coupon.setter
    def coupon(self, value):
        if 0 < value < 100:
            self.__coupon = value
        else:
            raise ValueError("Coupon value must be between 0 and 99")

#    def use_coupon(self):
 #       self.__coupon = 0

  #  def update_coupon(self, amount):
   #     self.__coupon = amount

    @property
    def message(self):
        return self.__messege

    @message.setter
    def message(self, value):
        self.__messege = value

    def update_client(self):
        if self.new_message > 0:
            new = f"\n * There are {self.new_message} new notifications for you *\n"
            for message in self.__message:
                new += message
                self.new_message = 0
                self.__message = []
            return f"{new}\n"

        else:
            return f"\n * There are no new notifications *\n "


    @property
    def currency(self):
        return self.__currency
    @currency.setter
    def currency(self, currency):
        if currency.upper() in CurrencyConverter.exchange_rates:
            self.__currency = currency
        else:
            raise ValueError("Currency not supported")

    def new_status(self, order):
        self.order_history[order.order_number] = order
        self.__message.append(f"\n * Order Number:{order.order_number} has been {order.status} *")
        self.new_message += 1

    def new_order(self, order):
        self.__message.append(f"\n * Thank you for your purchase!,  Order number: {order.order_number} has been received! *")
        self.new_message += 1

    def list_orders_client(self):
        if self.order_history:
            table = "            Orders History    \n"
            table += "-----------------------------------------\n"
            for key, value in self.order_history.items():
                table += f"Order number:{key:<12}  \n{value.converter():<18} | Status: {value.status}\n"
                table += "-----------------------------------------\n"
        else:
            table = "\n * There are no orders *\n"
        return table

    def to_dict(self):
        dict = {"message":self.__message,"coupon":self.__coupon,"currency":self.__currency}
        dict = {**super().to_dict(),**dict}
        dict["user_type"] = "Client"
        return dict

    def __str__(self):
        return super().__str__() + f"\nCoupon: {self.__coupon}\nOrder quantity: {len(self.order_history)} orders"
