class Display:
    '''
    The Display class contains static methods for displaying various menus
    and options in the Electronic Store Management System.
    all functions returns choice
    '''

    @staticmethod
    def display_user():
        '''
           Displays the main menu for user interaction including options to log in,
           sign up, reset password, or exit.
        '''
        print("\n Welcome to Electronic Store Management System!\n ")
        print("1. Existing User? Log in")
        print("2. New User? Sign up now ")
        print("3. Forgot password? Reset here")
        print("4. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_client(new_message, cart, sales):
        '''
        Displays the client menu with options to update details
        , view cart, view collections, check orders, logout, or exit.
        '''
        print("\n * Welcome to Electronic Store Management Main menu * \n ")
        if new_message > 0:
            print(f"\n * There are {new_message} new notifications on orders * \n")
        print("\n1. Update details")
        if cart.count_item > 0:
            print(f'2. Cart({cart.count_item}')
        else:
            print("2. Cart(0)")
        if len(sales) > 0:
            print("3.   Collection * new sale *")
        else:
            print("3. Collection")
        if new_message > 0:
            print(f"4. Orders * {new_message} notifications * ")
        else:
            print("4. Orders")
        print("5. Logout")
        print("6. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_coupon(coupon):
        '''
        Displays the coupon menu for user interaction if using the coupon or not
        :param coupon:
        '''
        print(f"\nWould you like to use your {coupon}% coupon?")
        print('\n1. Yes')
        print('2. No')
        choice = input('\nEnter your choice: ')
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_order(cart):
        '''
        Displays the order menu with options to view catalog, go to cart, or exit.
        '''
        print("\n * Order menu *")
        print("\n1. Catalog ")
        if cart.total_amount > 0:
            print(f"2. Go to Cart({cart.count_item})")
        print("3. Exit ")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_payment():
        '''
        Displays the payment menu with options to pay with Credit-Card, PayPal or cash.
        '''
        print("How would you like to pay?")
        print("\n1.Credit Card")
        print("2.Paypal")
        print("3.Cash")
        print("4.Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_product_type():
        '''
        Displays the product type selection menu.
        '''
        print("\n * Select Product type *")
        print('\n1. TV')
        print('2. Computer')
        print('3. Mobile Phone')
        print('4. Accessories')
        print("0. Exit Or Advanced Search")
        choice = input("\nEnter Your Choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def advanced_search():
        '''
        Displays the advanced search options.
        '''
        print("ֿ\n***** Advanced search system ****\n")
        print("1. Search by Name")
        print("2. Search by Model")
        print("3. Search by Price range")
        print("4. Search by Rating range")
        print("5. Exit")
        select = input("\nEnter your choice: ")
        return select

    @staticmethod
    def display_discount():
        '''
        Displays the discount options for category or specific product.
        '''
        print("\nChoose an option:")
        print("\n1. Discount from a category")
        print("2. Discount from a specific product")
        choice = input("\nEnter your choice: ").replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        return choice

    @staticmethod
    def display_client_details():
        '''
        Displays the options for updating client details.
        '''
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
        '''
        Displays the options for updating user details.
        '''
        print("\n * Choose which detail you want to change *")
        print("\n1. Name")
        print("2. Password")
        print("3. Address")
        print("4. Currency")
        print('5. Exit')
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def cart_display(cart):
        '''
        Displays the shopping cart menu with options to proceed to checkout
        , change items, empty the cart, or exit.
        '''
        print("\n * Shopping Cart *\n")
        print(cart)
        print("\n1. Proceed to checkout ")
        print("2. Change")
        print("3. Empty the cart")
        print("4. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def orders_history(list_orders_client):
        '''
        Displays the user's order history.
        '''
        print("\n * Your orders *\n")
        print(list_orders_client)
        print("1.View order details")
        print("2.Exit")
        choice = input("\nEnter your choice: ")
        return choice

    @staticmethod
    def display_manage_user():
        '''
        Displays the manage user account,
        '''
        print("\n * Wellcome to manage users display *\n")
        print("1. View all clients")
        print("2. Add user")
        print("3. Remove user")
        print("4. Change password")
        print("5. Update client's details")
        print("6. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_manage_product():
        '''
        Displays the manage product menu,
        '''
        print("1. Add Product or Adding a quantity to an existing product ")
        print("2. Remove Product")
        print("3. Add Discount")
        print("4. Remove Discount")
        print("5. Product list")
        print("6. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_manage_order():
        '''
        Displays the manage order menu,
        '''
        print("1. Update order status")
        print("2. List Orders")
        print("3. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))

    @staticmethod
    def display_menu():
        '''
        Displays the main menu options,
        '''
        print("4. Reporting")
        print("5. Logout")
        print("0. Exit")
        choice = input("\nEnter your choice: ")
        return choice.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
