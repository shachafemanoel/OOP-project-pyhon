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
        macbook_air_15 = Computer('MacBook air 15', 'Air',"Liquid Retina display",7000, 10,"15","256","M2")
        iphone_14 = Phone('Iphone 14 pro max', 'Pro max ', " Iphone 14 pro max best value for money !",3000, 10,"6.7","256")
        admin = User("1111","Admin",'1234')
        client1 = Client("2020", "Client Check", '1234', 'Address')
        order1 = Order(client1,0,{macbook_air_13.get_key_name() : 3, iphone_15_promax.get_key_name() : 2})
        client1.order_history[order1.order_number] = order1

        self.collection = {macbook_air_13.get_key_name() : macbook_air_13, iphone_15_promax.get_key_name() : iphone_15_promax, iphone_14.get_key_name() : iphone_14, macbook_air_15.get_key_name() : macbook_air_15, smart_tv.get_key_name() : smart_tv,}  # קולקציית המוצרים שבחנות
        self.users = {admin.user_id:admin, client1.user_id:client1}  # משתמשי החנות
        self.orders = {order1.order_number:order1}  # הזמנות החנות
        self.order_number = 1  # מספר הזמנה
        self.reporting = Reporting()
        for key , item in self.collection.items():
            self.reporting.sold_products[item.name] = 0
    def search(self, name=None, product_type=None, model=None):
        if name is not None:
            cleaned_name = name.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if model is not None:
            cleaned_model = model.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        found = []
        for key, value in self.collection.items():
            if name is not None:     # חיפוש לפי שם
                if value.get_key_name().casefold()[0:len(cleaned_name)] == cleaned_name.casefold():
                    if model is not None and cleaned_model.casefold() == value.get_model_name()[0:len(cleaned_model)].casefold():# חיפוש לפי שם ומודל
                        found.append(value)
                    else:
                        found.append(value)



            if product_type is not None and name is None:
                if product_type == "1":
                    if type(value) == Tv:
                        found.append(value)
                elif product_type == "2":
                    if type(value) == Computer:
                        found.append(value)
                elif product_type == "3":
                    if type(value) == Phone:
                        found.append(value)
                else:
                    if type(value) == Product:
                        found.append(value)


        return found


    def add_product(self, product):
        self.collection[product.get_key_name()] = product
        self.reporting.sold_products[product.name] = 0
        return "Product added successfully."



    def add_user(self, user:User):  # הוספת משתמש לחנות
        if user.user_id not in self.users:
            user = Client(user.user_id, user.user_full_name, user.password)
            self.users[user.user_id.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))] = user
            self.reporting.messege.append(f"  *There is a new client at your store* {user} ")
            self.reporting.new_update +=1
            return True
        return False

    def remove(self, product):
        del self.collection[product.get_key_name()]
        return True


    def add_item_order(self, product, how_many, order):
        if self.collection[product.get_key_name()].available(how_many):
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
                if self.collection[name].get_quantity() <4:
                    self.reporting.messege.append(f" *Less than {self.collection[name].get_quantity()}  left in stock* {self.collection[name]}")
                    self.reporting.new_update +=1
                if name is self.reporting.sold_products:
                    self.reporting.sold_products[name] += quant
                else:
                    self.reporting.sold_products[name] = quant
            self.order_number += 1
            self.reporting.messege.append(f" *A new order has entered the system*   {order}")
            self.reporting.new_update +=1

    def list_products(self):
        if len(self.collection) > 0:
            return [(product.name, product.model, f"Price: {product.price} ₪ ", f"Available: {product.quantity}") for name, product in
                    self.collection.items()]

    def list_orders(self):
        return [[order_number, order.customer.user_full_name, order.total_amount, order.status] for order_number, order in
                self.orders.items()]

    def log (self,user_id,password):
        login = user_id.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if login in self.users and self.users[login].login(password):
            return self.users[login]
        else:
            return None



