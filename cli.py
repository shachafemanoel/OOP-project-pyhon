from Store.store import Store
from Store.order import Order
from Store.product import Product
from Store.user import User
class StoreCLI:
    def __init__(self):
        self.store = Store()
    def log_in ():
        pass
    def display_menu(self):
        print("\nElectronic store Management System")
        print("1. Add Product")
        print("2. Add User")
        print("3. New Order")
        print("4. Remove Product")
        print("5. List Product")
        print("6. List Orders")
        print("7. Exit")
        choice = input("Enter your choice: ")
        return choice

    def add_book(self):
        ISBN = input("Enter ISBN: ")
        title = input("Enter title: ")
        author = input("Enter author: ")
        genre = input("Enter genre: ")
        book = Book(ISBN, title, author, genre)
        if self.library.add_book(book):
            print("Book added successfully.")
        else:
            print("Book already exists.")

    def add_member(self):
        member_id = input("Enter member ID: ")
        name = input("Enter member name: ")
        member = Member(member_id, name)
        if self.library.add_member(member):
            print("Member added successfully.")
        else:
            print("Member already exists.")

    def borrow_book(self):
        ISBN = input("Enter book ISBN to borrow: ")
        member_id = input("Enter member ID: ")
        success, message = self.library.borrow_book(ISBN, member_id)
        if success:
            print("Book borrowed successfully.")
        else:
            print(message or "Unable to borrow book.")

    def return_book(self):
        ISBN = input("Enter book ISBN to return: ")
        member_id = input("Enter member ID: ")
        success, message = self.library.return_book(ISBN, member_id)
        if success:
            print("Book returned successfully.")
        else:
            print(message or "Unable to return book.")

    def list_books(self):
        for book_info in self.library.list_books():
            print(book_info)

    def list_members(self):
        for member_info in self.library.list_members():
            print(member_info)

    def run(self):
        while True:
            choice = self.display_menu()

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.add_member()
            elif choice == '3':
                self.borrow_book()
            elif choice == '4':
                self.return_book()
            elif choice == '5':
                self.list_books()
            elif choice == '6':
                self.list_members()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    cli = LibraryCLI()
    cli.run()