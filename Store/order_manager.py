from Store.json import DataManager

class OrderManager:
    def __init__(self):
        self.orders = {}
        self.order_number = 1
        self.new_message = []
        self.new_update = 0
        self.revenue = 0
    def load_orders(self, users):
        self.orders = DataManager.load_orders(users)
        self.order_number = len(self.orders) + 1
        for order in self.orders.values():
            self.revenue += order.total_amount
    def save_orders(self):
        DataManager.save_orders(self.orders)



    def list_orders(self):
        if self.orders:
            table = "\n            Orders History    \n"
            table += "-----------------------------------------\n"
            for key, value in self.orders.items():
                table += f"Order number:{key:<12}  \n{value.converter():<18} | Status: {value.status}\n"
                table += "-----------------------------------------\n"
        else:
            table = "\n * There are no orders *\n"
        return table

    def change_order_status(self, order_number, choice):
        self.orders[order_number].change_status(choice)
        order = self.orders[order_number]


    def user_order_history(self, user):
        user_orders_dict = {}
        for order in self.orders.values():
            if order.customer == user:
                user_orders_dict[order.order_number] = order
        return user_orders_dict
