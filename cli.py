
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
                    new_user = Client(user_id, full_name, pass_word)
                    if self.store.add_user(new_user):
                        self.set_address(new_user)
                        new_user.online = 1
                        self.store.users[user_id] = new_user
                        print("\n * User registered successfully. * ")
                        new_user.coupon = 5
                        print("Thank you for register. Enjoy a 5% coupon !")

                    else:
                        print("\n * User already exists please try to log in *")
                else:
                    print("\n The password must contain at least 4 characters. Please try again ")
            else:
                print("\n * Invalid full name. Try again * ")
        else:
            print("\n * User ID must be at least 4 digit.Try again * ")

        return new_user

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


    def add_review(self,order):
        for key, value in order.product_dict.items():
            print(key)
            prod = self.store.collection[key]
            star = input("\nEnter a rating between 1-5: ")
            review = input("Enter your opinion: ")
            new = Rating(star, review)
            prod.add_review(new)
            self.store.collection[key] = prod

    def display_order_user(self,user):
        order_number = input("Enter order number: ")
        if order_number.isdigit() :
            order_number = int(order_number)
            if 0 < order_number < len(user.order_history):
                order = user.order_history[order_number]
                print(order)
                if order.status == 'delivered':
                    print("Are you interested in giving a review on the order?\n1. Yes!\n2. No")
                    choice = input("Enter your choice: ")
                    if choice == '1':
                        self.add_review(order)


    def display_client(self,notifications):
        if len(self.store.sales) > 0:
            for sale in self.store.sales:
                print(sale)
        if notifications > 0:
            print(f"\n * There are {notifications} new notifications on orders * \n")
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

    def display_coupon(self, user):
        print(f"\nWould you like to use your {user.coupon}% coupon?")
        print('\n1. Yes')
        print('2. No')
        choice = input('\nEnter your choice: ')
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def set_address(self, user):
        print("\n * Please enter the details *\n")
        new_address = input("Country: ")
        city = input("City: ")
        street = input("Street: ")
        apt = input("Building,Apt,Floor: ")
        new_address += f",{city},{street},{apt}"
        new_address.replace(" ", "").translate(str.maketrans("", "", ".!?;:"))
        if len(new_address) > 3 and isinstance(user, Client):
            user.change_address(new_address)
            self.store.users[user.user_id] = user
            print("\n * Address has been set successfully *")
            print(f"\n * New Address updated: *\n {new_address}")
        else:
            user.address = None
            print("\n * Not enough details were entered for setting address. *")

    def display_order(self):
        print("\n1.Add Item ")
        print("2.Check Out or Exit ")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))


    def display_payment(self,order):
        print(order.converter())
        print(order.payments())
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

            for i in range(4):
                pay_option = self.display_payment(order)
                if pay_option == '1':
                    card_holder = input("Name on card: ")
                    card_number = input("Card number: ")
                    paymethood = Payment(card_holder, card_number,"Credit Card")
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
                        paymethood = Payment(user.user_full_name, None, 'PayPal')
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
        print("\n * Select Product type *")
        print('\n1. TV')
        print('2. Computer')
        print('3. Mobile Phone')
        print('4. Accessories')
        print('5. All')
        print("0. Exit Or Manual Search")
        choice = input("\nEnter Your Choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def product_type(self,choice = None):
        if choice ==None:
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
        if category is not None:
            discount = self.discount()
            self.store.sale_prodduct_type(choice,discount)
            self.store.new_discount(category, discount)
        if category is None:
            print("\nAre you interested in adding a discount to a specific product?")
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
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Add Discount")
        print("4. Remove Discount")
        print("5. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def display_menu(self,notifications):
        if notifications > 0:
            print(f"\n * There are {notifications} new notifications Reporting *")
        print(" \n *  Electronic store Management System * \n")
        print("1. Product Manager")
        print("2. User Manager")
        print("3. Update order status")
        print("4. List Product")
        print("5. List Orders")
        if notifications > 0:
            print(f"7. Reporting * {notifications} notifications *")
        else:
            print("6. Reporting")
        print("7. Logout")
        print("0. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))


    def pick_item(self, lst,):
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
                if select < len(lst) and select>=-1:
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
                    if choice!= -100 and choice is not None:
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
                break
            elif sub_choice == '2':
                self.remove_product()
                break
            elif sub_choice == '3':
                self.add_discount()
                break
            elif sub_choice == '4':
                self.remove_discount()
            elif sub_choice == '5':
                break
            else:
                print("\n * Invalid choice. Please try again. *\n")

    def search_system(self):
        print("\n * Welcome to the catalog *")
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
        if len(search) > 0:
            print(f" \n * This products exists in the system please choose product for adding amount. * ")
            s = self.pick_item(search)
            if s != -100:
                pro = search[s]
                print(f"\n{pro}")
                print("How much would you like to add to the inventory?")
                quan = input("Add quantity: ")
                self.store.collection[pro.get_key_name()].add_quantity(int(quan))
                print("\n * Quantity added successfully *")
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
                    pro =Tv(name,model,description,price,quantity,size,tv_type)
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

    def apply_coupon(self, order, user):
        if user.coupon is not None:
            for each in range(5):
                choice_coupon = self.display_coupon(user)
                if choice_coupon == '1':
                    order.total_amount = order.total_amount * (1 - (user.coupon / 100))
                    break
                elif choice_coupon == '2':
                    break
                else:
                    print("\n * Invalid choice. Try again. *")
                    print(f" * You have left {4 - each} tries. *\n")

            return choice_coupon

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
            coupon = self.apply_coupon(new_order, user)

            payment = self.pay(new_order, user)
            if payment:
                new_order.pay_order(payment)
                self.store.place_order(new_order)
                print(f" {new_order}\n {payment}\n * The order was successfully completed * ")
                if coupon == 1:
                    user.use_coupon()


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
        print("\n Your orders \n\n")
        print(user.update_client())
        if len(user.order_history) > 0:
            self.display_order_user(user)

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
            user.online =1

            while user.online ==1:
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
                           print(user.logout())
                           break

                        elif sub_choice == '7':
                            return "Bye, have a nice day"
                        else:
                            print("\n * Invalid choice. Please try again. * ")
                else:
                    while True:

                                choice = self.display_menu(self.store.reporting.new_update)

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
                                    user.logout()
                                    break

                                elif choice == '0':
                                    return "Bye, have a nice day"
                                else:
                                    print("\n* Invalid choice. Please try again.* ")


if __name__ == "__main__":
    cli = StoreCLI()
    cli.run()