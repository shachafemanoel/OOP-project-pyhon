from Store.payment import Payment
from Store.payment_calculator import CurrencyConverter
from Store.payment_calculator import InstallmentPayment


class Order:
    def __init__(self, order_number, product_dict, payment, total_amount, currency=None, address=None, status=None,
                 customer=None):
        self.order_number = order_number
        self.customer = customer
        self.__total_amount = total_amount
        self.__payment = Payment(**payment)
        self.status = "Processing" if status is None else status
        self.product_dict = product_dict
        self.currency = "₪ILS" if currency is None else currency
        self.address = address

    def change_status(self, choice: int):
        if choice == 1:
            self.status = 'Shipped'
        elif choice == 2:
            self.status = 'Delivered'
        elif choice == 3:
            self.status = 'Canceled'

    @property
    def total_amount(self):
        return self.__total_amount

    @total_amount.setter
    def total_amount(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        else:
            self.__total_amount = amount

    @property
    def payment(self):
        return self.__payment

    @payment.setter
    def payment(self, payment):
        if isinstance(payment, Payment):
            self.__payment = payment
        if isinstance(payment, dict):
            self.__payment = Payment(**payment)

    def order_to_dict(self):
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
        self.status = 'completed'

    def converter(self):
        pay = f" Total amount: {CurrencyConverter.convert(self.total_amount, "₪ILS", self.currency)} {self.currency}"
        if self.status == 'Canceled':
            pay += "\n ** Order canceled payment method not charged ** "
        else:
            if self.payment.amount_of_payments > 1:
                pay += self.payments()
        return pay

    def payments(self):
        pay = CurrencyConverter.convert(self.total_amount, "₪ILS", self.currency)
        return f"\nEstimated payment each month:{InstallmentPayment.calculate_installment_amount(pay, self.payment.amount_of_payments)} {self.currency}"

    def pay_order(self, payment):
        self.payment = payment
        self.status = "Processing"

    def search(self, name):
        found = []
        cleaned_name = name.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        for key in self.product_dict.keys():
            if key.casefold()[:3] == cleaned_name.casefold()[:3]:
                found.append(key)
        return found

    def add_item_to_order(self, product, how_many):
        if product.get_key_name() not in self.product_dict:
            self.product_dict[product.get_key_name()] = how_many
        else:
            self.product_dict[product.get_key_name()] += how_many
        self.total_amount += product.get_price(how_many)

    def list_products(self):
        if len(self.product_dict) > 0:
            result = ""
            for key, value in self.product_dict.items():
                result += key + f" -------- quantity  {str(value)}\n"
            return result

    def __str__(self):
        return f"===================\nOrder number: {self.order_number}\nCustomer: {self.customer.user_full_name}\n===================\nShipping address: {self.customer.address}\nItems: {self.product_dict}\n================= \nStatus:{self.status}\n===================\n{self.payment}\n{self.converter()}\n==================="
