from SystemManagement.ManageCSV import ManageCSV
from SystemManagement.Notification import Notification


class Library:
    """
    Singleton class for managing library operations, including notifications,
    librarian registration and removal, and retrieving most popular books.
    """

    _instance = None

    def __init__(self):
        """
        Initializes the library instance.
        Ensures the class is a singleton by preventing direct instantiation.
        """
        if Library._instance is not None:
            raise Exception("This is a singleton class, use get_instance() to get the instance.")
        self.notification_system = Notification()

    def get_notifications(self):
        """
        Retrieves all notifications from the notification system.
        - Returns a string with all notifications if available.
        - Returns a message indicating no notifications if the list is empty.
        """
        notifications = self.notification_system.get_all_notifications()
        if notifications:
            return "Notification: " + "\nNotification: ".join(notifications)
        else:
            return "No notifications available."

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of the Library class.
        - If no instance exists, creates one.
        """
        if Library._instance is None:
            Library._instance = Library()
        return Library._instance

    @staticmethod
    def remove_user(user):
        """
        Removes a librarian user from the library system.
        - Searches for the user in the librarians list.
        - Removes the user if found and deletes their details from the CSV file.
        """
        for librarian in Library.get_instance().librarians_list:
            if librarian.to_dict() == user.to_dict():
                Library.get_instance().librarians_list.remove(librarian)
                ManageCSV.delete_user_from_csv(librarian)
                break

    @staticmethod
    def register_librarian(librarian):
        """
        Registers a new librarian in the library system.
        - Checks if the username already exists.
        - If not, adds the librarian to the CSV file and sends a notification.
        - Returns a message indicating success or that the user already exists.
        """
        if not ManageCSV.user_exists(librarian.to_dict()["user_name"]):
            ManageCSV.add_users_to_csv(librarian)
            Library.get_instance().notification_system.notify_observers(
                f"Librarian {librarian.to_dict()['user_name']} was registered."
            )
            return "Librarian added successfully"
        else:
            return "User already exists"

    @staticmethod
    def get_most_popular():
        """
        Retrieves the most popular books in the library based on loan data.
        - Returns a DataFrame with popular books if available.
        - Returns False if no popular books are found.
        """
        popular_books = ManageCSV.get_popular_books()
        if popular_books.empty:
            return False
        else:
            return popular_books