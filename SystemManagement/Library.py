from SystemManagement.ManageCSV import ManageCSV
from SystemManagement.Notification import Notification


class Library:

    _instance = None

    def __init__(self):
        if Library._instance is not None:
            raise Exception("This is a singleton class, use get_instance() to get the instance.")
        self.notification_system = Notification()


    def get_notifications(self):
        notifications = self.notification_system.get_all_notifications()
        if notifications:
            return "Notification: " + "\nNotification: ".join(notifications)
        else:
            return "No notifications available."

    @staticmethod
    def get_instance():
        if Library._instance is None:
            Library._instance = Library()

        return Library._instance

    @staticmethod
    def remove_user(user):
        for librarian in Library.get_instance().librarians_list:
            if librarian.to_dict() == user.to_dict():
                Library.get_instance().librarians_list.remove(librarian)
                ManageCSV.delete_user_from_csv(librarian)
                break

    @staticmethod
    def register_librarian(librarian):
        if not ManageCSV.user_exists(librarian.to_dict()["user_name"]):
            ManageCSV.add_users_to_csv(librarian)
            Library.get_instance().notification_system.notify_observers(f"Librarian {librarian.to_dict()["user_name"]} was registered.")
            return "Librarian added successfully"
        else:
            return "User already exists"

    @staticmethod
    def get_most_popular():
        popular_books = ManageCSV.get_popular_books()
        if popular_books.empty:
            return False
        else:
            return popular_books


