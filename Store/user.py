from Store.storeerror import StoreError

class User:
    """
    A class to represent a user of the store.

    Attributes
    ----------
    user_id : str
    user_full_name : str
    password : str
    online : int
    address : str, optional
    payment : Payment, optional
    currency : str
    """

    def __init__(self, user_id, user_full_name, password, online=0, address=None, payment=None):
        """
        Constructs all the necessary attributes for the User object.
        """
        self.__user_id = user_id
        self.__user_full_name = user_full_name
        self.__password = password
        self.__online = online
        self.__address = address
        self.payment = payment
        self.currency = "₪ILS"

    @property
    def user_id(self):
        """
        Return the user ID.
        """
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user ID.

        Parameters
        ----------
        user_id : str
        """
        if user_id.isdigit():
            self.__user_id = user_id
        else:
            raise ValueError('user_id must be an integer')

    @property
    def user_full_name(self):
        """
        Return the user full name.
        """
        return self.__user_full_name

    @user_full_name.setter
    def user_full_name(self, name):
        """
        Sets the user full name.

        Parameters
        ----------
        name : str
        """
        if len(name) < 3:
            raise ValueError('user full name must be at least 3 characters')
        else:
            self.__user_full_name = name

    @property
    def password(self):
        """
        Return the user password.
        """
        return self.__password

    @password.setter
    def password(self, password):
        """
        Sets the user password.

        Parameters
        ----------
        password : str
        """
        if len(password) > 3:
            self.__password = password
        else:
            raise ValueError('password must be at least 4 characters')

    @property
    def online(self):
        """
        Return 0 if user logged out or 1 if user logged in.
        """
        return self.__online

    @online.setter
    def online(self, online):
        """
        Sets the user online status.

        Parameters
        ----------
        online : int
        """
        self.__online = online

    @property
    def address(self):
        """
        Return the user address
        """
        return self.__address

    @address.setter
    def address(self, address):
        """
        Sets the user address.

        Parameters
        ----------
        address : str
        """
        self.__address = address

    def change_address(self, new_address):
        """
        Changes the address of the user.

        Parameters
        ----------
        new_address : str
        """
        self.__address = new_address

    def login(self, entered_password):
        """
        Logs the user into the store.

        Parameters
        ----------
        entered_password : str
        Returns The logged-in user.
        """
        if self.password == entered_password:
            self.online = 1
            return self
        else:
            raise StoreError.AuthenticationError("\n * Wrong password * ")

    def logout(self):
        """
        Logs the user out of the store.
        """
        self.online = 0
        return True

    def change_user_password(self, new_password):
        """
        Changes the user's password.

        Parameters
        ----------
        new_password : str
        """
        self.password = new_password

    def change_name(self, new_name):
        """
        Changes the user's full name.

        Parameters
        ----------
        new_name : str
        """
        self.user_full_name = new_name

    @staticmethod
    def valid_user(user: dict):
        """
        Validates the user's information (ID, Name, Password, Type).

        Parameters
        ----------
        user : dict
        """
        errors = []

        user_type = user.get("user_type", "Client").upper()
        password = user.get("password")
        user_full_name = user.get("user_full_name")
        user_id = user.get("user_id")

        if not user_id or len(user_id) < 3 or not user_id.isdigit():
            errors.append(StoreError("* user_id must be at least 4 numbers * "))

        if not user_full_name or len(user_full_name) < 3:
            errors.append(StoreError.InvalidFullNameError(" * Full name must be at least 4 characters long * "))

        if not password or len(password) < 3:
            errors.append(StoreError.InvalidPasswordError("* Password must be at least 4 characters long *"))

        if user_type not in ['ADMIN', 'CLIENT']:
            errors.append(StoreError.InvalidInputError("* Unknown user type provided * "))

        if errors:
            raise StoreError(f"errors occurred:\n" + "\n".join([error.message for error in errors]))

    def to_dict(self):
        '''
        creating dict with all the arguments of user that will be saved to user's JSON file
        :return: dict
        '''
        return {
            'user_id': self.user_id,
            'user_full_name': self.user_full_name,
            'password': self.__password,
            'address': self.__address,
            'payment': self.payment if self.payment else None,
            'user_type': 'Admin'
        }

    def __eq__(self, other):
        """
        Checks if two user objects are equal.

        Parameters
        ----------
        other : User
        """
        if self.user_id == other.user_id and self.user_full_name == other.user_full_name and self.password == other.password:
            return True

    def __str__(self):
        return f"User: {self.user_full_name}\nID: {self.user_id}"

    def get_save_payment(self):
        """
        Returns a string representation of the saved payment information.
        """
        return f"{self.payment.get("info")[:4]} {self.payment.get('payment_method')} "
