from Store.user import User


class Client(User):
    def __init__(self,user_id = None, full_name = None, password = None,address=None, order_history=None,online = 0,payment = None):
        super().__init__(user_id,full_name, password, online, address)
        if order_history is None:
            self.order_history = {}
        else:
            self.order_history = order_history

    def append_order(self, order):
        self.order_history.append(order)

    def change_address(self, new_address):
        self.address = new_address


    def __str__(self):
        return super().__str__() + f", Order History: \n  {self.history()}"
