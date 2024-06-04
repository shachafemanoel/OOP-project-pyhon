from Store.payment import Payment
from Store.user import User
from Store.order import Order


class Client(User):
    def __init__(self, user_id=None, user_full_name=None, password=None, address=None, online=0, payment=None, coupon=None,order_history=None, messege = None, new_messege=None):
        super().__init__(user_id, user_full_name, password, online, address, payment)
        if messege is not None:
            self.__messege = messege
            self.new_messege = len(messege)
        else:
            self.__messege = []
            self.new_messege = 0

        if coupon is not None:
            self.__coupon = coupon
        else:
            self.__coupon = 0
        if order_history:
            self.__order_history = order_history
        else:
            self.__order_history = {}
    @property
    def coupon(self):
        return self.__coupon

    @coupon.setter
    def coupon(self, value):
        if 0 < value < 100:
            self.__coupon = value
        else:
            raise ValueError("Coupon value must be between 0 and 99")

    @property
    def messege(self):
        return self.__messege

    @property
    def order_history(self):
        return self.__order_history

    @order_history.setter
    def order_history(self, order):
        if order is not None:
            self.__order_history.update(order)
            return self.__order_history
        return self.__order_history

    def update_client(self):
        if self.new_messege > 0:
            new = f"\n * There are {self.new_messege} new notifications for you *\n"
            for messe in self.__messege:
                new += messe
                self.new_messege = 0
                self.__messege = []
            return f"{new}\n"

        else:
            return f"\n * There are no new notifications *\n "

    def use_coupon(self):
        self.__coupon = 0

    def update_coupon(self, amount):
        self.__coupon = amount


    def new_status(self, order):
        self.__order_history[order.order_number] = order
        self.__messege.append(f"\n *Order Number:{order.order_number} has been {order.status} *")
        self.new_messege += 1

    def new_order(self,order):
        self.__order_history[order.order_number] = order
        self.__messege.append(f"\n * Thank you for your purchase!,  Order number: {order.order_number} has been received! *")
        self.new_messege += 1

    def list_orders_client(self):
        if self.__order_history is not None:
         return [[f"Order Number: {order_number}",f"Total amount: {order.converter()}",f"Status: {order.status}"] for order_number, order
                in self.__order_history.items()]
        else:
            return []

    def list_orders_to_dict(self,lst):
        for item in lst:
            self.__order_history[item.order_number] = Order(**item)



    def to_dict(self):
        dict = {"messege":self.__messege,"new_messege":self.new_messege,"coupon":self.__coupon}
        dict = {**super().to_dict(),**dict}
        dict["user_type"] = "Client"
        return dict



    def __str__(self):
        return super().__str__() + f"\nCoupon: {self.__coupon}\nOrder History: {len(self.__order_history)} orders"
