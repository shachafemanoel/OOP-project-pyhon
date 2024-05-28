from Store.user import User
from Store.order import Order


class Client(User):
    def __init__(self, user_id=None, user_full_name=None, password=None, address=None, online=0, payment=None, coupon=None):
        super().__init__(user_id,user_full_name, password, online, address, payment)
        self.order_history = {}
        self.messege = []
        self.new_messege = 0
        self.coupon = coupon

    def update_client (self):
        if self.new_messege > 0:
            new = f"\n * There are {self.new_messege} new notifications for you *\n"
            for messe in self.messege:
                new += messe
                self.new_messege = 0
                self.messege = []
            return f"{new}\n"

        else:
            return f"\n * There are no new notifications *\n "

    def use_coupon(self):
        self.coupon = None

    def new_status(self, order):
        self.order_history[order.order_number] = order
        self.messege.append(f"\n *Order Number:{order.order_number} has been {order.status} *")
        self.new_messege += 1

    def new_order(self,order):
        self.order_history[order.order_number] = order
        self.messege.append(f"\n * Thank you for your purchase!,  Order number: {order.order_number} has been received! *")
        self.new_messege += 1

    def list_orders_client(self):
        return [[f"Order Number: {order_number}",f"Total amount: {order.converter()}",f"Status: {order.status}"] for order_number, order
                in self.order_history.items()]

    def change_address(self, new_address):
        self.address = new_address

    def __str__(self):
        return super().__str__()
