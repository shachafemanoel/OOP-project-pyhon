
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
from Store.rating import Rating

class StoreCLI:
    def __init__(self):
        self.store = Store()
        self.user = Client()
        self.count_item = 0
        self.cart = Order()
        self.exit = False

    def log_in(self):
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")
        loggg = self.store.log(user_id, password)
        if loggg is not None:
            self.cart = Order()
            self.count_item = 0
            self.user = loggg
            if type(self.user) == User:
                self.user.__class__ = User
                print("Login successful!")

    def register(self):
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
                    new_user = Client(user_id, full_name, pass_word)
                    if self.store.add_user(new_user):
                        self.user = new_user
                        self.set_address()
                        self.store.users[user_id] = new_user
                        self.user.online = 1
                        print("\n * User registered successfully. * ")
                        self.user.coupon = 5
                        print("Thank you for register. Enjoy a 5% coupon !")

                    else:
                        print("\n * User already exists please try to log in *")
                else:
                    print("\n The password must contain at least 4 characters. Please try again ")
            else:
                print("\n * Invalid full name. Try again * ")
        else:
            print("\n * User ID must be at least 4 digit.Try again * ")


    def register_admin(self, new_admin=None):
        print("\nAdding new admin\n")
        print(" User ID must be at least 4 digits ")
        user_id = input("Enter User ID: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

        if user_id.isdigit() and len(user_id) > 3:
            print("\n Full name must be at least 4 characters ")
            full_name = input("Enter the admin's full name: ")

            if len(full_name) > 3:
                print("\n The password must contain at least 4 characters ")
                password = input("Enter the admin's password: ")

                if len(password) > 3:
                    new_admin = User(user_id, full_name, password)
                    new_admin.online = 1
                    self.store.users[user_id] = new_admin
                    print("\n * Admin registered successfully. * ")
                    return new_admin
                else:
                    print("\n The password must contain at least 4 characters. Please try again ")
            else:
                print("\n * Invalid full name. Try again * ")
        else:
            print("\n * User ID must be at least 4 digits. Try again * ")

        return new_admin

    def add_admin(self):
        new_admin = self.register_admin()
        return new_admin

    def change_password(self):
        old_password = input("\nFor changing password please enter your old password: ")

        if self.user.password == old_password:
            print("\n * The password must contain at least 4 characters *")
            new_user_password = input("Enter your new password: ")

            if len(new_user_password) > 3:
                self.user.change_user_password(new_user_password)
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
                    self.user = user
                    print("\n * Password changed successfully, you can now log in *")
                else:
                    print("\n *The password must contain at least 4 characters. Please try again.* ")
            else:
                print("\n * Full name or ID is incorrect. Please try again. *")
        else:
            print("Error,user id not found ")

    def display_manage_user(self):
        print("\n * Wellcome to manage users display *\n")
        print("1. Add user")
        print("2. Add admin")
        print("3. Change password")
        print("4. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def user_manager(self):
        while True:
            sub_choice = self.display_manage_user()
            if sub_choice == '1':
                self.register()
                break
            elif sub_choice == '2':
                self.register_admin()
                break
            elif sub_choice == '3':
                self.change_password()
            elif sub_choice == '4':
                break
            else:
                print("\n * Invalid choice. Please try again. *\n")
                sub_choice = self.display_manage_product()

    def display_user(self):
        print("\n Welcome to Electronic Store Management System!\n ")
        print("1. Existing User? Log in")
        print("2. New User? Sign up now ")
        print("3. Forgot password? Reset here")
        print("4. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))


    def add_review(self, order):
        for key, value in order.product_dict.items():
            print(key)
            prod = self.store.collection[key]
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
                    new = Rating(star, review)
                    prod.add_review(new)
                    self.store.collection[key] = prod
                else:
                    print("Wrong choice")
            else:
                print("Wrong choice")

    def choice_order(self):
        order_number = input("Enter order number: ")
        if order_number.isdigit():
            order_number = int(order_number)
            if 0 < order_number < self.store.order_number + 1:
                order = self.user.order_history[order_number]
                print(order)
                if order.status == 'delivered':
                    print("Are you interested in giving a review on the order?\n1. Yes!")
                    option = input("Enter your choice: ")
                    if option == '1':
                        self.add_review(order)

    def display_order_user(self):
        if len(self.user.order_history)>0 :
            while True:
                choice =self.orders_history()
                if choice == '1' :
                  self.choice_order()
                else:
                    print("Return to Main menu")
                    break


    def display_client(self):
        if self.user.new_messege > 0:
            print(f"\n * There are {self.user.new_messege} new notifications on orders * \n")
        print("\n1. Change address")
        if self.count_item > 0:
            print(f"2. Cart({self.count_item})")
        else:
            print("2. Cart(0)")
        if len(self.store.sales) > 0:
            print("3.   Collection * new sale *")
        else:
            print("3. Collection")
        if self.user.new_messege > 0:
            print(f"4. Orders * {self.user.new_messege} notifications * ")
        else:
            print("4. Orders")
        print("5. Change password")
        print("6. Logout")
        print("7. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def display_coupon(self):
        print(f"\nWould you like to use your {self.user.coupon}% coupon?")
        print('\n1. Yes')
        print('2. No')
        choice = input('\nEnter your choice: ')
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def set_address(self):
        print("\n * Please enter the details *\n")
        new_address = input("Country: ")
        city = input("City: ")
        street = input("Street: ")
        apt = input("Building,Apt,Floor: ")
        new_address += f",{city},{street},{apt}"
        new_address.replace(" ", "").translate(str.maketrans("", "", ".!?;:"))
        if len(new_address) > 3:
            self.user.change_address(new_address)
            print("\n * Address has been set successfully *")
            print(f"\n * New Address updated: *\n {new_address}")
        else:
            self.user.address = None
            print("\n * Not enough details were entered for setting address. *")


    def display_order(self):
        print("\n1. Add Item ")
        if self.count_item > 0:
            print(f"2.Cart({self.count_item})")
        print("3. Exit ")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))


    def display_payment(self):
        print(self.cart.converter())
        print(self.cart.payments())
        print("How would you like to pay?")
        print("\n1.Credit Card")
        print("2.Paypal")
        print("3.Cash")
        print("4.Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def pay(self):
        paymethood = Payment()
        if self.user.payment is not None:
            self.user.payment.amount_of_payments =1
            print(f"\n===================\nfor paying with:\n")
            print(self.user.payment)
            s = input("Press 1:")
            if s == '1':
                how_much = input("how many payments would you like to spread the deal?")
                if how_much.isdigit():
                    self.user.payment.amount_of_payments = int(how_much)
                return self.user.payment
        else:

            for i in range(4):
                pay_option = self.display_payment()
                if pay_option == '1':
                    card_holder = input("Name on card: ")
                    card_number = input("Card number: ")
                    how_much = input("how many payments would you like to spread the deal?")
                    if card_number.isdigit() and how_much.isdigit():
                        paymethood = Payment(card_holder, card_number,"Credit Card")
                    if paymethood.check_card(how_much):

                        print("\nWould you like to save your payment method for future orders?")
                        print("\n1. Yes, save it")
                        print("\n2. No ")
                        save = input("Enter your choice: ")
                        if save == '1':
                            self.user.payment = paymethood
                        return paymethood
                    else:
                        print("\n * The card number is invalid * ")

                elif pay_option == '2':
                    paypal_id = input("Enter your Paypal id: ")
                    if len(paypal_id) > 0:
                        paymethood = Payment(self.user.user_full_name, None, 'PayPal')
                        print("\nWould you like to save your payment method for future orders?")
                        print("1. Yes,save it")
                        print("2 .No ")
                        save = input("Enter your choice: ")
                        if save == '1':
                            self.user.payment = paymethood
                        return paymethood
                    else:
                        print("\n * Paypal id in invalid * ")

                elif pay_option == '3':
                    paymethood = Payment(self.user.user_full_name, None, 'Cash')
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
                self.store.change_order(number, int(choice))
                print(f"\n* Order number:{self.store.orders[number].order_number} New status:{self.store.orders[number].status} *\n")
            else:
                print("\n * Invalid choice.The status has not changed * \n")
        else:
            print("\n * Wrong order number *\n")

    def display_product_type(self):
        print("\n * Select Product type *")
        print('\n1. TV')
        print('2. Computer')
        print('3. Mobile Phone')
        print('4. Accessories')
        print('5. All')
        print("0. Exit Or Manual Search")
        choice = input("\nEnter Your Choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def product_type(self, choice=None):
        if choice is None:
            choice = self.display_product_type()

        for i in range(5):
            if choice in '1234':
                return self.store.search(None, choice, None)
            elif choice == "5":
                return self.list_products()
            elif choice == "0":
                    return None

            else:
                print("Try Again")
                choice = self.display_product_type()
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
        choice = self.display_product_type()
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

    def display_remove_discount(self):
        print("\nChoose an option:")
        print("\n1. Remove discount from a category")
        print("2. Remove discount from a specific product")
        choice = input("\nEnter your choice: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        return choice

    def remove_discount(self):
        choice = self.display_remove_discount()

        if choice == "1":
            category = self.display_product_type()
            self.store.remove_discount(category)
        elif choice == "2":
            product_name = self.manual_search()
            if product_name is not None and product_name != -100:
                self.store.remove_discount(product_name)
            else:
                print("\nProduct not found.")
        else:
            print("Invalid choice.")


    def display_manage_product(self):
        print("\n * Wellcome to manage product display *\n")
        print("1. Add Product or Adding a quantity to an existing product ")
        print("2. Remove Product")
        print("3. Add Discount")
        print("4. Remove Discount")
        print("5. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def display_menu(self):
        if self.store.reporting.new_update > 0:
            print(f"\n * There are {self.store.reporting.new_update} new notifications Reporting *")
        print(" \n *  Electronic store Management System * \n")
        print("1. Product Manager")
        print("2. User Manager")
        print("3. Update order status")
        print("4. List Product")
        print("5. List Orders")
        if self.store.reporting.new_update > 0:
            print(f"6. Reporting * {self.store.reporting.new_update} notifications *")
        else:
            print("6. Reporting")
        print("7. Logout")
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
            item = Product()
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
            sub_choice = self.display_manage_product()
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
        new_item = Product()
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
        self.cart.customer = self.user
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
                        print(f" * Sorry there is only {self.store.collection[new_item.get_key_name()].quantity} of {new_item.name} in  the inventory *")
                    else:
                        self.cart.add_item_to_order(new_item,how_much)
                        self.count_item += how_much
                        print(f"\n * {new_item.name} ----- quantity {how_much} total:{new_item.price*how_much} has been successfully updated ! *\n{self.cart.converter()} ")
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
        amount = input("\nEnter a quantity: ")
        if amount.isdigit():
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
        if len(search) > 0:
            print(f" \n * This products exists in the system please choose product for adding amount. * ")
            s = self.pick_item(search)
            if s != -100:
                pro = search[s]
                print(f"\n{pro}")
                print("How much would you like to add to the inventory?")
                quan = input("Add quantity: ")
                if quan.isdigit():
                    self.store.collection[pro.get_key_name()].add_quantity(int(quan))
                    print("\n * Quantity added successfully *")
                else:
                    print("Quantity must be a digit!")

            else:

                description = input("Enter description: ")
                price = input("Enter Price: ")
                quantity = input("Enter Quantity: ")
                category = self.display_product_type()
                if price.isdigit() and int(price) > 0 and quantity.isdigit():
                    price = float(price)
                    quantity = int(quantity)
                    if category == 1:
                        size = input("Enter Screen size: ")
                        tv_type = input("Enter TV type")
                        pro = Tv(name,model, description, price, quantity, size, tv_type)
                    if category == 2:
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

    def apply_coupon(self):
        if self.user.coupon is not None:
            for each in range(5):
                choice_coupon = self.display_coupon()
                if choice_coupon == '1':
                    self.cart.total_amount = self.cart.total_amount * (1 - (self.user.coupon / 100))
                    break
                elif choice_coupon == '2':
                    break
                else:
                    print("\n * Invalid choice. Try again. *")
                    print(f" * You have left {4 - each} tries. *\n")

            return choice_coupon

    def remove_item_order(self):
            new_item = self.pick_item_order()
            if new_item is not None:
                print(f"{new_item.name}============{new_item.quantity}")
                print("Update the quantity for the product or 0 to remove from your cart")
                how_much = input("\nEnter a quantity of the following product: ")
                if how_much.isdigit():
                    how_much = int(how_much)
                    if how_much == 0:
                        print("* The item has been removed from your cart *")
                        self.cart.remove(new_item, 0)
                        self.count_item -= 1

                    if not self.store.add_item_order(new_item, how_much):
                        print(f" * Sorry there is only {new_item.quantity} of {new_item.name} in  the inventory *")

                    else:
                        self.cart.add_item_to_order(new_item, how_much)
                        print(f"\n * {new_item.name} ----- quantity {how_much} has been successfully updated ! ! *\n{self.cart.converter()} ")

                else:
                    print(f"\n * Error: Invalid quantity entered.Try Again * ")

            if self.cart.total_amount < 0:
                self.cart = Order()


    def pick_item_order(self):
        lst = self.store.lst_search(self.cart)
        choice = self.pick_item(lst)
        if choice != -100 and choice is not None:
            return lst[choice]
        else:
            return None


    def cart_display(self):
        print("\n * Shopping Cart *\n")
        print(self.cart)
        print("1. Proceed to checkout ")
        print("2. Change")
        print("3. Empty the cart")
        print("4. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def cart_check_out(self):
            while self.count_item > 0:
                choice = self.cart_display()
                if choice == '1':
                    self.check_out()
                elif choice == '2':
                    self.remove_item_order()
                elif choice == '3':
                    self.cart = Order(self.user, None, None, None)
                    self.count_item = 0
                    break
                elif choice == '4':
                    print("Good bye ")
                    break

            print("Your Cart is empty.")


    def check_out(self):
        if self.user.address is None:
            User.set_address()
        if self.cart.total_amount > 0 or len(self.cart.product_dict) > 0:
            coupon = self.apply_coupon()
            payment = self.pay()
            if payment:
                order = self.cart
                order.pay_order(payment)
                self.store.place_order(order)
                self.user.new_order(order)
                print(f" {order}\n {payment}\n * The order was successfully completed * ")
                self.cart = Order()
                self.count_item = 0

                if coupon == 1:
                    self.user.use_coupon()

    def catalog(self):
            while True:
                choice = self.display_order()
                if choice == '1':
                    self.add_item()
                elif choice == '2':
                    if self.count_item > 0:
                        self.cart_check_out()
                        break
                elif choice == '3':
                    break
                else:
                    print(" * Wrong choice,Try again *")

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

    def orders_history(self):
        print(self.user.update_client())
        print("\n * Your orders *\n")
        print(self.user.list_orders_client())
        print("1.View order details")
        print("2.Exit")
        choice = input("Enter your choice: ")
        return choice

    def reporting(self):
        print(self.store.reporting)
        self.store.reporting.seen()

    def logout(self):
        self.user.logout()
        self.store.users[self.user.user_id] = self.user

    def wellcome_page(self):
            selection = self.display_user()
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
            self.change_status()
        elif choice == '4':
            self.list_products()
        elif choice == '5':
            self.orders()
        elif choice == '6':
            self.reporting()
        elif choice == '7':
            self.user.logout()
        elif choice == '0':
            print("Bye, have a nice day")
            self.exit = True
        else:
            print("\n* Invalid choice. Please try again.* ")



    def customer_menu(self):
        sub_choice = self.display_client()
        if sub_choice == '1':
            self.set_address()
        elif sub_choice == '2':
            self.cart_check_out()
        elif sub_choice == '3':
            self.catalog()
        elif sub_choice == '4':
            self.display_order_user()
        elif sub_choice == '5':
            self.change_password()
        elif sub_choice == '6':
            self.logout()
        elif sub_choice == '7':
            self.logout()
            self.exit = True
            print("Bye, have a nice day")
        else:
            print("\n * Invalid choice. Please try again. * ")



    def run(self):
        while not self.exit:
            if self.user.online == 0:
                self.wellcome_page()
            if self.user.online == 1:
                print(f"\n * Welcome {self.user.user_full_name}! You are now connected. *")
                if type(self.user) == Client:
                        self.customer_menu()
                else:
                    self.management_menu()



if __name__ == "__main__":
    cli = StoreCLI()
    cli.run()