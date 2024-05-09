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

    def log_in(self, user):
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")
        loggg = self.store.log(user_id, password)
        if loggg is not None :
            user = loggg
            if type(user) == User:
                user.__class__ = User
        return user

    def register(self, new_user=None):
        print("\nWelcome to the registration systemֿ\n")
        print(" User id must be a at least 4 digit ")
        user_id = (input("Enter User ID: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:")))
        if user_id.isdigit() and len(user_id) > 3:
            print("\n Full name must be at least 4 characters ")
            full_name = input("Enter your Full name: ")
            if len(full_name) > 3:
                print("\n The password must contain at least 4 characters ")
                pass_word = str(input("Enter your Password: "))
                if len(pass_word) > 3:
                    new_user = Client(user_id, full_name, pass_word, address)
                    if self.store.add_user(new_user):
                        self.set_address(new_user)
                        new_user.online = 1
                        print("\n * User registered successfully. * ")
                    else:
                        print("\n * User already exists please try to log in *")
                else:
                    print("\n The password must contain at least 4 characters. Please try again ")
            else:
                print("\n * Invalid full name. Try again * ")
        else:
            print("\n * User ID must be at least 4 digit.Try again * ")

        return new_user

    def change_password(self, user):
        old_password = input("\nFor changing password please enter your old password: ")

        if user.password == old_password:
            print("\n * The password must contain at least 4 characters *")
            new_user_password = input("Enter your new password: ")

            if len(new_user_password) > 3:
                user.change_user_password(new_user_password)
                print("\n* Password changed successfully* ")
            else:
                print("\n * The password must contain at least 4 characters. Please try again. * ")
        else:
            print("\n *  Wrong old password, please try again. * ")

    def forgot_password(self):
        id_check = input("\nFor password reset, please enter your ID: ")
        name_check = input("Enter your full name: ")

        if id_check  in self.store.users:
            user = self.store.users[id_check]

            if user is not None and user.user_full_name.casefold() == name_check.casefold() and user.user_id == id_check:
                print("\n * The password must contain at least 4 characters *")
                new_user_password = input("Enter your new password: ")

                if len(new_user_password) > 3:
                    user.change_user_password(new_user_password)
                    print("\n * Password changed successfully, you can now log in *")
                else:
                    print("\n *The password must contain at least 4 characters. Please try again.* ")
            else:
                print("\n * Full name or ID is incorrect. Please try again. *")
        else:
            print("Error,user id not found ")
    def display_user(self):
        print("\n Welcome to Electronic Store Management System!\n ")
        print("1. Existing User? Log in")
        print("2. New User? Sign up now ")
        print("3. Forgot password? Reset here")
        print("4. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))


    def display_client(self,notifications):
        if notifications > 0:
            print(f"\n * There is a new {notifications} notifications Reporting ")
        print("\n1. Change address")
        print("2. List of products")
        print("3. Place order")
        if notifications > 0:
            print(f"4. Orders * {notifications} notifications * ")
        else:
            print("4. Orders")
        print("5. Change password")
        print("6. Logout")
        print("7. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))


    def set_address(self,user):
        print("\n * Please enter the details *\n")
        new_address = input("Country: ")
        city = input("City: ")
        street = input("Street: ")
        apt = input("Building,Apt,Floor: ")
        new_address += f",{city},{street},{apt}"
        self.store.users[user.user_id].change_address(new_address)
        print("\n * Address has been set successfully *")
        print(f"\n * New Address updated: *\n {new_address}")

    def display_order(self):
        print("\n1.Add Item ")
        print("2.Check Out or Exit ")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))


    def display_payment(self,order):
        print(order.converter())
        print("How would you like to pay?")
        print("\n1.Credit Card")
        print("2.Paypal")
        print("3.Cash")
        print("4.Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def pay(self, order, user):
        paymethood = Payment
        if user.payment is not None:
            print(f"for paying with:")
            print(user.payment)
            s = input(" \n Press 1:")
            if s == '1':
                return user.payment
        else:
            pay_option = self.display_payment(order)
            while True:
                if pay_option == '1':
                    card_holder = input("Name on card: ")
                    card_number = input("Card number: ")
                    paymethood = Payment(card_holder, card_number)
                    if paymethood.check_card():

                        print("\nWould you like to save your payment method for future orders?")
                        print("\n1. Yes, save it")
                        print("\n2. No ")
                        save = input("Enter your choice: ")
                        if save == '1':
                            self.store.users[user.user_id].payment = paymethood
                        return paymethood
                    else:
                        print("\n * The card number is invalid * ")

                elif pay_option == '2':
                    paypal_id = input("Enter your Paypal id: ")
                    if len(paypal_id) > 0:
                        paymethood = Payment(paypal_id, None, 'Paypal')
                        print("\nWould you like to save your payment method for future orders?")
                        print("1. Yes,save it")
                        print("2 .No ")
                        save = input("Enter your choice: ")
                        if save == '1':
                            self.store.users[user.user_id].payment = paymethood
                        return paymethood
                    else:
                        print("\n * Paypal id in invalid * ")

                elif pay_option == '3':
                    paymethood = Payment(order.customer.user_full_name, None, 'Cash')
                    return paymethood

                elif pay_option == '4':
                    print('Good bye')
                    return False
                else:
                    print("\n * Invalid choice. Please try again.* ")

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
                self.store.change_order(number,int(choice))
                print(f"\n* Order number:{self.store.orders[number].order_number} New status:{self.store.orders[number].status} *\n")
            else:
                print("\n * Invalid choice.The status has not changed * \n")
        else:
            print("\n * Wrong order number *\n")

    def display_product_type(self):
        print(" Select Product type")
        print("\n1. TV")
        print("2. Computer")
        print("3. Mobile Phone ")
        print("4. Accessories ")
        print(" Other")
        choice = input("\nEnter Your Choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def display_menu(self,notifications):
        if notifications > 0:
            print(f"\n * There is a new {notifications} notifications Reporting ")
        print(" \n *  Electronic store Management System * \n")
        print("1. Add Product")
        print("2. Add User")
        print("3. Change password")
        print("4. Update order status")
        print("5. Remove Product")
        print("6. List Product")
        print("7. List Orders")
        if notifications >0:
            print(f"8. Reporting * {notifications} notifications *")
        else:
            print("8. Reporting")
        print("9. Logout")
        print("10. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def pick_item(self, lst, item):
        item_check = (False,item)
        if len(lst) == 0:
           return item_check
        print("\nPlease select one of the options")
        for i in range(len(lst)):
            print(f"\n {lst[i]} \n  \n for {lst[i].name} Press =>  {i+1} \n", )
        print("Choose one of the options \n 0.For Exit ")
        select = input("Enter your choice: ")
        if select.isdigit():
            select = (int(select)-1)
            if select < len(lst) and select>-2:
                item_check = (True,lst[select-1])
                return item_check

        else:
            print("\n * Invalid choice. Please try again. * ")
            return item_check


    def search_system(self):
        print("\n * Welcome to the catalog *")
        count = 0
        new_item = Product()
        tup_item = (False, new_item)
        type_item = self.display_product_type()
        type_search = self.store.search(None, type_item, None)
        if len(type_search) > 0:
            tup_item = self.pick_item(type_search, new_item)
            if tup_item[0]:
                new_item = tup_item[1]
                return new_item
        if len(type_search) == 0:
            print("No products of this type were found in the system. Please try to search by the name of the product")
        else:
            while True:
                count += 1
                new_item = tup_item[1]
                new_name = input("\nEnter Product name: ")
                type_search_name = self.store.search(new_name, type_item)
                tup_item= self.pick_item(type_search_name, new_item)
                if not tup_item[0]:
                    model = input("Enter model: ")
                    type_search_name_model = self.store.search(new_name, type_item, model)
                    tup_item = self.pick_item(type_search_name_model, new_item)
                if tup_item[0]:
                    new_item = tup_item[1]
                    return new_item

                elif count > 8:
                    print("\nYou have exceeded the limit of search attempts")
                    return None
                else:
                    print("\nTry to search for another product")
    def add_item(self, order):
        new_item = self.search_system()
        if new_item is not None:
            print(f"Your choice:\n {new_item}")
            for i in range(5):
                how_much = input("\nEnter a quantity of the following product: ")
                if how_much.isdigit():
                    how_much = int(how_much)
                    if how_much == 0:
                        print("* No quantity provided *")
                    if not self.store.add_item_order(new_item, how_much, order):
                        print(f" * Sorry there is only {self.store.collection[new_item.get_key_name()].quantity} of {new_item.name} in  the inventory *")
                    else:
                        print(f"\n * {new_item.name} ----- quantity {how_much} added to your order ! *\n{order.converter()} ")
                        break
                else:
                    print(f"\n * Error: Invalid quantity entered.Try Again * ")
                if i == 4:
                    print("* You have passed the possible amount of attempts *")


    def display_adding_products(self):
        print("\n1. Add new product")
        print("2. Add quantity to existing product")
        print("3. Return to primary display")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))


    def add_quantity_to_product(self):
        item = self.search_system()
        amount = int(input("\nEnter a quantity: "))
        if item is not None and amount > 0:
            item.add_quantity(amount)
            print(" * Quantity added successfully * \n")
        else:
            print("* Invalid input or product not found. * \n")

    def add_product(self):
        pro = Product()
        name = input("Enter Product Name: ")
        model = input("Enter Product Model: ")
        search = self.store.search(name, model)
        if len(self.store.search(name, model)) >0:
            print(f"* \n This products exists in the system. * ")
            s = self.pick_item(search, pro)
            if s[0]:
                pro = s[1]
                print(f"\n{pro}")
                print("How much would you like to add to the inventory?")
                quan = input("Add quantity: ")
                self.store.collection[pro.get_key_name()].add_quantity(int(quan))
        else:

            description = input("Enter description: ")
            price = input("Enter Price: ")
            quantity = input("Enter Quantity: ")
            category = self.display_product_type()
            if int(price) > 0 and price.isdigit() and quantity.isdigit():
                price = float(price)
                quantity = int(quantity)
                if category == 1 :
                    size = input("Enter Screen size: ")
                    tv_type = input("Enter TV type")
                    pro =Tv(name,model,description,price,quantity,size,tv_type)
                if category == 2 :
                    chip = input("Enter Chip: ")
                    size = input("Enter Screen size: ")
                    storge = input("Enter Storge:")
                    pro = Computer(name, model, description, price, quantity,size,storge,chip)
                if category == 3:
                    size = input("Enter Screen size: ")
                    storge = input("Enter Storge:")
                    pro = Phone(name, model, description, price, quantity,size,storge)
                else:
                    pro = Product(name, model, description, price, quantity, )
                self.store.add_product(pro)
            else:
                print("* Price and Quantity must be a digit *")

    def place_order(self, user):
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
                    print(" * Wrong choice,Try again *")

        if new_order.total_amount > 0 or len(new_order.product_dict) > 0:
            payment = self.pay(new_order, user)
            if payment:
                    new_order.pay_order(payment)
                    self.store.place_order(new_order)

                    print(f" {new_order}\n {payment}\n *The order was successfully completed * ")


    def remove_product(self):
        removed_product = Product()
        removed_product = self.search_system()
        if removed_product is not None:
            name = removed_product.name
            removed_product = self.store.remove(removed_product)
            if removed_product:
                print(f"\n {name} has been removed ")
        else:
            print(f"Good bye")

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

    def orders_history(self,user):
        print("\n Your orders \n")
        print(user.update_client())

    def reporting(self):
        print(self.store.reporting)
        self.store.reporting.seen()



    def wellcome_page(self):
        user = Client()

        while user.online == 0:
            selection = self.display_user()
            if selection == '1':
                user = self.log_in(user)
            elif selection == '2':
                user = self.register(user)
            elif selection == '3':
                self.forgot_password()
            elif selection == '4':
                print('Bye, Thank you')
                return None
            else:
                print("\n * Login failed. Please check your credentials and try again. * \n ")
        return user

    def run(self):
        while True:
            user = self.wellcome_page()
            if user is None:
                break

            print(f"\n * Welcome {user.user_full_name}! You are now connected. *")
            logged_out = False

            while not logged_out:
                if type(user) == Client:
                    while True:
                        sub_choice = self.display_client(user.new_messege)
                        if sub_choice == '1':
                            self.set_address(user)
                        elif sub_choice == '2':
                            self.list_products()
                        elif sub_choice == '3':
                            self.place_order(user)
                        elif sub_choice == '4':
                            self.orders_history(user)
                        elif sub_choice == '5':
                            self.change_password(user)

                        elif sub_choice == '6':
                            logged_out = user.logout()
                            break

                        elif sub_choice == '7':
                            return "Bye, have a nice day"
                        else:
                            print("\n * Invalid choice. Please try again. * ")
                else:
                    while True:

                                choice = self.display_menu(self.store.reporting.new_update)

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
                                            print("\n * Invalid choice. Please try again. * ")

                                elif choice == '2':
                                    self.register()
                                elif choice == '3':
                                    self.change_password(user)
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

                                    user.logout()
                                    logged_out = True
                                    break

                                elif choice == '10':
                                    return "Bye, have a nice day"
                                else:
                                    print("\n* Invalid choice. Please try again.* ")


if __name__ == "__main__":
    cli = StoreCLI()
    cli.run()