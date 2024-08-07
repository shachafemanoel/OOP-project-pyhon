import logging

from Store.cart import Cart
from Store.cart_command import CartInvoker,Command, ChangeCurrencyCommand, UseCouponCommand,AddItemCommand,ChangeItemQuantityCommand
from Store.client import Client
from Store.display import Display
from Store.payment import Payment
from Store.store import Store
from Store.storeerror import StoreError
from Store.user import User


class StoreCLI:
    def __init__(self):
        self.store = Store()
        self.user = Client("0000", "0000", "0000", online=0)
        self.cart = Cart()
        self.cart_invoker = CartInvoker()
        self.exit = False

    def log_in(self):
        # פונקציית התחברות למערכת הפונקציה מקבלת שם משתמש וסיסמא קוראת לפונקציה בחנות במידה והערכים תקינים יחזור משתמש אם המשתמש מנהל הפונקציה תחבר אותו בתור מנהל
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")
        try:
            loggg = self.store.log(user_id, password)
            self.user = loggg
            if type(self.user) == User:
                self.user.__class__ = User
            self.cart.currency = self.user.currency
        except StoreError.AuthenticationError as e:
            print(e)
            logging.warning(f"Login Failed\n")

    def register(self):
        print("\nWelcome to the registration systemֿ\n")
        print(" User id must be a at least 4 digit ")
        user_id = input("Enter user ID: ")
        user_full_name = input("Enter full name: ")
        print(" Password must be a at least 4 characters ")
        password = input("Enter password: ")
        user_type = "CLIENT"
        if self.user.online == 1 and not isinstance(self.user, Client):
            print("\n1.Client")
            print("2.Admin")
            choice = input("Enter your choice: ")
            if choice == "2":
                user_type = "ADMIN"
        user = {
            "user_id": user_id,
            "user_full_name": user_full_name,
            "password": password,
            "user_type": user_type
        }

        try:
            if self.user.online == 0:
                self.user = self.store.add_user(user)
            else:
                self.store.add_user(user)
            print("User registered successfully!")
        except StoreError as error:
            print(error)

    def set_password(self, user_id=None, user_full_name=None):
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

    def display_manage_user(self):
        if self.store.reporting.new_update["users"] > 0:
            for i in self.store.reporting.message["users"]:
                print(i)
        self.store.reporting.total_update -= self.store.reporting.new_update["users"]
        self.store.reporting.new_update["users"] = 0
        self.store.reporting.message["users"].clear()
        return Display.display_manage_user()

    def user_manager(self):
        while True:
            sub_choice = self.display_manage_user()
            if sub_choice == "1":
                client_list = self.store.client_list()
                print(client_list)
            elif sub_choice == '2':
                self.register()
                break
            elif sub_choice == "3":
                self.remove_client()
                break
            elif sub_choice == '4':
                self.change_password()
            elif sub_choice == '5':
                self.update_client_details()
            elif sub_choice == '6':
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
                    self.store.add_review(key, str(star), review)
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
        try:
            print(self.user.update_client())
            if len(self.user.order_history) > 0:
                while True:
                    choice = Display.orders_history(self.user.list_orders_client())
                    if choice == '1':
                        self.choice_order()
                    else:
                        print("\nReturning to Main menu")
                        break
        except Exception as e:
            print(f"\n * An error occurred while displaying your orders: {e} * \n")

    def set_address(self):
        print(" Add a new address \n * Please enter the details *\n")
        new_address = input("Country: ")
        city = input("City: ")
        street = input("Street: ")
        apt = input("Building,Apt,Floor: ")
        new_address += f",{city},{street},{apt}"
        new_address.replace(" ", "").translate(str.maketrans("", "", ".!?;:"))
        if len(new_address) > 3:
            if self.store.set_address(self.user.user_id, new_address):
                print("\n * Address has been set successfully *")
                print(f"\n * New Address updated: *\n {new_address}")
        else:
            print("\n * Not enough details were entered for setting address. *")

    def new_card(self, paymethod):
        card_holder = input("Name on card: ")
        card_number = input("Card number: ")
        how_much = input("how many payments would you like to spread the deal?: ")
        try:
            how_much = int(how_much)
            if Payment.check_card(card_number, how_much):
                paymethod["owner"] = card_holder
                paymethod["info"] = card_number
                paymethod["amount_of_payments"] = how_much
                print("Credit card verified")
                print("\nWould you like to save your payment method for future orders?")
                print("\n1. Yes, save it")
                print("\n2. No ")
                save = input("Enter your choice: ")
                if save == '1':
                    self.user.payment = paymethod
                return paymethod
        except StoreError.InvalidCardNumberError as e:
            print(e)
        except StoreError.InvalidPaymentsNumberError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def new_paypal(self, paymethod):
        paypal_id = input("Enter your Paypal id: ")
        if len(paypal_id) > 8:
            paymethod["owner"] = self.user.user_full_name
            paymethod["info"] = paypal_id
            paymethod["payment_method"] = "Paypal"
            paymethod["amount_of_payments"] = 1
            print("\nWould you like to save your payment method for future orders?")
            print("\n1. Yes,save it")
            print("2 .No ")
            save = input("Enter your choice: ")
            if save == '1':
                self.user.payment = paymethod
            return paymethod
        else:
            print("\n * Paypal id in invalid * ")

    def new_payment(self):
        paymethod = {"owner": "", "info": "", "payment_method": ""}
        for i in range(4):
            pay_option = Display.display_payment()
            if pay_option == '1':
                return self.new_card(paymethod)
            elif pay_option == '2':
                return self.new_paypal(paymethod)
            elif pay_option == '3':
                paymethod = {"owner": self.user.user_full_name, "info": "", "payment_method": 'Cash'}
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
            for i in range(4):
                print(f"Wrong choice. Please try again.You have {4 - i} attempts left")
                choice = input("Enter your choice: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
                if choice in currencies:
                    self.set_currency(currencies[choice])

                elif i == 4:
                    print("You have passed the number of attempts.\nThe currency is set to be ILS")

        print(f"Your currency is:{currencies[choice]}")

    def set_currency(self, currency):
        try:
            self.user.currency = currency
            command = ChangeCurrencyCommand(self.cart, currency)
            self.cart_invoker.add_command(command)
            self.store.change_currency(currency)
        except Exception as e:
            print(f"An error occurred while setting currency: {e}")

    def change_status(self):
        print(f"{self.store.list_orders()}")
        number = input("\nPlease Enter the order number: ")
        if number.isdigit():
            number = int(number)
            if number in self.store.orders:
                print(f"{self.store.orders[number]}")
                print("\n1. New status - Shipped")
                print("2. New status - Delivered")
                print("3. New status - Canceled")
                choice = input("Enter your choice: ")
                if choice == '1' or choice == '2' or choice == '3':
                    self.store.change_order(number, int(choice))
                    print(
                        f"\n* Order number:{self.store.orders[number].order_number} New status: {self.store.orders[number].status} *\n")
                    if choice == '3':
                        self.store.cancel_order(number)
                else:
                    print("\n * Invalid choice.The status has not changed * \n")
            else:
                print("\n * Order do not exist. Please try again. *")
        else:
            print("\n * Invalid order number")

    def product_type(self, choice=None):
        if choice is None:
            choice = Display.display_product_type()
        for each in range(5):
            if choice in '1234':
                return self.store.search(None, choice, None)
            elif choice == "0":
                return None
            else:
                choice = Display.display_product_type()
                print("Try Again")
        return None

    def discount(self):
        try:
            discount = input("Enter amount of % for discount: ")
            discount = int(discount)
            return discount
        except ValueError:
            raise StoreError.InvalidInputError("Discount amount must be an integer")

    def choice_discount(self):
        choice = Display.display_discount()
        if choice == '1':
            self.add_discount()
        if choice == '2':
            self.add_promotion()

    def add_discount(self):
        choice = Display.display_product_type()
        try:
            discount = self.discount()
            category = self.store.sale_prodduct_type(choice, discount)
            print(f"\n* Discount has been successfully updated")
            self.store.apply_discount_to_category(category, discount)
        except StoreError.InvalidInputError as e:
            print(f"An error occurred while adding discount: {e}")

    def add_promotion(self):
        product = self.search_system()
        if product is not None and product != -100:
            discount = self.discount()
            try:
                self.store.new_promotion(product, discount)
            except Exception as e:
                print(f"An error occurred while adding promotion: {e}")

    def remove_discount(self):
        choice = Display.display_discount()
        if choice == "1":
            select = Display.display_product_type()
            try:
                category = self.store.remove_product_sale(select)
                self.store.remove_discount_to_category(category)
                print("\n* Discount has been successfully removed *")
            except StoreError.InvalidInputError as e:
                print(f"An error occurred: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        elif choice == "2":
            product_name = self.search_system()
            if product_name is not None and product_name != -100:
                try:
                    self.store.remove_promotion(product_name)
                    print("\n* Discount successfully removed *")
                except Exception as e:
                    print(f"An error occurred while removing discount: {e}")
        else:
            print("Invalid choice. Please select a valid option.")

    def display_manage_order(self):
        print("\n * Wellcome to manage order display *\n")
        if self.store.reporting.new_update["orders"] > 0:
            for i in self.store.reporting.message["orders"]:
                print(f"{i}")
        self.store.reporting.total_update -= self.store.reporting.new_update["orders"]
        self.store.reporting.new_update["orders"] = 0
        self.store.reporting.message["orders"].clear()
        return Display.display_manage_order()

    def order_manager(self):
        while True:
            choice = self.display_manage_order()
            if choice == "1":
                self.change_status()
            elif choice == "2":
                self.orders()
            elif choice == "3":
                break
            else:
                print("\n * Invalid choice. Please try again. *\n")

    def pick_item(self, lst):
        """
        The function receives a list of products from the search in the system and displays the results to the customer to allow him to choose a product
        and returns the position of the product in the list
        if no product is selected or there are no results the function returns -100
            """
        if len(lst) == 0:
            return -100
        print("\nPlease select one of the options")
        for i in range(len(lst)):
            print(f" {lst[i]} \n  \n * for {lst[i].name} Press =>  {i + 1} ", )
            print("======================================")
        print("Choose one of the options \n\n For exit, enter a different value from the options ")
        select = input("Enter your choice: ")
        if select.isdigit():
            select = int(select)
            if select > 0 and select <= len(lst):
                select -= 1
                if len(lst) > select >= -1:
                    return select
            else:
                return -100
        else:
            return -100

    def model_search(self):
        try:
            model = input("Enter model: ")
            search_name_model = self.store.search(None, None, model)
            choice = self.pick_item(search_name_model)
            if choice != -100 and choice is not None:
                return search_name_model[choice]
            else:
                return None
        except StoreError.ProductNotFoundError as e:
            print(e)
    def name_search(self):
        try:
            new_name = input("\nEnter Product name: ")
            search_name = self.store.search(new_name)
            choice = self.pick_item(search_name)
            if choice != -100 and choice is not None:
                return search_name[choice]
            else:
                    return None
        except StoreError.ProductNotFoundError as e:
            print(e)
    def display_manage_product(self):
        print("\n * Wellcome to manage product display *\n")
        if self.store.reporting.new_update["products"] > 0:
            for i in self.store.reporting.message["products"]:
                print(f"{i}")
        self.store.reporting.total_update -= self.store.reporting.new_update["products"]
        self.store.reporting.new_update["products"] = 0
        self.store.reporting.message["products"].clear()
        return Display.display_manage_product()

    def product_manager(self):
        while True:
            sub_choice = self.display_manage_product()
            if sub_choice == '1':
                self.add_product()
            elif sub_choice == '2':
                self.remove_product()
            elif sub_choice == '3':
                self.choice_discount()
            elif sub_choice == '4':
                self.remove_discount()
            elif sub_choice == '5':
                product_list = self.store.list_products()
                print(product_list)
            elif sub_choice == '6':
                break
            else:
                print("\n * Invalid choice. Please try again. *\n")

    def search_system(self):
        while True:
            print("\n * Welcome to the catalog Menu * \n ")
            new_item = self.catalog_menu()
            if new_item == False:
                break
            elif new_item  is not None:
                while True:
                    choice = Display.pick_item_menu(new_item)
                    if choice == "1":
                        self.add_item_to_cart(new_item)
                        break
                    elif choice == "2":
                        print(new_item.rate)
                    elif choice == "0":
                        break
                    else:
                        print("\n * Invalid choice. Please try again. *\n")




    def view_categories(self):
        type_search = self.product_type()
        if type_search is not None:
            choice = self.pick_item(type_search)
            if choice != -100 and choice is not None:
                return type_search[choice]
            else:
                print("\n * No Product selected * \n")
                return None


    def catalog_menu(self):
            select = Display.catalog_main_menu(self.store.sales)
            if select == "1":
                new_item =self.view_categories()
                if new_item is not None:
                    return new_item
            if select == "2":
                new_item = self.name_search()
                if new_item is not None:
                    return new_item
            elif select == "3":
                new_item = self.model_search()
                if new_item is not None:
                    return new_item
            elif select == "4":
                new_item = self.search_by_price()
                if new_item is not None:
                    return new_item
            elif select == "5":
                new_item = self.search_by_rating()
                if new_item is not None:
                    return new_item
            elif select == "0":
                return False
            else:
                print("\n * Invalid choice. Please try again. *\n")



    def search_by_price(self):
        try:
            print("\n * Welcome to search by price *\n")
            print(f"Your currency :{self.user.currency} ")
            low = input("Enter low price: ")
            high = input("Enter high price: ")
            products = self.store.price_search(low, high, self.user.currency)
            choice = self.pick_item(products)
            if choice != -100 and choice is not None:
                return products[choice]
            else:
                print("\nNo product selected.")
        except StoreError.InvalidInputError as e:
            print(e.message)
        except StoreError.ProductNotFoundError as e:
            print(e.message)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def search_by_rating(self):
        try:
            low = input("\nEnter low rating: ")
            high = input("\nEnter high rating: ")
            products = self.store.rate_search(low, high)
            choice = self.pick_item(products)
            if choice != -100:
                return products[choice]

            else:
                print("\nNo product selected.")
        except StoreError.InvalidInputError as e:
            print(e.message)
        except StoreError.ProductNotFoundError as e:
            print(e.message)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def add_item_to_cart(self,new_item):
        """
        Add an item to the cart via CLI.
        """
        if new_item is not None:
            try:
                    quantity = input("\nEnter a quantity of the product: ")
                    quantity = int(quantity)
                    if new_item.available(quantity):
                        command = AddItemCommand(self.cart, new_item, quantity)
                        self.cart_invoker.add_command(command)
                        print(f"\n * {new_item.name} =========== > quantity {quantity} has been successfully added to cart! *\n")
                    else:
                        print(f"\n ** We apologize, but the quantity you requested exceeds the available stock ** .\nCurrently, we have only {new_item.quantity} units available. ")

            except ValueError as e:
                    print(e)
            except StoreError.NotInStockError as e:
                    print(e)

    def add_product(self):

        product_type = Display.display_product_type()
        if product_type in '1234':
            name = input("Enter Product Name: ")
            model = input("Enter Product Model: ")
            try:
                search = self.store.search(name, model)
                self.check_if_exist(search)
                print(" \n * This products exists in the system please choose product for adding amount. * ")
            except StoreError.ProductNotFoundError as e:
                    description = input("Enter description: ")
                    try:
                        price = float(input("Enter Price: ").strip())
                    except ValueError:
                        print("\nInvalid input for price. Please enter a valid number.")
                        return
                    try:
                        quantity = int(input("Enter Quantity: ").strip())
                    except ValueError:
                        print("\nInvalid input for quantity. Please enter a valid number.")
                        return

                    kwargs = {}
                    if product_type == "2":  # Computer
                        kwargs["size"] = input("Enter Screen size: ")
                        kwargs["storage"] = input("Enter storage: ")
                        kwargs["chip"] = input("Enter Chip: ")
                    elif product_type == "1":  # Tv
                        kwargs["size"] = input("Enter Screen size: ")
                        kwargs["tv_type"] = input("Enter Resolution: ")
                    elif product_type == "3":  # Phone
                        kwargs["size"] = input("Enter Screen size: ")
                        kwargs["storage"] = input("Enter Storage: ")

                    product_dict = {
                        "product_type": self.map_product_type(product_type),
                        "name": name,
                        "model": model,
                        "description": description,
                        "price": price,
                        "quantity": quantity,
                        **kwargs
                    }
                    try:
                        self.store.add_product(product_dict)
                        print("\n* Product has been successfully added *")
                    except ValueError as e:
                        print(e)


    def map_product_type(self, choice):
        try:
            if choice == "1":
                return "Tv"
            elif choice == "2":
                return "Computer"
            elif choice == "3":
                return "Phone"
            elif choice == "4":
                return "Product"
        except:
            raise ValueError("Invalid product type selected")

    def check_if_exist(self, search):
        s = self.pick_item(search)
        if s != -100:
            pro = search[s]
            print(f"\n{pro}")
            print("\nHow much would you like to add to the inventory?")
            quantity = input("\nAdd quantity: ")
            if quantity.isdigit():
                self.store.collection[pro.get_key_name()].add_quantity(int(quantity))
                print("\n * Quantity added successfully *")
            else:
                print("\nQuantity must be a digit!")

    def update_client_details(self):
        client_lst = self.store.client_list()
        print(client_lst)
        choice = input("\nChoose Client ID: ")
        if choice in self.store.users:
            client = self.store.users.get(choice)
            while True:
                sub_choice = Display.display_client_details()
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
                    self.apply_coupon_to_client(client.user_id)
                elif sub_choice == '5':

                    break
                else:
                    print("\n * Invalid choice. Please try again. *\n")

        else:
            print("\n* Invalid ID *")

    def update_details(self):
        while True:
            choice = Display.display_update_details()
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

    def apply_coupon_to_client(self, user_id):
        for i in range(3):
            amount = input("Enter coupon value: ")
            try:
                if amount.isdigit():
                    self.store.sales.add_coupon(user_id, int(amount))
                    print("\n * Coupon has been successfully updated! *")
                    break
                else:
                    raise ValueError("Coupon value must be a number between 0 and 99")
            except ValueError as e:
                print(f"\n * {e}.\nPlease enter a valid number between 0 and 99. *")
            except StoreError.InvalidInputError as e:
                print(f"\n * {e}.\nPlease enter a valid number between 0 and 99. *")

            if i == 2:
                print("* You have exceeded the maximum number of attempts *")

    def apply_coupon(self):
        if self.store.sales.get_coupon_discount(self.user.user_id) != 0:
            for each in range(5):
                choice_coupon = Display.display_coupon(self.store.sales.get_coupon_discount(self.user.user_id))
                if choice_coupon == '1':
                    coupon_value = self.store.sales.get_coupon_discount(self.user.user_id)
                    command = UseCouponCommand(self.cart, coupon_value)
                    self.cart_invoker.add_command(command)
                    return True
                elif choice_coupon == '2':
                    return False
                else:
                    print("\n * Invalid choice. Try again. *")
                    print(f" * You have left {4 - each} tries. *\n")
        return False

    def remove_client(self):
        client_lst = self.store.client_list()
        print(client_lst)
        print("\n * Choose which client you want to remove *")
        choice = input("\nChoose Client ID: ")
        if choice in self.store.users.keys():
            self.store.remove_client(choice)
            print("\n * Client removed successfully *")
        else:
            print("\n * Invalid ID *")

    def update_cart(self):
        """
        Update the quantity of an item in the cart via CLI.
        """
        while True:
            new_item = self.pick_item_order()
            if new_item is not None:
                print(
                    f"\n * {new_item.name} =============== quantity {self.cart.get_product_quantatiy(new_item.get_key_name())}  *\n")
                print("\nPlease enter the desired quantity of the product. To remove it from the cart, enter 0.")
                quantity = input("\nEnter a quantity: ")
                try:
                    quantity = int(quantity)
                    if new_item.available(quantity):
                        command = ChangeItemQuantityCommand(self.cart, new_item, quantity)
                        self.cart_invoker.add_command(command)
                        print(f"\n * {new_item.name} ===============> new quantity {quantity}  *\n")
                        if quantity == 0:
                            print(f"{new_item.name} will be removed from the cart when you save the changes")
                    else:
                        print("\n *** Error:The quantity was not changed in the cart")
                        print(f"\n ** We apologize, but the quantity you requested exceeds the available stock ** .\nCurrently, we have only {new_item.quantity} units available. ")
                except ValueError as e:
                    print(f"\n * {e}.\n")
                except StoreError.NotInStockError as e:
                    print(f"\n * {e}.\n")
                except StoreError as e:
                    print(e)
            else:
                print("\n * No item selected. *")


            while True:
                choice = Display.save_changes_menu()
                if choice == "1":
                    break
                elif choice == "2":
                    self.cart_invoker.execute_commands()
                    print("Changes saved.")
                    self.cart_invoker.reset_commands()
                    return
                elif choice == "3":
                    self.cart_invoker.undo_commands()
                    break
                elif choice == '4':
                    self.cart_invoker.reset_commands()
                    print("Changes not saved.")
                    return
                else:
                    print("\n * Invalid choice. Please try again. *")




    def pick_item_order(self):
        lst = self.store.lst_search(self.cart.product_dict)
        choice = self.pick_item(lst)
        if choice != -100 and choice is not None:
            return lst[choice]
        else:
            return None

    def cart_check_out(self):
        if self.cart.count_item > 0:
            while self.cart.count_item > 0:
                choice = Display.cart_display(self.cart)
                if choice == '1':
                    self.check_out()
                elif choice == '2':
                    self.update_cart()
                elif choice == '3':
                    self.empty_cart()

                    break
                elif choice == '4':
                    print("Good bye ")
                    break
        else:
            print("Your Cart is empty.")

    def empty_cart(self):
        self.cart.clear_cart()
        self.cart_invoker.reset_commands()
        print("\n * Cart has been cleared! *\n")

    def check_out(self):
        print("\n * Check Out  *\n")
        self.cart_invoker.execute_commands()
        if self.user.address is None:
            self.set_address()
        if self.cart.total_amount > 0 or len(self.cart.product_dict) > 0:
            coupon = self.apply_coupon()
            payment = self.pay()
            if payment is not None:
                new_order = self.cart.get_cart_dict()
                new_order["payment"] = payment
                new_order["customer"] = self.user
                new_order["address"] = self.user.address
                self.store.place_order(new_order)
                print(f" * The order was successfully completed * ")
                print(self.store.orders[self.store.order_number - 1])
                self.empty_cart()
                if coupon is True:
                    self.store.sales.use_coupon_discount(self.user.user_id)


    def remove_product(self):
        removed_product = self.search_system()
        try:
            self.store.remove(removed_product)
            print(f"\n {removed_product}\n has been removed ")

        except Exception as e:
            print(f"\n {e}")

    def list_products(self):
        if len(self.store.collection) > 0:
            print(f"{self.store.list_products()}")
        else:
            print(" No products in inventory yet!")

    def orders(self):
        if len(self.store.orders) > 0:
            print(self.store.list_orders())
        else:
            print(' No orders placed yet ')

    def reporting(self):
        print(self.store.reporting)

    def logout(self):
        # פונקציית התנתקות תבצע התנתקות למשתמש עצמו דרך הפונקציה במחלקה שלו ולאחר מכן תשמור בחנות את המשתמש החדש כדי לשמור את הנתונים החדשים שלו
        self.user.logout()
        self.store.users[self.user.user_id] = self.user
        logging.info("Logged out successfully\n")

    def wellcome_page(self):
        selection = Display.display_user()
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
            print("\n * Invalid choice,Try again * \n ")

    def display_menu(self):
        print(self.store.reporting.nofiction())
        print(" \n=== Control System ==")
        print("=====================")
        print("1. Product Manager")
        print("2. User Manager")
        print("3. Order Manager")
        print("4. Reporting")
        print("5. Logout")
        print("0. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def management_menu(self):
        choice = self.display_menu()
        if choice == '1':
            self.product_manager()
        elif choice == '2':
            self.user_manager()
        elif choice == '3':
            self.order_manager()
        elif choice == '4':
            self.reporting()
        elif choice == '5':
            self.user.logout()
        elif choice == '0':
            print("Bye, have a nice day")
            self.exit = True
        else:
            print("\n* Invalid choice. Please try again.* ")

    def customer_menu(self):
        self.cart_invoker.execute_commands()
        self.cart_invoker.reset_commands()
        sub_choice = Display.display_client(self.user.new_message, self.cart, self.store.sales)
        if sub_choice == '1':
            self.update_details()
        elif sub_choice == '2':
            self.cart_check_out()
        elif sub_choice == '3':
            self.search_system()
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
        print(" \n * Welcome to Electronic Store  *  ")
        while not self.exit:
            print(self.store.sales)
            if self.user.online == 0:
                self.wellcome_page()
            elif self.user.online == 1:
                print(f"\n Welcome Back ,{self.user.user_full_name.title()} ",end="  ")
                if type(self.user) == Client:
                    self.customer_menu()
                else:
                    self.management_menu()
        self.store.save_files()


if __name__ == "__main__":
    cli = StoreCLI()
    cli.run()
