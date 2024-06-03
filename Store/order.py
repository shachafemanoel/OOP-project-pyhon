
from Store.user import User
from Store.payment import Payment

class Order:
    def __init__(self, customer=None, order_number=None, product_dict=None, payment=None, total_amount=None, status=None):
        self.order_number = order_number
        self.customer = customer
        self.total_amount = total_amount if total_amount is not None else 0
        self.payment = payment if payment is not None else Payment()
        self.status = status if status is not None else "Not paid"
        self.product_dict = product_dict if product_dict is not None else {}

    def change_status(self, choice: int):
        if choice == 1:
            self.status = 'shipped'
        elif choice == 2:
            self.status = 'delivered'

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
        if self.customer.address and self.payment and self.payment.amount_of_payments != 1:
            if self.customer.address[:3].casefold() != "isr":
                return f"\nTotal amount: {round(self.total_amount / 3.7611, 2)} US$ \n * {round((self.total_amount / 3.7611 / self.payment.amount_of_payments), 2)} US$ /mo for {self.payment.amount_of_payments} month *"
            else:
                return f"\nTotal amount: {self.total_amount} ₪ILS\n * {round(self.total_amount / self.payment.amount_of_payments, 2)} ₪ILS /mo for {self.payment.amount_of_payments} month *"
        elif self.customer.address is None or self.customer.address[:3].casefold() != "isr":
            return f" * {round(self.total_amount / 3.7611, 2)} US$ *\n"
        else:
            return f" * {self.total_amount} ₪ILS *\n"

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

    def remove(self, product, how_many):
        product_key = product.get_key_name()
        if product_key in self.product_dict:
            if how_many > 0:
                if self.product_dict[product_key] >= how_many:
                    self.product_dict[product_key] -= how_many
                    self.total_amount += product.price * how_many
                    product.quantity -= how_many
                    if self.product_dict[product_key] == 0:
                        del self.product_dict[product_key]
                    return True
                return False
            elif how_many == 0:
                self.total_amount -= product.price * self.product_dict[product_key]
                self.product_dict.pop(product.get_key_name())
                return True
        return False

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
        if len(self.product_dict) > 0:
                if self.status == "Processing":
                    return f"===================\nOrder number: {self.order_number}\nCustomer: {self.customer.user_full_name}\n===================\nShipping address: {self.customer.address}\nItems: {self.product_dict}\n================= \nStatus:{self.status}\n===================\n{self.payment}\n{self.converter()}\n==================="
                else:
                    return f"{self.list_products()} \nSubtotal: {self.converter()} \n "
        else:
            return "Empty cart"