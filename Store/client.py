from Store.user import User
from Store.order import Order

class Client(User):
    def __init__(self,user_id = None, full_name = None, password = None,address=None, order_history=None,online = 0,payment = None):
        super().__init__(user_id,full_name, password, online, address,payment)
        if order_history is None:
            self.order_history = {}
        else:
            self.order_history = order_history


    def change_address(self, new_address):
        self.address = new_address

    def list_orders(self):
        return [(order_number, f"Ordr total amount: {order.total_amount}",f"status: {order.status}" ) for order_number, order
                in
                self.order_history.items()]
    def __str__(self):
        return super().__str__()
