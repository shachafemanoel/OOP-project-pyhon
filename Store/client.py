from Store.user import User
from Store.user import User

from Store.storeerror import StoreError

class Client(User):
    '''
    Client class represent client in our store and attributes for Client object
    '''
    def __init__(self, user_id, user_full_name, password, address=None, online=0, payment=None,message = None,currency =None,order_history=None):
        '''
        Client constructor
        :param user_id: str
        :param user_full_name: str
        :param password: str
        :param address: str, optional
        :param online: int
        :param payment: Payment object, optional
        :param message: list, optional
        :param currency: str, optional
        :param order_history: dict, optional
        '''
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



        if currency is not None:
            self.__currency = currency
        else:
            self.__currency = "₪ILS"


    @property
    def message(self):
        '''
        :return: message
        '''
        return self.__messege

    @message.setter
    def message(self, value):
        '''
        Sets new message
        '''
        self.__messege = value

    def update_client(self):
        '''
        Update client object with new message
        :return: all messages or that there are no notifications
        '''
        try:
            if self.new_message > 0:
                new = f"\n * There are {self.new_message} new notifications for you *\n"
                for message in self.__message:
                    new += message
                self.new_message = 0
                self.__message = []
                return f"{new}\n"
            else:
                return f"\n * There are no new notifications *\n "
        except Exception as e:
            return f"\n * An error occurred while checking notifications: {e} *\n"

    @property
    def currency(self):
        '''
        :return: currency
        '''
        return self.__currency

    @currency.setter
    def currency(self, currency):
        '''
        Sets new currency
        :param currency:
        :return:
        '''
        try:
            if currency.upper() in CurrencyConverter.exchange_rates:
                self.__currency = currency
        except:
            raise ValueError("Currency not supported")

    def new_status(self, order):
        '''
        Adding message that order status has been changed
        :param order:
        '''
        self.order_history[order.order_number] = order
        self.__message.append(f"\n * Order Number:{order.order_number} has been {order.status} *")
        self.new_message += 1

    def new_order(self, order):
        '''
        Adding message that order has been made
        :param order:
        :return:
        '''
        self.__message.append(f"\n * Thank you for your purchase!,  Order number: {order.order_number} has been received! *")
        self.new_message += 1

    def list_orders_client(self):
        '''
        :return: string that represents orders list for client
        '''
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
        '''
        :return: dictionary to JSON data
        '''
        dict = {"message":self.__message,"currency":self.__currency}
        dict = {**super().to_dict(),**dict}
        dict["user_type"] = "Client"
        return dict

    def __str__(self):
        '''
        :return: string representation of client
        '''
        return super().__str__() + f"\nOrder quantity: {len(self.order_history)} orders"
