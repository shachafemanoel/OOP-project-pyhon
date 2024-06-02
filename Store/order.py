from Store.user import User
from Store.payment import Payment
class Order:
    def __init__(self, customer=None, order_number=None, product_dict=None, payment=None,total_amount = None,status = None):  # כדי ליצור אובייקט יש לקבל שם לקוח ומילון של שמות מוצרים שהמפתח הוא השם והערך הוא הכמות
        self.order_number = order_number
        self.customer = customer
        if total_amount is None:
            self.total_amount = 0
        else:
            self.total_amount = total_amount
        if payment is not None:
            self.payment = payment
        else:
            self.payment = None
        if status is None:
            self.status = "Processing"
        else:
            self.status = status
        if product_dict is None:
            self.product_dict = {}
        else:
            self.product_dict = product_dict
    # להוסיף פונקציה שמעדכנת סטטוס הזמנה
    def change_status(self, choice: int):
        ship = 'shipped'
        deli = 'delivered'
        if choice == 1:
            self.status = ship
        elif choice == 2:
            self.status = deli



    def order_to_dict(self):
        dict = {}
        dict['order_number'] = self.order_number
        dict['customer_id'] = self.customer.user_id
        dict['total_amount'] = self.total_amount
        dict['payment'] = self.payment.payment_to_dict()
        dict['status'] = self.status
        dict['product_dict'] = self.product_dict
        return dict



    def order_completed(self):
        self.status = 'completed'

    def converter(self):
        if self.payment is not None and self.payment.amount_of_payments != 1:
            if self.customer.address[0:3].casefold() != "isr":
                return f"\nTotal amount: {round(self.total_amount/3.7611,2)} US$ \n * {round((self.total_amount / 3.7611 / self.payment.amount_of_payments), 2)} US$ /mo for {self.payment.amount_of_payments} month *"
            else:
                return f"\nTotal amount: {self.total_amount}  ₪ILS\n * {round(self.total_amount / self.payment.amount_of_payments, 2)} ₪ILS /mo for {self.payment.amount_of_payments} month *"
        elif  self.customer.address[0:3].casefold() != "isr":
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
            if key.casefold()[0:3] == cleaned_name.casefold()[0:3]:
                found.append(key)
        return key

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
            if self.payment is not None:
                return f"===================\nOrder number: {self.order_number}\nCustomer: {self.customer.user_full_name}\n===================\nShipping address: {self.customer.address}\nItems: {self.product_dict}\n================= \nStatus:{self.status}\n===================\n{self.payment}\n{self.converter()}\n==================="
            else:
                return f"{self.list_products()} \nSubtotal: {self.converter()} \n "
        else:
            return "Empty cart"