from Store.payment import Payment
from Store.payment_calculator import CurrencyConverter
from Store.payment_calculator import InstallmentPayment


class Order:
    """
    A class used to represent a Customer Order.
    ...
    Attributes
    ----------
    order_number : int
    product_dict: Dict
    payment: Payment
    total_amount: int
    currency: str
    address: str
    status: str
    customer_name: str
    """
    def __init__(self, order_number, product_dict, payment, total_amount, currency=None, address=None, status=None,
                 customer=None):
        '''
        Constructs all the necessary attributes for the Order object.
        '''
        self.order_number = order_number
        self.customer = customer
        self.__total_amount = total_amount
        self.__payment = Payment(**payment)
        self.status = "Processing" if status is None else status
        self.product_dict = product_dict
        self.currency = "₪ILS" if currency is None else currency
        self.address = address

    def change_status(self, choice: int):
        '''
        Function that get a choice (number) that will change the order's status
        :param choice:
        :return:
        '''
        if choice == 1:
            self.status = 'Shipped'
        elif choice == 2:
            self.status = 'Delivered'
        elif choice == 3:
            self.status = 'Canceled'

    @property
    def total_amount(self):
        '''
        :return: order's total amount
        '''
        return self.__total_amount

    @total_amount.setter
    def total_amount(self, amount):
        '''
        Updating the order's total amount after adding products and quantity
        :param amount:
        '''
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        else:
            self.__total_amount = amount

    @property
    def payment(self):
        '''
        :return: create Payment's object
        '''
        return self.__payment

    @payment.setter
    def payment(self, payment):
        '''
        Setting payment as object or dict
        :param payment:
        '''
        if isinstance(payment, Payment):
            self.__payment = payment
        if isinstance(payment, dict):
            self.__payment = Payment(**payment)


    def order_to_dict(self):
        '''
        creating dict with all the arguments of order that will be saved to Order's JSON file
        :return: dict
        '''
        order_dict = {
            'order_number': self.order_number,
            'customer_id': self.customer.user_id,
            'total_amount': self.total_amount,
            'payment': self.payment.payment_to_dict_order(),
            'status': self.status,
            'product_dict': self.product_dict
        }
        return order_dict

    def order_completed(self):
        '''
        After order's has been completed the order's status will change to "completed"
        '''
        self.status = 'completed'

    def converter(self):
        '''
        Converts the total amount to the appropriate currency and returns a summary string
        :return: Summary string
        '''
        pay = f" Total amount: {CurrencyConverter.convert(self.total_amount, "₪ILS", self.currency)} {self.currency}"
        if self.status == 'Canceled':
            pay += "\n ** Order canceled, payment method not charged ** "
        else:
            if self.payment.amount_of_payments > 1:
                pay += self.payments()
        return pay

    def payments(self):
        '''
        Calculates and returns the estimated monthly payment amount if the payment is in installments.
        :return: Summary string of amount to pay
        '''
        pay = CurrencyConverter.convert(self.total_amount, "₪ILS", self.currency)
        return f"\nEstimated payment each month:{InstallmentPayment.calculate_installment_amount(pay, self.payment.amount_of_payments)} {self.currency}"


    def __str__(self):
        return f"===================\nOrder number: {self.order_number}\nCustomer: {self.customer.user_full_name}\n===================\nShipping address: {self.customer.address}\nItems: {self.product_dict}\n================= \nStatus:{self.status}\n===================\n{self.payment}\n{self.converter()}\n==================="
