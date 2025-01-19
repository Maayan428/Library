from SystemManagement.Library import Library
from SystemManagement.Book.FileCSV import FileCSV
from SystemManagement.ManageCSV import ManageCSV
from werkzeug.security import generate_password_hash


class Librarians:
    """
    Manages librarian-related operations, such as handling books,
    lending books to members, and managing the waiting list.
    """

    def __init__(self, first_name, last_name, user_name, password):
        """
        Initializes a librarian object with their personal details and a hashed password.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = generate_password_hash(password)

    def get_username(self):
        return self.user_name

    def get_password(self):
        """Returns the hashed password of the librarian."""
        return self.password

    def to_dict(self):
        """Converts librarian details into a dictionary format."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "password": self.password
        }

    @staticmethod
    def add_new_book(book):
        """
        Adds a new book to the library system.
        - If the book does not exist, it's added to both the main catalog and relevant CSV files (loaned/available).
        - If the book already exists, the number of copies is updated.
        - Notifications are sent to observers about the addition of a new book.
        """
        count = ManageCSV.return_appearances(FileCSV.file_book.value, book)
        if count == 0:
            ManageCSV.add_new_book(book)
            loan_status = ManageCSV.get_value_books(book, "is_loaned")
            if loan_status == "Yes":
                for i in range(ManageCSV.get_value_books(book, "copies")):
                    ManageCSV.add_book_to_csv(FileCSV.file_loaned.value, book)
                    ManageCSV.add_to_parameter(FileCSV.file_book.value, book, "currently_loaned")
            else:
                for i in range(ManageCSV.get_value_books(book, "copies")):
                    ManageCSV.add_book_to_csv(FileCSV.file_available.value, book)
        else:
            ManageCSV.add_to_parameter(FileCSV.file_book.value, book, "copies")
            ManageCSV.add_book_to_csv(FileCSV.file_available.value, book)
            ManageCSV.update_is_loaned(book)
        Library.get_instance().notification_system.notify_observers(f"New book added to the library: {book.to_dict()['title']}")

    @staticmethod
    def remove_book(book):
        """
        Removes a book from the library system.
        - If the book is fully loaned, removal is not allowed.
        - Reduces the number of copies if there are multiple.
        - Sends notifications about book removal.
        """
        count = int(ManageCSV.return_appearances(FileCSV.file_book.value, book))
        if count == 0:
            print("Error: Book does not exist")
        else:
            copies = int(ManageCSV.get_value_books(book, "copies"))
            currently_loaned = int(ManageCSV.get_value_books(book, "currently_loaned"))
            if currently_loaned == copies:
                print("Error: All books are loaned")
                return False
            else:
                Library.get_instance().notification_system.notify_observers(
                    f"The book: {book.to_dict()['title']} has been removed from the library")
                if copies > 1:
                    ManageCSV.sub_from_parameter(FileCSV.file_book.value, book, "copies")
                    ManageCSV.delete_book_from_csv(FileCSV.file_available.value, book)
                else:
                    ManageCSV.delete_book_from_csv(FileCSV.file_book.value, book)
                    ManageCSV.delete_book_from_csv(FileCSV.file_available.value, book)
                return True

    @staticmethod
    def lend_book_to_member(member, book):
        """
        Lends a book to a member.
        - If the book is available, it moves from available to loaned status.
        - If already loaned, the member is added to the waiting list.
        - Sends notifications about lending or waiting list updates.
        """
        if_exists = int(ManageCSV.return_appearances(FileCSV.file_book.value, book))
        print(f"Looking for book: {book}")
        print(f"File path: {FileCSV.file_book.value}")
        if if_exists == 0:
            print("Error, the book not found")
        else:
            status_loan = ManageCSV.get_value_books(book, "is_loaned")
            if status_loan == "No":
                ManageCSV.add_to_parameter(FileCSV.file_book.value, book, "requests")
                ManageCSV.delete_book_from_csv(FileCSV.file_available.value, book)
                ManageCSV.add_book_to_csv(FileCSV.file_loaned.value, book)
                ManageCSV.add_to_parameter(FileCSV.file_book.value, book, "currently_loaned")
                ManageCSV.update_is_loaned(book)
                return True
            else:
                ManageCSV.add_to_parameter(FileCSV.file_book.value, book, "requests")
                ManageCSV.add_to_waiting_list(book.to_dict()["title"], member)
                Library.get_instance().notification_system.notify_observers(f"Member: {member.to_dict()['name']} added "
                                                                            f"to the waiting list of the book: {book.to_dict()['title']}")
                return False

    @staticmethod
    def return_book_to_library(book):
        """
        Handles the return of a book to the library.
        - Updates the status of the book in the catalog and CSV files.
        - If there is a waiting list, assigns the book to the next person in line.
        - Sends notifications about the return and waiting list updates.
        """
        if_exists = ManageCSV.return_appearances(FileCSV.file_loaned.value, book)
        if if_exists == 0:
            print("Error, the book not found")
            return 0
        else:
            ManageCSV.delete_book_from_csv(FileCSV.file_loaned.value, book)
            ManageCSV.add_book_to_csv(FileCSV.file_available.value, book)
            ManageCSV.sub_from_parameter(FileCSV.file_book.value, book, "currently_loaned")
            ManageCSV.update_is_loaned(book)
            person = ManageCSV.pop_from_waiting_list(book.to_dict()["title"])
            if person is not None:
                Library.get_instance().notification_system.notify_observers(f"The book: {book.to_dict()['title']} has been returned."
                                                                            f"\n Member: {person.to_dict()['name']} is waiting for it:) \n Notify at: {person.to_dict()['phone_number']}")
                Librarians.lend_book_to_member(person, book)
                return 1
            return 2