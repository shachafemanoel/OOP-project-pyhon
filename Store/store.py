from Store.order import Order
from Store.product import Product
from Store.user import User


class Store:  # מחלקה שמממשת את החנות עצמה

    def __init__(self):
        self.collection = {}  # קולקציית המוצרים שבחנות
        self.users = {}  # משתמשי החנות
        self.orders = {}  # הזמנות החנות
        self.order_number = 1  # מספר הזמנה

    def add_product(self, product):
        if product.name not in self.collection:
            self.collection[product.name] = product
            return True  # במידה ונוסף למלאי ולא קיים כבר אחד
        return False

    def add_user(self, user):  # הוספת משתמש לחנות
        if user.user_id not in self.users:
            self.users[user.user_id] = user
            return True
        return False

    def add_item_order(self, product, how_many, order):
        if product.name in self.collection:
            if self.collection[product.name].available(how_many):
                new_order = order
                new_order.add_item_to_order(product, how_many)
                self.collection[product.name].buy_product(how_many)
            else:
                return False, f"Sorry there is only{self.collection[product.name].quantity} of {product.name} in  the inventory"
        else:
            return False, f"Sorry,There is not{product.name} is our shop"

    def place_order(self, order):
        self.orders[self.order_number] = order
        self.order_number += 1

    def list_products(self):
        return [(name, product.description, product.price, product.quantity) for name, product in
                self.collection.items()]

    def list_orders(self):
        return [(order_number, order.customer_name, order.total_amount, order.status) for order_number, order in
                self.orders.items()]


# יצירת הזמנה עם המוצרים שנוצרו קודם

# יצירת המוצרים
product1 = Product("Laptop", "Dell XPS 15", 4500.0, 10)
product2 = Product("Smartphone", "iPhone 13", 3500.0, 20)
product3 = Product("Headphones", "Sony WH-1000XM4", 1200.0, 15)

# יצירת החנות והוספת המוצרים אליה
store = Store()
store.add_product(product1)
store.add_product(product2)
store.add_product(product3)

order = Order("John Doe")
store.add_item_order(product1, 2, order)
store.add_item_order(product2, 1, order)
store.add_item_order(product3, 3, order)
shachaf = User(2073, "shachaf", 783434)
store.add_user(shachaf)
print(order)
for key, value in store.users.items():
    print(key, ':', value)
