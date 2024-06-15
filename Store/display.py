from Store.payment_calculator import CurrencyConverter


class Display:
    @staticmethod
    def display_user():
        print("\n Welcome to Electronic Store Management System!\n ")
        print("1. Existing User? Log in")
        print("2. New User? Sign up now ")
        print("3. Forgot password? Reset here")
        print("4. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_client(user, cart, store):
        print("\n * Welcome to Electronic Store Management Main menu * \n ")
        if user.new_message > 0:
            print(f"\n * There are {user.new_message} new notifications on orders * \n")
        print("\n1. Update details")
        if cart["count_item"] > 0:
            print(f'2. Cart({cart["count_item"]})')
        else:
            print("2. Cart(0)")
        if len(store.sales) > 0:
            print("3.   Collection * new sale *")
        else:
            print("3. Collection")
        if user.new_message > 0:
            print(f"4. Orders * {user.new_message} notifications * ")
        else:
            print("4. Orders")
        print("5. Logout")
        print("6. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_coupon(user):
        print(f"\nWould you like to use your {user.coupon}% coupon?")
        print('\n1. Yes')
        print('2. No')
        choice = input('\nEnter your choice: ')
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_order(cart):
        print("\n * Order menu *")
        print("\n1. Catalog ")
        if cart["total_amount"] > 0:
            print(f"2. Go to Cart({cart["count_item"]})")
        print("3. Exit ")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_payment():
        print("How would you like to pay?")
        print("\n1.Credit Card")
        print("2.Paypal")
        print("3.Cash")
        print("4.Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_product_type():
        print("\n * Select Product type *")
        print('\n1. TV')
        print('2. Computer')
        print('3. Mobile Phone')
        print('4. Accessories')
        print("0. Exit Or Advanced Search")
        choice = input("\nEnter Your Choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    def advanced_search():
        print("ֿ\n*****Advanced search system****\n")
        print("1. Search by Name")
        print("2. Search by Model")
        print("3. Search by Price range")
        print("4. Search by Rating range")
        print("5. Exit")
        select = input("\nEnter your choice: ")
        return select
    @staticmethod
    def display_remove_discount():
        print("\nChoose an option:")
        print("\n1. Remove discount from a category")
        print("2. Remove discount from a specific product")
        choice = input("\nEnter your choice: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        return choice

    @staticmethod
    def display_client_details():
        print("\n * Choose which detail you want to change *")
        print("\n1. Client Name")
        print("2. Client Password")
        print("3. Client Address")
        print("4. Client Coupon")
        print("5. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_update_details():
        print("\n * Choose which detail you want to change *")
        print("\n1. Name")
        print("2. Password")
        print("3. Address")
        print("4. Currency")
        print('5. Exit')
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def cart_display(user, cart):
        print("\n * Shopping Cart *\n")
        if cart["total_amount"] > 0:
            print(cart["product_dict"])
            print(f"{CurrencyConverter.convert(cart["total_amount"],"₪ILS",user.currency)} {user.currency}")
            print("\n1. Proceed to checkout ")
            print("2. Change")
            print("3. Empty the cart")
            print("4. Exit")
            choice = input("\nEnter your choice: ")
            return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        else:
            return 4

    @staticmethod
    def orders_history(user):
        print("\n * Your orders *\n")
        print(user.list_orders_client())
        print("1.View order details")
        print("2.Exit")
        choice = input("\nEnter your choice: ")
        return choice

    @staticmethod
    def display_manage_user(store):
        if store.reporting.new_update["users"] > 0:
            for i in store.reporting.message["users"]:
                print(i)
        store.reporting.total_update -= store.reporting.new_update["users"]
        store.reporting.new_update["users"] = 0
        store.reporting.message["users"] = []
        print("\n * Wellcome to manage users display *\n")
        print("1. View all clients")
        print("2. Add user")
        print("3. Remove user")
        print("4. Add admin")
        print("5. Change password")
        print("6. Update client's details")
        print("7. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_manage_product(store):
        print("\n * Wellcome to manage product display *\n")
        if store.reporting.new_update["products"] > 0:
            for i in store.reporting.message["products"]:
                print(f"{i}")
        store.reporting.total_update -= store.reporting.new_update["products"]
        store.reporting.new_update["products"] = 0
        store.reporting.message["products"] = []
        print("1. Add Product or Adding a quantity to an existing product ")
        print("2. Remove Product")
        print("3. Add Discount")
        print("4. Remove Discount")
        print("5.Product list")
        print("6. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_manage_order(store):
        print("\n * Wellcome to manage order display *\n")
        if store.reporting.new_update["orders"] > 0:
            for i in store.reporting.message["orders"]:
                print(f"{i}")
        store.reporting.total_update -= store.reporting.new_update["orders"]
        store.reporting.new_update["orders"] = 0
        store.reporting.message["orders"] = []

        print("1. Update order status")
        print("2. List Orders")
        print("3. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_menu(store):
        product_manager = "1. Product Manager"
        order_manager = "3. Order Manager"
        user_manager = "2. User Manager"
        if store.reporting.total_update > 0:
            print(f"\n * There are {store.reporting.total_update} new notifications *")
            for key, item in store.reporting.new_update.items():
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
        print("4. Reporting")
        print("5. Logout")
        print("0. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))