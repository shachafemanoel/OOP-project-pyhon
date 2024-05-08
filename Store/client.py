from Store.user import User
from Store.order import Order


class Client(User):
    def __init__(self, user_id=None, full_name=None, password=None, address=None, order_history=None, online=0, payment=None):
        super().__init__(user_id, full_name, password, online, address, payment)
        if order_history is None:
            self.order_history = {}
        else:
            self.order_history = order_history
        self.messege = []
        self.new_messege =0

    def update_client (self):
        if self.new_messegee>0:
            new = f"\n *There is a new {self.new_messege} Updates for you*"
            for messe in range(self.new_messege-1,len(self.messege)):
                new += f"\n{self.messege[messe]}"
            return  new
        else:
            return "\n * There are no new notifications * "

    def new_status(self,order):
        self.order_history[order.order_number] = order
        self.messege.append(f"\n *{order.order_number} has been {order.status}")
        self.new_messege += 1

    def new_order(self,order):
        self.order_history[order.order_number] = order
        self.messege.append(f" *A new order has entered the system*   {order}")
        self.new_messege +=1

    def change_address(self, new_address):
        self.address = new_address

    def list_orders(self):
        return [(order_number, f"Ordr total amount: {order.total_amount}", f"status: {order.status}") for
                order_number, order in self.order_history.items()]

    def __str__(self):
        return super().__str__()
