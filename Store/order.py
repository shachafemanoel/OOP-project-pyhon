class Order:
    def __init__(self, customer, product_dict=None):  # כדי ליצור אובייקט יש לקבל שם לקוח ומילון של שמות מוצרים שהמפתח הוא השם והערך הוא הכמות
        self.customer = customer
        self.total_amount = 0
        self.status = "processing"
        self.product_dict = {}
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
        else:
            return "Wrong choice"


    def add_item_to_order(self, product, how_many):
        if product.name not in self.product_dict:
            self.product_dict[product.name] = how_many
        else:
            self.product_dict[product.name] += how_many
        self.total_amount += product.get_price(how_many)

    def __str__(self):
        return f"Customer: {self.customer.full_name}\nItems: {self.product_dict}\nTotal amount: {self.total_amount}₪ \nStatus:{self.status}"
