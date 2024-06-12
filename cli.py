from Store.payment_calculator import CurrencyConverter
from Store.store import Store
from Store.product import Product
from Store.user import User
from Store.client import Client
from Store.display import Display
import logging

class StoreCLI:
    def __init__(self):
        self.store = Store()
        self.display = Display()
        self.user = Client("0000" ,"0000" ,"0000" ,online=0)
        self.cart = {
            'total_amount':0,
            'payment': None,
            'product_dict': {},
            "count_item":0
        }
        self.exit = False

    def log_in(self):
        # פונקציית התחברות למערכת הפונקציה מקבלת שם משתמש וסיסמא קוראת לפונקציה בחנות במידה והערכים תקינים יחזור משתמש אם המשתמש מנהל הפונקציה תחבר אותו בתור מנהל
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")
        loggg = self.store.log(user_id, password)
        if loggg is not None:
            self.user = loggg
            if type(self.user) == User:
                self.user.__class__ = User
            logging.warning(f"\n Welcome  {self.user.user_full_name}. you are now connected\n")
        else:
            logging.warning("Login failed!\n")

    def register(self):
        print("\nWelcome to the registration systemֿ\n")
        print(" User id must be a at least 4 digit ")
        user_id = (input("Enter User ID: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:")))
        if user_id.isdigit() and len(user_id) > 3:
            print("\n Full name must be at least 4 characters ")
            user_full_name = input("Enter your Full name: ")
            if len(user_full_name) > 3:
                new_user = self.set_password(user_id, user_full_name)
                if new_user:
                    new_user["user_type"] = "Client"
                    if self.store.add_user(new_user):
                        self.user = self.store.log(new_user["user_id"], new_user["password"])
                        self.set_address()
                        print("\n * User registered successfully. * ")
                        print("Thank you for register. Enjoy a 5% coupon !")
                        logging.info(f"\n{self.user.user_full_name} are now connected\n")
                    else:
                        print("\n * User already exists please try to log in *")

            else:
                print("\n * Invalid full name. Try again * ")
        else:
            print("\n * User ID must be at least 4 digit.Try again * ")


    def register_admin(self,):
        print("\nAdding new admin\n")
        print(" User ID must be at least 4 digits ")
        user_id = input("Enter User ID: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if user_id.isdigit() and len(user_id) > 3:
            print("\n Full name must be at least 4 characters ")
            user_full_name = input("Enter the admin's full name: ")
            if len(user_full_name) > 3:
                print("\n The password must contain at least 4 characters ")
                new_user = self.set_password(user_id, user_full_name)
                if new_user:
                    new_user["user_type"] = "Admin"
                    if self.store.add_user(new_user):
                        print("\n * Admin registered successfully. * ")
                else:
                    print("\n * User already exists please try to log in *")
            else:
                print("\n * Invalid full name. Try again * ")
        else:
            print("\n * User ID must be at least 4 digits. Try again * ")

    def set_password(self,user_id = None,user_full_name = None):
        print("\n * The password must contain at least 4 characters *")
        new_user_password = input("Enter your new password: ")
        if len(new_user_password) > 3:
            if user_id is not None and user_full_name is not None:
                user = {"user_id": user_id, "user_full_name": user_full_name, "password": new_user_password}
                print("\n* Password set successfully* ")
                return user
            else:
                self.user.change_user_password(new_user_password)
        else:
            print("\n * The password must contain at least 4 characters. Please try again. * ")
            return None

    def change_password(self):
        old_password = input("\nFor changing password please enter your old password: ")
        if self.user.password == old_password:
            self.set_password()
        else:
            print("\n *  Wrong old password, please try again. * ")

    def forgot_password(self):
        id_check = input("\nFor password reset, please enter your ID: ")
        name_check = input("Enter your full name: ")
        if id_check in self.store.users:
            user = self.store.users[id_check]
            if user is not None and user.user_full_name.casefold() == name_check.casefold() and user.user_id == id_check:
                print("\n * The password must contain at least 4 characters *")
                new_user_password = input("Enter your new password: ")
                if len(new_user_password) > 3:
                    user.change_user_password(new_user_password)
                    self.user = user
                    print("\n * Password changed successfully, you can now log in *")
                else:
                    print("\n *The password must contain at least 4 characters. Please try again.* ")
            else:
                print("\n * Full name or ID is incorrect. Please try again. *")
        else:
            print("Error,user id not found ")

    def user_manager(self):
        while True:
            sub_choice = self.display.display_manage_user(self.store)
            if sub_choice == "1":
                self.store.client_list()
            elif sub_choice == '2':
                self.register()
                break
            elif sub_choice == "3":
                self.remove_client()
                break
            elif sub_choice == '4':
                self.register_admin()
                break
            elif sub_choice == '5':
                self.change_password()
            elif sub_choice == '6':
                self.update_client_details()
            elif sub_choice == '7':
                break
            else:
                print("\n * Invalid choice. Please try again. *\n")

    def add_review(self, order):
        for key, value in order.product_dict.items():
            print(key)
            print("1. ⭐")
            print("2. ⭐⭐")
            print("3. ⭐⭐⭐")
            print("4. ⭐⭐⭐⭐")
            print("5. ⭐⭐⭐⭐⭐")
            star = input("\nEnter your choice: : ")
            review = input("Enter your opinion: ")
            if star.isdigit():
                star = int(star)
                if 0 < star < 6:
                    self.store.add_review(key,str(star),review)
                else:
                    print("Wrong choice")
            else:
                print("Wrong choice")
        order.order_completed()

    def choice_order(self):
        order_number = input("Enter order number: ")
        if order_number.isdigit():
            order_number = int(order_number)
            if 0 < order_number < self.store.order_number and order_number in self.user.order_history:
                order = self.user.order_history[order_number]
                print(order)
                if order.status == 'delivered':
                    print("Are you interested in giving a review on the order?\n1. Yes!")
                    option = input("Enter your choice: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
                    if option == '1':
                        self.add_review(order)
            else:
                print("\n *Order number is not valid")

    def display_order_user(self):
        print(self.user.update_client())
        if len(self.user.order_history) > 0:
            while True:
                choice = self.display.orders_history(self.user)
                if choice == '1':
                  self.choice_order()
                else:
                    print("Return to Main menu")
                    break

    def set_address(self):
        print(" Add a new address \n * Please enter the details *\n")
        new_address = input("Country: ")
        city = input("City: ")
        street = input("Street: ")
        apt = input("Building,Apt,Floor: ")
        new_address += f",{city},{street},{apt}"
        new_address.replace(" ", "").translate(str.maketrans("", "", ".!?;:"))
        if len(new_address) > 3:
            if self.store.set_address(self.user.user_id,new_address):
                print("\n * Address has been set successfully *")
                print(f"\n * New Address updated: *\n {new_address}")
        else:
            print("\n * Not enough details were entered for setting address. *")

    def new_card(self, paymethod):
        card_holder = input("Name on card: ")
        card_number = input("Card number: ")
        how_much = input("how many payments would you like to spread the deal?: ")
        how_much = int(how_much) if how_much.isdigit() else 1
        if len(card_number) > 6  and card_number.isdigit():
            paymethod["owner"] = card_holder
            paymethod["info"] = card_number
            paymethod["amount_of_payments"] = how_much
            print("\nWould you like to save your payment method for future orders?")
            print("\n1. Yes, save it")
            print("\n2. No ")
            save = input("Enter your choice: ")
            if save == '1':
                self.user.payment = paymethod
            return paymethod
        else:
            print("\n * The card details are invalid * ")


    def new_paypal(self, paymethod):
        paypal_id = input("Enter your Paypal id: ")
        how_much = input("how many payments would you like to spread the deal?: ")
        if len(paypal_id) > 0:
            paymethod["owner"] = self.user.user_full_name
            paymethod["info"] = paypal_id
            paymethod["payment_method"] = "Paypal"
            paymethod["amount_of_payments"] = int(how_much)
            print("\nWould you like to save your payment method for future orders?")
            print("1. Yes,save it")
            print("2 .No ")
            save = input("Enter your choice: ")
            if save == '1':
                self.user.payment = paymethod
            return paymethod
        else:
            print("\n * Paypal id in invalid * ")

    def new_payment(self):
        paymethod = {"owner":"", "info":"", "payment_method":""}
        for i in range(4):
            pay_option = self.display.display_payment()
            if pay_option == '1':
               return self.new_card(paymethod)
            elif pay_option == '2':
               return self.new_paypal(paymethod)
            elif pay_option == '3':
                paymethod ={"owner":self.user.user_full_name,"info":"", "payment_method":'Cash'}
                return paymethod

            elif pay_option == '4':
                print('Good bye')
                return False
            else:

                print("\n * Invalid choice. Please try again.* ")

    def pay(self):
        if self.user.payment is not None:
            self.user.payment["amount_of_payments"] = 1
            print(f"\n===================\nfor paying with:\n")
            print(self.user.get_save_payment())
            s = input("Press 1:")
            if s == '1':
                how_much = input("how many payments would you like to spread the deal?")
                if how_much.isdigit():
                    payment = self.user.payment
                    payment["amount_of_payments"] = int(how_much)
                    return payment

            else:
                return self.new_payment()
        else:
                return self.new_payment()

    def choose_currency(self):
        """
        פונקציה זו מציגה למשתמש רשימת מטבעות אפשריים ובוחרת את סוג המטבע על פי בחירת המשתמש.
        :return: קוד המטבע הנבחר
        """
        currencies = {
            '1': '$USD',
            '2': '€EUR',
            '3': '₪ILS'
        }
        print("choice currency")
        for key, value in currencies.items():
            print(f"{key}: {value}")
        choice = input("Enter your choice: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if choice in currencies.keys():
            self.set_currency(currencies[choice])

        else:
            count = 0
            for i in range(4):
                print(f"Wrong choice. Please try again.You have {4-i} attempts left")
                choice = input("Enter your choice: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
                if choice in currencies:
                   self.set_currency(currencies[choice])

                elif i == 4:
                    print("You have passed the number of attempts.\nThe currency is set to be ILS")

        print(f"Your currency is:{currencies[choice]}")

    def set_currency(self,currency):
        if self.cart["total_amount"] > 0:
            CurrencyConverter.convert(self.cart["total_amount"], self.store.currency, currency)
        self.user.currency = currency
        self.store.change_currency(currency)

    def change_status(self):
        print(f"{self.store.list_orders()}")
        number = input("\nPlease Enter the order number: ")
        if number.isdigit():
            number = int(number)
            if number in self.store.orders:
                print(f"{self.store.orders[number]}")
                print("1, new status - Shipped")
                print("2, new status - Delivered")
                choice = input("Enter your choice: ")
                if choice == '1' or choice == '2':
                    self.store.change_order(number, int(choice))
                    print(f"\n* Order number:{self.store.orders[number].order_number} New status:{self.store.orders[number].status} *\n")
                else:
                    print("\n * Invalid choice.The status has not changed * \n")
            else:
                print("\n * Order did not exist. Please try again. *")
        else:
                print("\n * Invalid order number")

    def product_type(self, choice=None):
        if choice is None:
            choice = self.display.display_product_type()
        for i in range(5):
            if choice in '1234':
                return self.store.search(None, choice, None)
            elif choice == "5":
                return self.list_products()
            elif choice == "0":
                    return None
            else:
                print("Try Again")
                choice = self.display.display_product_type()
        return None

    def discount(self):
        discount = input("Enter amount of % for discount: ")
        if discount.isdigit():
            discount = int(discount)
            return discount
        else:
            discount = 0
            return discount

    def add_discount(self):
        choice = self.display.display_product_type()
        category = self.product_type(choice)
        if category is not None :
            if category[0].sale == 0:
                discount = self.discount()
                self.store.sale_prodduct_type(choice,discount)
                self.store.new_discount(category, discount)
            else:
                category = None
                print("There is a sale for this department")
        if category is None :
            print("\n1. Yes")
            print("For exit, enter a different value from the options ")
            choice = input("\nEnter your choice: ")
            if choice == '1':
                product = self.manual_search()
                if product is not None and product != -100:
                    discount = self.discount()
                    self.store.new_discount(product, discount)
            else:
                print("\nGood bye")

    def remove_discount(self):
        choice = self.display.display_remove_discount()
        if choice == "1":
            category = self.display.display_product_type()
            self.store.remove_discount(category)
        elif choice == "2":
            product_name = self.manual_search()
            if product_name is not None and product_name != -100:
                self.store.remove_discount(product_name)
            else:
                print("\nProduct not found.")
        else:
            print("Invalid choice.")

    def order_manager(self):
        while True:
            choice = self.display.display_manage_order(self.store)
            if choice == "1":
                self.change_status()
            elif choice == "2":
                self.orders()
            elif choice == "3":
                break
            else:
                print("\n * Invalid choice. Please try again. *\n")

    def display_menu(self):
        product_manager = "1. Product Manager"
        order_manager = "3. Order Manager"
        user_manager = "2. User Manager"
        if self.store.reporting.total_update > 0:
            print(f"\n * There are {self.store.reporting.total_update} new notifications *")
            for key,item in self.store.reporting.new_update.items():
                if key == "products" and item >0:
                    product_manager += f" ({item}) new notifications"
                if key == "orders" and item > 0:
                    order_manager += f" ({item}) new notifications"
                if key == "users" and item > 0:
                    user_manager += f" ({item}) new notifications"
        print(" \n *  Electronic store Management Menu * \n")
        print(product_manager)
        print(user_manager)
        print(order_manager)
        print("4. List Product")
        print("5. Reporting")
        print("6. Logout")
        print("0. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))


    def pick_item(self, lst):
        if len(lst) == 0:
            return -100
        print("\nPlease select one of the options")
        for i in range(len(lst)):
            print(f" {lst[i]} \n  \n * for {lst[i].name} Press =>  {i + 1} ", )
            print("======================================")
        print("Choose one of the options \n For exit, enter a different value from the options ")
        select = input("Enter your choice: ")
        if select.isdigit():
            select = int(select)
            if select>0:
                select -= 1
                if len(lst) > select >= -1:
                    return select
            else:
                return -100
        else:
            return -100

    def manual_search(self):
            new_name = input("\nEnter Product name: ")
            search_name = self.store.search(new_name)
            choice = self.pick_item(search_name)
            if choice == -100 and choice is not None:
                    model = input("Enter model: ")
                    search_name_model = self.store.search(new_name, None,model)
                    choice = self.pick_item(search_name_model)
                    if choice != -100 and choice is not None:
                        item = search_name_model[choice]
                    else:
                        item = None
            else:
                item = search_name[choice]
            return item

    def product_manager(self):
        while True:
            sub_choice = self.display.display_manage_product(self.store)
            if sub_choice == '1':
                self.add_product()

            elif sub_choice == '2':
                self.remove_product()

            elif sub_choice == '3':
                self.add_discount()

            elif sub_choice == '4':
                self.remove_discount()
            elif sub_choice == '5':
                break
            else:
                print("\n * Invalid choice. Please try again. *\n")

    def search_system(self):
        print("\n * Welcome to the catalog * \n ")
        if len(self.store.sales) > 0:
            print("   *   New deals   * ")
            for sale in self.store.sales:
                print(sale)
        new_item = None
        type_search = self.product_type()
        if type_search is not None:
            choice = self.pick_item(type_search)
            if choice != -100 and choice is not None:
                new_item = type_search[choice]
            else:
                new_item = None
        if type_search is None:
            print("\n1.Manual search")
            print("2.Exit")
            select = input("\nEnter your choice: ")
            if select == "1":
                new_item = self.manual_search()
            else:
                new_item = None

        return new_item

    def add_item(self):
        new_item = self.search_system()
        if new_item is not None:
            print(f"\nYour choice:\n {new_item}")
            for i in range(5):
                how_much = input("\nEnter a quantity of the following product: ")
                if how_much.isdigit():
                    how_much = int(how_much)
                    if how_much <= 0:
                        print("* No quantity provided *")
                    if not self.store.add_item_order(new_item, how_much):
                        print( f" * Sorry there is only {self.store.collection[new_item.get_key_name()].quantity} of {new_item.name} in  the inventory *")
                    else:
                        if new_item.get_key_name() not in self.cart["product_dict"]:
                            self.cart["product_dict"][new_item.get_key_name()] = how_much
                            self.cart["total_amount"] += new_item.get_price(how_much)
                            self.cart["count_item"] +=how_much

                        else:
                            self.cart["product_dict"][new_item.get_key_name()] += how_much
                            self.cart["total_amount"] += new_item.get_price(how_much)
                            self.cart["count_item"] += how_much
                        print(
                            f"\n * {new_item.name} ----- quantity {how_much} total:{new_item.get_price_in_user_currency(how_much)}  has been successfully add to cart  ! *\n ")
                        break
                else:
                    print(f"\n * Error: Invalid quantity entered.Try Again * ")
                if i == 4:
                    print("* You have passed the possible amount of attempts *")

    def add_quantity_to_product(self):
        item = self.search_system()
        amount = input("\nEnter a quantity: ")
        if amount.isdigit():
            amount = int(amount)
            if item is not None and amount > 0:
                item.add_quantity(amount)
                print(" * Quantity added successfully * \n")
        else:
            print("* Invalid input or product not found. * \n")

    def add_pruduct_categoty(self,dict_new_product):
        category = self.display.display_product_type()
        if category == '1':
            size = input("Enter Screen size: ")
            tv_type = input("Enter TV type: ")
            dict_new_product["size"] = size
            dict_new_product["tv_type"] = tv_type
            dict_new_product["product_type"] = "Tv"
        elif category == '2':
            chip = input("Enter Chip: ")
            size = input("Enter Screen size: ")
            storage = input("Enter storage: ")
            dict_new_product["size"] = size
            dict_new_product["chip"] = chip
            dict_new_product["storage"] = storage
            dict_new_product["product_type"] = 'Computer'
        elif category == '3':
            size = input("Enter Screen size: ")
            storage = input("Enter storage: ")
            dict_new_product["size"] = size
            dict_new_product["storage"] = storage
            dict_new_product["product_type"] = 'Phone'
        if  self.store.add_product(dict_new_product):
            print("Product added successfully")

        else:
            print("\n * One of the entered values is Invalid *\n")

    def add_product(self):
        name = input("Enter Product Name: ")
        model = input("Enter Product Model: ")
        search = self.store.search(name, model)
        if len(search) > 0:
            print(f" \n * This products exists in the system please choose product for adding amount. * ")
            s = self.pick_item(search)
            if s != -100:
                pro = search[s]
                print(f"\n{pro}")
                print("How much would you like to add to the inventory?")
                quantity = input("Add quantity: ")
                if quantity.isdigit():
                    self.store.collection[pro.get_key_name()].add_quantity(int(quantity))
                    print("\n * Quantity added successfully *")
                else:
                    print("Quantity must be a digit!")

        else:

            description = input("Enter description: ")
            price = input("Enter Price: ")
            quantity = input("Enter Quantity: ")
            if price.isdigit() and int(price) > 0 and quantity.isdigit():
                    price = float(price)
                    quantity = int(quantity)
                    dict_new_product = {"name": name, "model": model, "description": description, "price": price,
                                        "quantity": quantity}
                    self.add_pruduct_categoty(dict_new_product)


            else:
                    print("* Price and Quantity must be a digit *")

    def update_client_details(self):
        client_lst = self.store.client_list()
        choice = input("\nChoose Client ID: ")
        if choice in self.store.users:
            client = self.store.users.get(choice)
            while True:
                sub_choice = self.display.display_client_details()
                if sub_choice == "1":
                    new_name = input("\nEnter Client new full name: ")
                    if len(new_name) > 3:
                        client.change_name(new_name)
                        print("Client name updated successfully")
                        break
                    print("Not enough info")
                elif sub_choice == "2":
                    new_password = input("\nEnter Client new password: ")
                    if len(new_password) > 3:
                        client.change_user_password(new_password)
                        print("Client password updated successfully")
                        break
                    print("Not strong enough")
                elif sub_choice == '3':
                    self.set_address()
                    break
                elif sub_choice == '4':
                    self.apply_coupon_to_client(client)
                elif sub_choice == '5':

                    break
                else:
                    print("\n * Invalid choice. Please try again. *\n")

        else:
             print("\n* Invalid ID *")

    def update_details(self):
        while True:
            choice = self.display.display_update_details()
            if choice == "1":
                new_name = input("\nEnter new full name: ")
                if len(new_name) > 3:
                    self.user.change_name(new_name)
                    print("\n Name changed successfully")
                    break
                print("\n * Not enough info *")
            elif choice == "2":
                new_password = input("\nEnter new password: ")
                if len(new_password) > 3:
                    self.user.change_user_password(new_password)
                    print("\n New password changed successfully")
                    break
                print("\n * Not enough info *")
            elif choice == '3':
                self.set_address()
                break
            elif choice == '4':
               self.choose_currency()
            elif choice == '5':
                print("\n * Exit")
                break
            else:
                print("\n * Invalid choice. Please try again. *\n")

    def apply_coupon_to_client(self, user):
        for i in range(3):
            amount = input("Enter coupon value: ")
            if amount.isdigit() and 0 < int(amount) < 100:
                user.update_coupon(int(amount))
                print("\n * Coupon has been successfully updated! *")
                break
            else:
                print("\n * Invalid coupon value. Please enter a number between 1 and 99 *")
            if i == 2:
                print("* You have exceeded the maximum number of attempts *")

    def apply_coupon(self):
        if self.user.coupon != 0:
            for each in range(5):
                choice_coupon = self.display.display_coupon(self.user)
                if choice_coupon == '1':
                    self.cart["total_amount"] *= (1 - (self.user.coupon / 100))
                    break
                elif choice_coupon == '2':
                    break
                else:
                    print("\n * Invalid choice. Try again. *")
                    print(f" * You have left {4 - each} tries. *\n")



    def remove_client(self):
        print("\n * Choose which client you want to remove *")
        client_lst = self.store.client_list()
        choice = input("\nChoose Client ID: ")
        if str(choice) in client_lst:
            self.store.remove_client(choice)
            print("\n * Client removed successfully *")
        else:
            print("\n * Invalid ID *")




    def remove_item_order(self):
            new_item = self.pick_item_order()
            if new_item is not None:
                print(f"{new_item.name} ============ {self.cart["product_dict"][new_item.get_key_name()]}")
                print("Update the quantity for the product or 0 to remove from your cart")
                how_much = input("\nEnter a quantity of the following product: ")
                if how_much.isdigit():
                    how_much = int(how_much)
                    quantity = self.cart["product_dict"][new_item.get_key_name()]
                    if how_much<quantity:
                        quantity -= how_much
                        if how_much == 0:
                            self.cart["product_dict"].pop(new_item.get_key_name())
                        else:
                            self.cart["product_dict"][new_item.get_key_name()] = how_much
                        self.cart["total_amount"]-=new_item.get_price(quantity)
                        self.cart["count_item"] -=quantity
                        print(f"\n * {new_item.name} ----- quantity {how_much} has been successfully updated ! ! *\n{self.cart["total_amount"]} ")

                    elif how_much>quantity:
                        quantity+=how_much
                        if self.store.add_item_order(new_item, quantity):
                            self.cart["total_amount"] += new_item.get_price(how_much)
                            self.cart["product_dict"][new_item.get_key_name()] = quantity
                            self.cart["count_item"] += how_much
                            print(f"\n * {new_item.name} ----- quantity {how_much} has been successfully updated ! ! *\n{self.cart["total_amount"]} ")


                    else:

                        print(f" * Sorry there is only {new_item.quantity} of {new_item.name} in  the inventory *")

                else:
                    print(f"\n * Error: Invalid quantity entered.Try Again * ")



    def pick_item_order(self):
        lst = self.store.lst_search(self.cart["product_dict"])
        choice = self.pick_item(lst)
        if choice != -100 and choice is not None:
            return lst[choice]
        else:
            return None

    def cart_check_out(self):
            while self.cart["count_item"] > 0:
                choice = self.display.cart_display(self.user, self.cart)
                if choice == '1':
                    self.check_out()
                elif choice == '2':
                    self.remove_item_order()
                elif choice == '3':
                    self.empty_cart()

                    break
                elif choice == '4':
                    print("Good bye ")
                    break

            print("Your Cart is empty.")

    def empty_cart(self):
         self.cart = {
                        'total_amount': 0,
                        'payment': None,
                        'product_dict': {},
                        "count_item": 0
        }


    def check_out(self):
        print("\n * Check Out  *\n")
        if self.user.address is None:
            self.set_address()
        if self.cart.get("total_amount") > 0 or len(self.cart.get("product_dict")) > 0:
            coupon = self.apply_coupon()
            payment = self.pay()
            if payment is not None:
                self.cart["payment"] = payment
                self.cart["customer"] = self.user
                self.store.place_order(self.cart)
                print(f" * The order was successfully completed * ")
                print(self.store.orders[self.store.order_number-1])
                self.empty_cart()
                if coupon == '1':
                    self.store.use_coupon(self.user)

    def catalog(self):
            while True:
                choice = self.display.display_order(self.cart)
                if choice == '1':
                    self.add_item()
                elif choice == '2':
                    if self.cart["count_item"] > 0:
                        self.cart_check_out()
                        break
                elif choice == '3':
                    break
                else:
                    print(" * Wrong choice,Try again *")

    def remove_product(self):
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

    def reporting(self):
        print(self.store.reporting)
        self.store.reporting.seen()

    def logout(self):
        #פונקציית התנתקות תבצע התנתקות למשתמש עצמו דרך הפונקציה במחלקה שלו ולאחר מכן תשמור בחנות את המשתמש החדש כדי לשמור את הנתונים החדשים שלו
        self.user.logout()
        self.store.users[self.user.user_id] = self.user
        logging.info("Logged out successfully\n")

    def wellcome_page(self):
            selection = self.display.display_user()
            if selection == '1':
                self.log_in()
            elif selection == '2':
                self.register()
            elif selection == '3':
                self.forgot_password()
            elif selection == '4':
                self.exit = True
                print('Bye, Thank you')
            else:
                print("\n * Login failed. Please check your credentials and try again. * \n ")

    def management_menu(self):
        choice = self.display_menu()
        if choice == '1':
            self.product_manager()
        elif choice == '2':
            self.user_manager()
        elif choice == '3':
            self.order_manager()
        elif choice == '4':
            self.list_products()
        elif choice == '5':
            self.reporting()
        elif choice == '6':
            self.user.logout()
        elif choice == '0':
            print("Bye, have a nice day")
            self.exit = True
        else:
            print("\n* Invalid choice. Please try again.* ")



    def customer_menu(self):
        sub_choice = self.display.display_client(self.user, self.cart, self.store)
        if sub_choice == '1':
            self.update_details()
        elif sub_choice == '2':
            self.cart_check_out()
        elif sub_choice == '3':
            self.catalog()
        elif sub_choice == '4':
            self.display_order_user()
        elif sub_choice == '5':
            self.logout()
        elif sub_choice == '6':
            self.logout()
            self.exit = True
            print("Bye, have a nice day")
        else:
            print("\n * Invalid choice. Please try again. * ")



    def run(self):
        self.store.load_files()
        while not self.exit:
            if self.user.online == 0:
                self.wellcome_page()
            elif self.user.online == 1:
                if type(self.user) == Client:

                        self.customer_menu()
                else:
                    self.management_menu()
        self.store.save_files()


if __name__ == "__main__":
    cli = StoreCLI()
    cli.run()