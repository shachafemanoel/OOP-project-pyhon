from Store.user import User
from Store.order import Order


class Client(User):
    def __init__(self, user_id=None, full_name=None, password=None, address=None, order_history=None, online=0, payment=None, coupon=None):
        super().__init__(user_id, full_name, password, online, address, payment)
        if order_history is None:
            self.order_history = {}
        else:
            self.order_history = order_history
        self.messege = []
        self.new_messege = 0
        self.coupon = coupon

    def update_client (self):
        if self.new_messege > 0 and len(self.order_history) >0:
            new = f"\n * There are {self.new_messege} new updates for you *\n"
            for messe in self.messege:
                new += messe
                self.new_messege = 0
                self.messege = []
            return f"{new}\n \n* Your Orders *\n {self.list_orders()}"

        else:
            return f"\n * There are no new notifications *\n No orders placed yet "


    def new_status(self,order):
        self.order_history[order.order_number] = order
        self.messege.append(f"\n *Order Number:{order.order_number} has been {order.status} *")
        self.new_messege += 1

    def new_order(self,order):
        self.order_history[order.order_number] = order
        self.messege.append(f"\n * Thank you for your purchase!,  Order number: {order.order_number} has been received! *\n")
        self.new_messege +=1

    def change_address(self, new_address):
        self.address = new_address

    def list_orders(self):
        return [(order_number, f"Order total amount: {order.total_amount}", f"status: {order.status}") for
                order_number, order in self.order_history.items()]

    def __str__(self):
        return super().__str__()
