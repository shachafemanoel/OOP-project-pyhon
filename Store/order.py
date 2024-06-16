from Store.payment import Payment
from Store.payment_calculator import CurrencyConverter
class Order:
    def __init__(self, order_number, product_dict, payment, total_amount,address = None ,status=None,customer=None):
        self.order_number = order_number
        self.customer = customer
        self.total_amount = total_amount
        self.payment = Payment(**payment)
        self.status = "Processing" if status is None else status
        self.product_dict = product_dict
        self.currency = "₪ILS"
        self.address = address
    def change_status(self, choice: int):
        if choice == 1:
            self.status = 'Shipped'
        elif choice == 2:
            self.status = 'Delivered'
        elif choice == 3:
            self.status = 'Canceled'

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
        return f" Total amount: {CurrencyConverter.convert(self.total_amount, "₪ILS", self.currency) } {self.currency}"

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
