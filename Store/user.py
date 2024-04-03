class User:
    def __init__(self, user_id =None,user_full_name =None, password=None,onlne = False):
        self.user_id = user_id
        self.user_full_name = user_full_name
        self.password = password
        self.online = onlne


    def login(self, entered_password):
        if self.password == entered_password:
            self.online =True
            return True
        return False,"Login failed. Incorrect user ID or password."

    def logout(self):
        print('Logged out successfully.')
        return True

    def ok(self):
        if self.user_id is None or self.password is None:
            return False



    def __str__(self):
        return f"User: {self.user_full_name}\nID: {self.user_id}\nPassword: {self.password}"
