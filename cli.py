from Store.store import Store
from Store.order import Order
from Store.product import Product
from Store.user import User
from Store.reporting import Reporting
class StoreCLI:
    def __init__(self):
        self.store = Store()
    def log_in(self,user):
        user_id = input("Enter User ID")
        if user_id.isdigit():
            user_id = int(user_id)
            if user_id in self.store.users:
                user = self.store.users[user_id]
                password = input("Enter Password: ")
                user.login(password)
        return user

    def register(self,new_user):
        print("\nWelcome to the registration systemֿ\n")
        print(" User id must be a at least 4 digit ")
        user_id = input("Enter User ID: ")
        if user_id.isdigit() and len(user_id) >3 :
            print("\n Full name must be at least 4 characters \n")
            full_name = input("Enter your Full name: ")
            if len(full_name) >3:
                print("\n The password must contain at least 4 characters ")
                pass_word = input("Enter your Password: ")
                if len(pass_word) > 3:
                    new_user = User(int(user_id),full_name,pass_word)
                    if self.store.add_user(new_user):
                        new_user.online = 1

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
        print("2. New User ? Sign up now ")
        print("3. Exit")
        choice = input("\nEnter your choice: ")
        return choice


    def display_order(self):
        print("\n1.Add Item")
        print("\n2.Check Out")
        choice = input(" Enter your choice: ")
        return choice




    def change_status(self):
        print(f"{self.store.list_orders()}")
        order_num = input("\nPlease Enter the order number")
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


    def display_menu(self):
            print("\nElectronic store Management System\n")
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

    def add_item(self,order):
        self.list_products()
        name = input("\nEnter Product name: ")
        if name in self.store.collection:
            print(self.store.collection[name])
            how_much = input("\nEnter a quantity of the following product: ")
            if how_much.isdigit():
                how_much = int(how_much)
                self.store.add_item_order(self.store.collection[name],how_much,order)
        else:
            print("\nThe product you entered does not exist in the store")

    def add_product(self):
        name = input("Enter Product Name: ")
        description = input("Enter Model: ")
        price = input("Enter Price: ")
        quantity = input("Enter Quantity: ")
        if price.isdigit() and quantity.isdigit():
            price = float(price)
            quantity = int(quantity)
            product = Product(name,description,price,quantity)
            self.store.add_product(product)
        else:
            print("Price and Quantity must be a digit")

    def place_order(self):
        customer_name = input("Enter Customer Name: ")
        new_order = Order(customer_name)
        self.orders()
        self.add_item(new_order)
        while True:
            choice = self.display_order()
            if choice == '1':
                self.add_item(new_order)
            elif choice =='2':
                break

        if new_order.total_amount != 0:
            self.store.place_order(new_order)
            print(new_order)

    def remove_product(self):
       name = ("Input Product Name: ")
       if name in self.store.collection:
            print(f"{self.store.collection[name]} has been removed")
            self.store.remove(self.store.collection[name])
    def list_products(self):
        print(self.store.list_products())

    def orders(self):
        for order_number in self.store.list_orders():
            print(order_number)


    def reporting(self):
        print(self.store.reporting)
    def welcome_page(self):
        user = User()
        while user.online == 0:
            selc = self.display_user()
            if selc == '1':
                user = self.log_in(user)
            elif selc == '2':
                user = self.register(user)
            elif selc == '3':
                break

            else:
                print("Invalid choice.")
            if user.online == 0:
                print("\nLogin failed. Please check your credentials and try again.\n")
        return user

    def run(self):

        user = self.welcome_page()
        print(f"\nwelcome {user.user_full_name}you are now connected\n")
        while True:

                    choice = self.display_menu()

                    if choice == '1':
                        self.add_product()
                    elif choice == '2':
                        self.register()
                    elif choice == '3':
                        self.place_order()
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
                        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    cli = StoreCLI()
    cli.run()