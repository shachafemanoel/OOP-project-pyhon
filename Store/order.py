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
        if self.customer.address is not None:
            if self.customer.address[0:3].casefold() != "isr":
                return f"{self.total_amount}₪ILS   or {round(self.total_amount/3.7611,2)} US$"


        return f"{self.total_amount}₪ILS"

    def payments(self):
        return f"{self.total_amount}ILS or {round(self.total_amount/12,2)}₪ILS 12/mo. for 12 mo.*"
    def pay_order(self,payme):
        self.payment = payme
        self.status = "Processing"

    def search(self,name):
        found = []
        cleaned_name = name.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        for key in self.product_dict.keys():
            if key.casefold()[0:len(cleaned_name)] ==cleaned_name.casefold:
                found.append(key)
        return key
    def remove(self, product,how_many):
            if product.get_key_name() in self.product_dict.keys():
                if how_many > 0:
                    self.product_dict[product.get_key_name()] = how_many
                if how_many ==0:
                    self.product_dict.pop(product.get_key_name())
                    return True

                else:
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
            for key,value in self.product_dict.items():
                result += key + f" -------- quantity  {str(value)} \n"
            return result
    def __str__(self):
        if self.payment is not None:
            return f"===================\nOrder number: {self.order_number}\nCustomer: {self.customer.user_full_name}\n===================\nShipping address: {self.customer.address}\nItems: {self.product_dict}\n=================\nTotal amount: {self.converter()} \nStatus:{self.status}\n==================="
        else:
            return f"{self.list_products()} \nSubtotal ({len(self.product_dict)}): {self.converter()} \n "
