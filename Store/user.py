from Store.storeerror import StoreError


class User:
    def __init__(self, user_id, user_full_name, password, online=0, address=None, payment=None):
        self.__user_id = user_id
        self.__user_full_name = user_full_name
        self.__password = password
        self.__online = online
        self.__address = address
        self.payment = payment
        self.currency = "₪ILS"

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        if user_id.isdigit():
            self.__user_id = user_id
        else:
            raise ValueError('user_id must be an integer')

    @property
    def user_full_name(self):
        return self.__user_full_name

    @user_full_name.setter
    def user_full_name(self, name):
        if len(name) < 3:
            raise ValueError('user full name must be at least 3 characters')
        else:
            self.__user_full_name = name

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if len(password) > 3:
            self.__password = password
        else:
            raise ValueError('password must be at least 4 characters')

    @property
    def online(self):
        return self.__online

    @online.setter
    def online(self, online):
        self.__online = online

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address

    def change_address(self, new_address):
        self.__address = new_address

    def login(self, entered_password):
        if self.password == entered_password:
            self.online = 1
            return self
        else:
            raise StoreError.AuthenticationError("\n * Wrong password * ")

    def logout(self):
        self.online = 0
        return True

    def change_user_password(self, new_password):
        self.password = new_password

    def change_name(self, new_name):
        self.user_full_name = new_name

    @staticmethod
    def valid_user(user: dict):
        errors = []

        user_type = user.get("user_type", "Client").upper()
        password = user.get("password")
        user_full_name = user.get("user_full_name")
        user_id = user.get("user_id")

        if not user_id or len(user_id) < 3 or not user_id.isdigit():
            errors.append(StoreError("* user_id must be at least 4 numbers * "))
        # בדיקת שם מלא
        if not user_full_name or len(user_full_name) < 3:
            errors.append(StoreError.InvalidFullNameError(" * Full name must be at least 4 characters long * "))

        # בדיקת סיסמה
        if not password or len(password) < 3:
            errors.append(StoreError.InvalidPasswordError("* Password must be at least 4 characters long *"))

        # בדיקת סוג משתמש
        if user_type not in ['ADMIN', 'CLIENT']:
            errors.append(StoreError.InvalidInputError("* Unknown user type provided * "))

        if errors:
            raise StoreError(f"errors occurred:\n" + "\n".join([error.message for error in errors]))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_full_name': self.user_full_name,
            'password': self.__password,
            'address': self.__address,
            'payment': self.payment if self.payment else None,
            'user_type': 'Admin'
        }

    def __eq__(self, other):
        if self.user_id == other.user_id and self.user_full_name == other.user_full_name and self.password == other.password:
            return True

    def __str__(self):
        return f"User: {self.user_full_name}\nID: {self.user_id}"

    def get_save_payment(self):
        return f"{self.payment.get("info")[:4]} {self.payment.get('payment_method')} "
