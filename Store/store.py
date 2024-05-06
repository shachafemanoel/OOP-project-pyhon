from Store.order import Order
from Store.product import Product
from Store.user import User
from Store.reporting import Reporting
from Store.client import Client
from Store.tv import Tv
from Store.phone import Phone
from Store.computer import Computer

class Store:  # מחלקה שמממשת את החנות עצמה

    def __init__(self):
        smart_tv = Tv("LG 52 Led","UR9000 Series"," Alexa Built-in 4K Smart TV (3840 x 2160),Bluetooth, Wi-Fi, USB, Ethernet, HDMI 60Hz Refresh Rate, AI-Powered 4K",7000,20,"65",'LED')
        macbook_air_13 = Computer('MacBook air 13', 'Air',"Liquid Retina display ",6000, 10,"13","256","M2")
        iphone_15_promax = Phone('Iphone 15', 'Pro max ', "The new Iphone 15 pro max ",5000, 10,"5.9",256)
        macbook_air_15 = Computer('MacBook air 15', 'Air',"Liquid Retina display w",7000, 10,"15","256","M2")
        iphone_14 = Phone('Iphone 14 pro max', 'Pro max ', " Iphone 14 pro max best value for money !",3000, 10,"6.7","256")
        admin = User(1111,"Admin",'1234')
        clinet1 = Client(2020, "Client Check", '1234', 'Address')
        order1 = Order(clinet1,0,{macbook_air_13.name:3,iphone_15_promax.name:2})
        clinet1.order_history[order1.order_number] =order1
        self.collection = {macbook_air_13.name:macbook_air_13,iphone_15_promax.name:iphone_15_promax,iphone_14.name:iphone_14,macbook_air_15.name:macbook_air_15,smart_tv.name:smart_tv}  # קולקציית המוצרים שבחנות
        self.users = {1111:admin,2020:clinet1,}  # משתמשי החנות
        self.orders = {order1.order_number:order1,}  # הזמנות החנות
        self.order_number = 1  # מספר הזמנה
        self.reporting = Reporting()

    def search(self,name = None,product_type = None,model = None):
        found = []
        for key, value in self.collection.items():
            if name is not None and key.casefold()[0:3] == name.casefold()[0:3]:
                if model is not None :
                    if value.model.casefold()[0:3]== model.casefold()[0:3]:
                        found.append(value)
                else:
                    found.append(value)

            if product_type is not None :
                if product_type == type(value):
                    found.append(value)


        return found


    def add_product(self, product):
        if len(self.search(product.name)) ==1 :
                self.collection[product.name].add_quantity(product.quantity)
                return "Product quantity updated successfully."
        else:
            len(self.search(product.name)) == 0
            self.collection[product.name] = product
            self.reporting.sold_products[product.name] = 0
            return "Product added successfully."



    def add_user(self, user:User):  # הוספת משתמש לחנות
        if user.user_id not in self.users:
            user = Client(user.user_id, user.user_full_name, user.password)
            self.users[user.user_id] = user
            return True
        return False

    def remove(self, product_name):
        if product_name in self.collection:
            del self.collection[product_name]
            return True
        else:
            return False

    def add_item_order(self, product, how_many, order):
        if self.collection[product.name].available(how_many):
            order.add_item_to_order(product, how_many)
            return True
        else:
            return False

    def place_order(self, order):
        if order.payment != None:
            self.orders[self.order_number] = order
            order.order_number =self.order_number
            self.reporting.revenue += order.total_amount
            self.users[order.customer.user_id].order_history[order.order_number]=order
            for name , quant in order.product_dict.items():
                self.collection[name].buy_product(quant)
                if name is self.reporting.sold_products:
                    self.reporting.sold_products[name] += quant
                else:
                    self.reporting.sold_products[name] = quant
            self.order_number += 1

    def list_products(self):
        if len(self.collection) > 0:
            return [(name, product.model, f"Price: {product.price} ₪ ", f"Available: {product.quantity}") for name, product in
                    self.collection.items()]

    def list_orders(self):
        return [(order_number, order.customer.user_full_name, order.total_amount, order.status) for order_number, order in
                self.orders.items()]





