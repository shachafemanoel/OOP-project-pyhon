from Store.store import Store
from Store.order import Order
from Store.product import Product
from Store.user import User
from Store.client import Client
from Store.payment import Payment
from Store.reporting import Reporting
from Store.tv import Tv
from Store.phone import Phone
from Store.computer import Computer
class StoreCLI:
    def __init__(self):
        self.store = Store()

    def log_in(self,user):
        user_id = input("Enter User ID: ")
        if user_id.isdigit():
            user_id = int(user_id)
            if user_id in self.store.users:
                user = self.store.users[user_id]
                password = input("Enter Password: ")
                user.login(password)
                if type(user) == User:
                    user.__class__ = User
        return user

    def register(self, new_user=None):
        print("\nWelcome to the registration systemֿ\n")
        print(" User id must be a at least 4 digit ")
        user_id = input("Enter User ID: ")
        if user_id.isdigit() and len(user_id) > 3:
            print("\n Full name must be at least 4 characters ")
            full_name = input("Enter your Full name: ")
            if len(full_name) > 3:
                address = input("\nEnter your address: ")  # Move address input here
                print("\n The password must contain at least 4 characters ")
                pass_word = input("Enter your Password: ")
                if len(pass_word) > 3:
                    new_user = Client(int(user_id), full_name, pass_word)
                    if self.store.add_user(new_user):
                        new_user.online = 1
                        print("\nUser registered successfully.")
                    else:
                        print("\n User already exists please try to log in ")
                else:
                    print("\n The password must contain at least 4 characters. Please try again ")
            else:
                print("\n Invalid full name. Try again ")
        else:
            print("\n User ID must be at least 4 digit.Try again ")
        return new_user

    def display_user(self):
        print("\n Welcome to Electronic Store Management System!\n ")
        print("1. Existing User? Log in")
        print("2. New User? Sign up now ")
        print("3. Exit")
        choice = input("\nEnter your choice: ")
        return choice

    def display_client(self):
        print("\n1. Change address")
        print("2. List of products")
        print("3. Place order")
        print("4. Historical orders")
        #print("5 Rating products")
        print("6 Exit")
        choice = input("\nEnter your choice: ")
        return choice

    def set_address(self,user):
        new_address = input("Enter your address: ")
        self.store.users[user.user_id].change_address(new_address)
        print("\nAddress has been changed successfully")
        print(f"f New Address: {new_address}")


    def display_order(self):
        print("\n 1.Add Item ")
        print("\n 2.Check Out or Exit ")
        choice = input(" Enter your choice: ")
        return choice

    def display_payment(self,order):
        print(order)
        print("\nHow would you like to pay?")
        print("\n 1.Credit Card ")
        print("\n 2.Paypal")
        print("\n 3.Cash")
        print("\n 4.Exit ")
        choice = input(" Enter your choice: ")
        return choice
    def pay(self,order,user):
        print(f"{order.total_amount}₪\n {order.total_amount/3.711} $")

        paymethood = Payment()
        if user.payment is not None:
            print(f"for paying with:")
            print(user.payment)
            s = input(" \n Press 1:")
            if s == '1':
                return user.payment
        else:
            pay_option = self.display_payment(order)
            while True:
                if pay_option =='1':
                    card_holder = input("Name on card ")
                    card_number = input("Card number ")
                    paymethood =Payment(card_holder,card_number,)
                    if paymethood.check_card():

                        print("\nWould you like to save your payment method for future orders?")
                        print("\n 1.Yes,save it")
                        print("\n 2 .No ")
                        save = input("Enter your choice: ")
                        if save =='1':
                            self.store.users[user.user_id].payment = paymethood
                        return paymethood
                    else:
                        print("The card number is invalid")

                elif pay_option == '2':
                    paypal_id = input("Enter your Paypal id")
                    if len(paypal_id) > 0:
                        paymethood = Payment(paypal_id,None,'paypal')
                        print("\nWould you like to save your payment method for future orders?")
                        print("\n 1.Yes,save it")
                        print("\n 2 .No ")
                        save = input("Enter your choice: ")
                        if save == '1':
                            self.store.users[user.user_id].payment = paymethood
                        return paymethood
                    else:
                        print("Paypal id in invalid ")

                elif pay_option == '3':
                    paymethood = Payment(order.customer.user_full_name,None,'Cash')
                    return paymethood

                elif pay_option == '4':
                    print('Good bye')
                    return False
                else:
                    print("\n Invalid choice. Please try again.")

    def change_status(self):
        print(f"{self.store.list_orders()}")
        order_num = input("\nPlease Enter the order number: ")
        number = int(order_num)
        if number in self.store.orders:
            print(f"{self.store.orders[number]}")
            print("1, new status - Shipped")
            print("2, new status - Delivered")
            choice = input("Enter your choice: ")
            if choice == '1' or choice == '2':
                self.store.orders[number].change_status(int(choice))
                print(f"{self.store.orders[number]}")
            else:
                print("Invalid choice.The status has not changed")
        else:
            print("Wrong order number")

    def display_product_type(self):
        print("Select Product type")
        print("\n1.TV")
        print("2.Computer")
        print("3.Mobile Phone ")
        print("Other")
        choice = input("Enter Your Choice")
        return choice
    def display_menu(self):
            print(" \n Electronic store Management System \n")
            print("1. Add Product")
            print("2. Add User")
            print("3. Place Order")
            print("4. Update order status")
            print("5. Remove Product")
            print("6. List Product")
            print("7. List Orders")
            print("8. Reporting")
            print("9. Exit")
            choice = input("Enter your choice: ")
            return choice

    def pick_item(self,lst,item):
        item_cheack = (False,item)
        if len(lst)==0:
           return item_cheack
        if len(lst)==1:
            return item_cheack

        for i in range(len(lst)):
            print(f"\n {lst[i]} \n  \n for {lst[i].name} Press  {i+1} \n", )
        print("Choose number or press other number to look for something more specific\n")
        select = input("Enter your choice")
        if select.isdigit():
            select = int(select)-1
            if select < len(lst):
                item_cheack = (True,lst[select])
                return item_cheack
            else:
                return item_cheack


    def search_system(self):
        print("Welcome to the catalog")
        count = 0
        new_item = Product()
        tup_item = (False,new_item)
        type_item = self.display_product_type()
        type_search = self.store.search(None, type_item)
        if len(type_search) >0:
            tup_item = self.pick_item(type_search,new_item)
            if tup_item[0] ==True:
                new_item = tup_item[1]
                return new_item
        if len(type_search) == 0:
            print("No products of this type were found in the system. Please try to search by the name of the product")

        else:
            while tup_item[0] == False:
                print("Try to search for another product")
                count +=1
                new_item = tup_item[1]
                new_name = input("\nEnter Product name: ")
                type_search_name = self.store.search(new_name,type_item)
                tup_item= self.pick_item(type_search_name,new_item)
                if tup_item[0]== False or tup_item:
                    model = input("\nEnter model: ")
                    type_search_name_model = self.store.search(new_name,type_item,model)
                    tup_item = self.pick_item(type_search_name_model,new_item)
                if tup_item[0] == True:
                    new_item = tup_item[1]
                    return new_item

                if count >5:
                    print("\nYou have exceeded the limit of search attempts")
                    return False,
    def add_item(self, order):
        new_item = self.search_system()
        if new_item!=False and new_item is not None:
            print(f"Your choice:\n {new_item}")
            how_much = input("\nEnter a quantity of the following product: ")
            if how_much.isdigit():
                how_much = int(how_much)
                if how_much == 0:
                    print("No quantity provided")
                if  self.store.add_item_order(new_item,how_much,order) == False:
                    print(f"Sorry there is only {self.store.collection[new_item.name].quantity} of {new_item.name} in  the inventory")
                else:
                    print(f"\n{new_item.name}  {how_much}  added to your order !" )

            else:
                print(" \nError: Invalid quantity entered. ")


    def display_adding_products(self):
        print("\n1. Add new product")
        print("2. Add quantity to existing product")
        print("3. Return to primary display")
        choice = input("\nEnter your choice: ")
        return choice

    def add_quantity_to_product(self):
        print(self.store.list_products())
        name = input("Enter Product Name: ")
        quantity = input("Enter Quantity: ")
        if name in self.store.collection and quantity.isdigit() and int(quantity) > 0:
            self.store.collection[name].add_quantatiy(int(quantity))
            print("Quantity added successfully\n")
        else:
            print("Invalid input or product not found.\n")

    def add_product(self):
        name = input("Enter Product Name: ")
        model = input("Enter Product Model: ")
        if name in self.store.collection and self.store.collection[name].model == model:
            print(f" {self.store.collection[name]}\n This product exists in the system. How much would you like to add to the inventory?")
            quan = input("Add quantity: ")
            self.store.collection[name].add_quantity(int(quan))
        else:
            description = input("Enter description: ")
            price = input("Enter Price: ")
            quantity = input("Enter Quantity: ")
            if int(price) > 0 and price.isdigit() and quantity.isdigit():
                price = float(price)
                quantity = int(quantity)
                product = Product(name, model, description, price, quantity)
                self.store.add_product(product)
            else:
                print("Price and Quantity must be a digit ")

    def place_order(self,user):
        new_order = Order(user)
        if user.address is None:
            self.set_address(user)

        else:
            self.add_item(new_order)
            while True:
                choice = self.display_order()
                if choice == '1':
                    self.add_item(new_order)
                elif choice == '2':
                    break
                else:
                    print("Wrong choice,Try again ")

        if new_order.total_amount > 0 or len(new_order.product_dict) > 0:
            payment = self.pay(new_order,user)
            if payment != False:
                    new_order.pay_order(payment)
                    self.store.place_order(new_order)
                    print(f" {new_order}\n {payment}\n The order was successfully completed ")


    def remove_product(self):
        name = input("Enter Product Name: ")
        removed_product = self.store.remove(name)
        if removed_product:
            print(f" {name} has been removed ")
        else:
            print(f" {name} does not exist ")

    def list_products(self):
        if len(self.store.collection) > 0:
            print(self.store.list_products())
        else:
            print(" No products in inventory yet!")

    def orders(self):
        if len(self.store.orders) > 0:
            print(self.store.list_orders())
        else:
            print(' No orders placed yet ')

    def reporting(self):
        print(self.store.reporting)



    def wellcome_page(self):
        user = Client()
        while user.online == 0:
            selection = self.display_user()
            if selection == '1':
                user = self.log_in(user)
            elif selection == '2':
                user = self.register(user)
            elif selection == '3':
                print('Bye, Thank you')
            else:
                print("\n Login failed. Please check your credentials and try again.\n ")


        return user

    def run(self):

        user = self.wellcome_page()
        print(f"\n welcome {user.user_full_name} you are now connected ")

        if type(user) == Client:
            while True:
                sub_choice = self.display_client()
                if sub_choice == '1':
                    self.set_address(user)
                elif sub_choice == '2':
                    self.list_products()
                elif sub_choice == '3':
                    self.place_order(user)
                elif sub_choice == '4':
                    for key,value in user.order_history.items():
                        print(f"Order Number:{key}\n user.order_history[key]")
                elif sub_choice == '5':
                    break
                else:
                    print("\n Invalid choice. Please try again.")

            return "Bye, have a nice day"


        while True:
                    choice = self.display_menu()

                    if choice == '1':
                        while True:
                            sub_choice = self.display_adding_products()
                            if sub_choice == '1':
                                self.add_product()
                            elif sub_choice == '2':
                                self.add_quantity_to_product()
                            elif sub_choice == '3':
                                break
                            else:
                                print("\n Invalid choice. Please try again.")

                    elif choice == '2':
                        self.register()
                    elif choice == '3':
                        self.place_order(user)
                    elif choice == '4':
                        self.change_status()
                    elif choice == '5':
                        self.remove_product()
                    elif choice == '6':
                        self.list_products()
                    elif choice == '7':
                        self.orders()
                    elif choice == '8':
                        self.reporting()
                    elif choice == '9':
                        break
                    else:
                        print("\n Invalid choice. Please try again.")


if __name__ == "__main__":
    cli = StoreCLI()
    cli.run()