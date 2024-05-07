class User:
    def __init__(self, user_id = None, user_full_name = None, password = None, online = 0, address = None, payment=None):
        self.user_id = user_id
        self.user_full_name = user_full_name
        self.password = password
        self.online = online
        self.address = address
        self.payment = payment

    def login(self, entered_password):
        if self.password == entered_password:
            self.online = 1
            return True
        else:
            return False

    def logout(self):
        self.online = 0
        print('Logged out successfully.')
        return True

    def change_user_password(self, new_password):
        self.password = new_password
        return True

    def __str__(self):
        return f"User: {self.user_full_name}\nID: {self.user_id}"
