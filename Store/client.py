from Store.user import User
class Client(User):
    def __init__(self,user_id,full_name,password,online = 0,order_history = None,addres):
        self.address = addres
        super().__init__(user_id,full_name,password,online)
        if order_history is None:
            self.order_history = []
        else:
            self.order_history = order_history

    def new_order(self,order):
        self.order_history.append(order)
    def __str__(self):
        return super().__str__() + f", Order History: \n  {self.order_history}"


