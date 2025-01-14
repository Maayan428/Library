from os.path import exists

from SystemManagement.PopularBooks import PopularBook
from SystemManagement.Book.FileCSV import FileCSV
from SystemManagement.Book.ManageCSV import ManageCSV
from werkzeug.security import generate_password_hash

class Librarians:

    def __init__(self, first_name, last_name, user_name, password):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = generate_password_hash(password)

    def get_username(self):
        return self.user_name

    def get_password(self):
        return self.password


    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "member_id": self.user_name,
            "password": self.password
        }

    @staticmethod
    def add_new_book(book):
        ################################################################### Ive added the amount of copies of the book to the available/loaned csv
        count=ManageCSV.return_appearances(FileCSV.file_book.value,book)
        if count==0:
            ManageCSV.add_new_book(book)

            loan_status = ManageCSV.get_value_books(book, "is_loaned")
            if loan_status=="Yes":
                for i in range(ManageCSV.get_value_books(book, "copies")):
                    ManageCSV.add_book_to_csv(FileCSV.file_loaned.value, book)
                    ManageCSV.add_to_parameter(FileCSV.file_book.value, book, "currently_loaned")
            else:
                for i in range(ManageCSV.get_value_books(book, "copies")):
                    ManageCSV.add_book_to_csv(FileCSV.file_available.value, book)
        else:
            ManageCSV.add_to_parameter(FileCSV.file_book.value,book,"copies")
            ManageCSV.add_book_to_csv(FileCSV.file_available.value,book)
            ManageCSV.update_is_loaned(book)

    @staticmethod
    def remove_book(book):
        count = int(ManageCSV.return_appearances(FileCSV.file_book.value, book))
        if count==0:
            print("Error: Book does not exist")
        else:
            copies=int(ManageCSV.get_value_books(book, "copies"))
            currently_loaned=int(ManageCSV.get_value_books(book, "currently_loaned"))
            if currently_loaned == copies:
                print("Error: All books are loaned")
                return False
            else:
                if copies>1:
                    ManageCSV.sub_from_parameter(FileCSV.file_book.value, book,"copies")
                    ManageCSV.delete_book_from_csv(FileCSV.file_available.value, book)
                else:
                    ManageCSV.delete_book_from_csv(FileCSV.file_book.value, book)
                    ManageCSV.delete_book_from_csv(FileCSV.file_available.value, book)
                return True


    @staticmethod
    def lend_book_to_member(member,book):
        if_exists = int(ManageCSV.return_appearances(FileCSV.file_book.value, book))
        if if_exists==0:
            print("Error,the book not found")
        else:
            status_loan = ManageCSV.get_value_books(book,"is_loaned")
            if status_loan=="No":
                ManageCSV.delete_book_from_csv(FileCSV.file_available.value, book)
                ManageCSV.add_book_to_csv(FileCSV.file_loaned.value, book)
                ManageCSV.add_to_parameter(FileCSV.file_book.value,book, "currently_loaned")
                ManageCSV.update_is_loaned(book)
            else:
                print("No books available")
                book.add_waiting_list(member)
            ManageCSV.add_to_parameter(FileCSV.file_book.value,book,"requests")

    @staticmethod
    def return_book_to_library(book):
        if_exists=ManageCSV.return_appearances(FileCSV.file_loaned.value,book)
        if if_exists==0:
            print("Error,the book not found")
        elif len(book.waiting_list)==0:
            ManageCSV.delete_book_from_csv(FileCSV.file_loaned.value, book)
            ManageCSV.add_book_to_csv(FileCSV.file_available.value, book)
            ManageCSV.sub_from_parameter(FileCSV.file_book.value,book,"currently_loaned")
            ManageCSV.update_is_loaned(book)
        else:
            person = book.pop_first_member()
            # notify the book is available and has been passed to person

































