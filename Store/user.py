class User:
    def __init__(self, user_id:str , user_full_name, password:str):
        self.user_id = user_id
        self.user_full_name = user_full_name
        self.password = password

    '''def register(self, user_id, user_full_name, password):
        if self.user_id in Store.users:
            print("User already registered, please log in.")
            return False
        else:
            self.user_id = user_id
            self.user_full_name = user_full_name
            self.password = password
            print("User registered successfully.")
            return True'''

    def login(self, user_id, entered_password):
        if self.user_id == user_id and self.password == entered_password:
            print("Logged in successfully.")
            return True
        print("Login failed. Incorrect user ID or password.")
        return False

    def logout(self):
        print('Logged out successfully.')
        return True

    def authenticate(self, user_id, password):
        if self.user_id == user_id and self.password == password:
            print("authenticated successfully.")
            return True
        return False

    def __str__(self):
        return f"User: {self.user_full_name}\nID: {self.user_id}\nPassword: {self.password}"
