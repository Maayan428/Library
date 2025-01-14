from SystemManagement.Book.ManageCSV import ManageCSV
from SystemManagement.Librarians import Librarians


class Library:

    _instance = None

    def __init__(self):
        if Library._instance is not None:
            raise Exception("This is a singleton class, use get_instance() to get the instance.")
        # self.librarians_list = []
        # I've deleted the list because we use the Users_CSV
        self.queue_priority = []

    @staticmethod
    def get_instance():
        if Library._instance is None:
            Library._instance = Library()
        return Library._instance


    @staticmethod
    def remove_user(user):
        for librarian in Library._instance.librarians_list:
            if librarian.to_dict()==user.to_dict():
                Library._instance.librarians_list.remove(librarian)
                ManageCSV.delete_user_from_csv(librarian)
                break

    # get popular books
    @staticmethod
    def register_librarian(first_name, last_name, user_name, password, conf_password):
        if not ManageCSV.user_exists(str(user_name)):
            if password == conf_password:
                librarian = Librarians(first_name, last_name, user_name, password)
                ManageCSV.add_users_to_csv(librarian)
                print("Librarian added successfully")
                return "Librarian added successfully"
            else:
                print("Passwords do not match")
                return "Passwords do not match"
        else:
            print("User already exists")
            return "User already exists"





