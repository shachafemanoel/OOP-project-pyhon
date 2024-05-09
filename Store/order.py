class Order:
    def __init__(self,customer=None,order_number = None,product_dict=None,payment = None):  # כדי ליצור אובייקט יש לקבל שם לקוח ומילון של שמות מוצרים שהמפתח הוא השם והערך הוא הכמות
        self.order_number = order_number
        self.customer = customer
        self.total_amount = 0
        self.payment = payment
        if self.payment is None:
            self.status = "Not Paid "
        else:
            self.status = "Processing"
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

    def converter(self):
        if self.customer.address[0:3].casefold() != "israel"[0:3]:
            return f"{self.total_amount}₪ILS   or {self.total_amount/3.7611} US$"
        else:
            return f"{self.total_amount}₪ILS"


    def pay_order(self, payme):
        self.payment = payme
        self.status = "Processing"

    def add_item_to_order(self, product, how_many):
        if product.get_key_name() not in self.product_dict:
            self.product_dict[product.get_key_name()] = how_many
        else:
            self.product_dict[product.get_key_name()] += how_many
        self.total_amount += product.get_price(how_many)

    def list_products(self):
        if len(self.product_dict) > 0:
            result = ""
            for key,value in self.product_dict.items():
                result += key + f" -------- quantity  {str(value)} \n"
            return result
    def __str__(self):
        if self.payment is not None:
            return f"Order number: {self.order_number}\nCustomer: {self.customer.user_full_name}\nShipping address: {self.customer.address}\nItems: {self.product_dict}\nTotal amount: {self.converter()} \nStatus:{self.status}"
        else:
            return f"{self.list_products()} \nTotal amount: {self.converter()} \n "
