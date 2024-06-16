from Store.client import Client
from Store.json import DataManager
from Store.user import User


class UserManager:
    def __init__(self):
        self.users = {}
        self.message = []
        self.new_update = 0

    def load_users(self):
        self.users = DataManager.load_users()

    def save_users(self):
        DataManager.save_users(self.users)

    def add_user(self, user: dict):
        if user.get("user_id") not in self.users:
            user_type = user.pop("user_type", "Client").upper()
            if user_type == 'ADMIN':
                new_user = User(**user)
            elif user_type == 'CLIENT':
                new_user = Client(**user)
                new_user.coupon = 5
            new_user.user_id = new_user.user_id.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
            self.users[new_user.user_id] = new_user
            return new_user
        return None

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    def log(self, user_id, password):
        login = user_id.replace(" ", "").translate(str.maketrans("", "", ".,!?;:"))
        if login in self.users and self.users[login].login(password):
            return self.users[login]
        return None

    def set_address(self, user_id, address):
        if user_id in self.users:
            self.users[user_id].change_address(address)
            return True
        return False

    def use_coupon(self, user):
        self.users[user.user_id].use_coupon()
