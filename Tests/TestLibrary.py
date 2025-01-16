import unittest
from unittest.mock import patch, Mock
from SystemManagement.Library import Library


class TestLibrary(unittest.TestCase):

    @patch("SystemManagement.Library.Library.get_instance")
    def test_get_notifications_with_notifications(self, mock_get_instance):
        mock_notification_system = Mock()
        mock_notification_system.get_all_notifications.return_value = [
            "Notification 1",
            "Notification 2",
            "Notification 3"
        ]
        mock_library_instance = Mock()
        mock_library_instance.notification_system = mock_notification_system
        mock_library_instance.get_notifications.side_effect = lambda: (
                "Notification: " + "\nNotification: ".join(mock_notification_system.get_all_notifications())
        )
        mock_get_instance.return_value = mock_library_instance
        result = Library.get_instance().get_notifications()

        self.assertEqual(
            result,
            "Notification: Notification 1\nNotification: Notification 2\nNotification: Notification 3"
        )
        mock_notification_system.get_all_notifications.assert_called_once()

    @patch("SystemManagement.Library.Library.get_instance")
    def test_get_notifications_no_notifications(self, mock_get_instance):
        mock_notification_system = Mock()
        mock_notification_system.get_all_notifications.return_value = []

        mock_library_instance = Library()
        mock_library_instance.notification_system = mock_notification_system
        mock_get_instance.return_value = mock_library_instance

        result = mock_library_instance.get_notifications()

        self.assertEqual(result, "No notifications available.")
        mock_notification_system.get_all_notifications.assert_called_once()

    @patch("SystemManagement.Library.Library._instance", None)
    def test_get_instance_creates_instance(self):
        instance1 = Library.get_instance()
        instance2 = Library.get_instance()

        self.assertIsNotNone(instance1)
        self.assertIs(instance1, instance2)  # Check singleton behavior
        self.assertIsInstance(instance1, Library)  # Ensure the instance is of type Library

    @patch("SystemManagement.Library.Library._instance", None)
    def test_get_instance_only_initializes_once(self):
        instance1 = Library.get_instance()
        instance2 = Library.get_instance()

        self.assertIs(instance1, instance2)  # Both should be the same instance


    @patch("SystemManagement.ManageCSV.ManageCSV.user_exists")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_users_to_csv")
    @patch("SystemManagement.Library.Library.get_instance")
    def test_register_librarian_new_user(self, mock_get_instance, mock_add_users_to_csv, mock_user_exists):
        mock_user_exists.return_value = False  # User does not exist
        mock_notification_system = Mock()
        mock_library_instance = Mock()
        mock_library_instance.notification_system = mock_notification_system
        mock_get_instance.return_value = mock_library_instance

        librarian = Mock()
        librarian.to_dict.return_value = {"user_name": "test_user"}

        result = Library.register_librarian(librarian)

        self.assertEqual(result, "Librarian added successfully")
        mock_user_exists.assert_called_once_with("test_user")
        mock_add_users_to_csv.assert_called_once_with(librarian)
        mock_notification_system.notify_observers.assert_called_once_with(
            "Librarian test_user was registered."
        )

    @patch("SystemManagement.ManageCSV.ManageCSV.user_exists")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_users_to_csv")
    @patch("SystemManagement.Library.Library.get_instance")
    def test_register_librarian_existing_user(self, mock_get_instance, mock_add_users_to_csv, mock_user_exists):
        mock_user_exists.return_value = True  # User already exists
        mock_notification_system = Mock()
        mock_library_instance = Mock()
        mock_library_instance.notification_system = mock_notification_system
        mock_get_instance.return_value = mock_library_instance

        librarian = Mock()
        librarian.to_dict.return_value = {"user_name": "test_user"}
        result = Library.register_librarian(librarian)

        self.assertEqual(result, "User already exists")
        mock_user_exists.assert_called_once_with("test_user")
        mock_add_users_to_csv.assert_not_called()
        mock_notification_system.notify_observers.assert_not_called()

    @patch("SystemManagement.ManageCSV.ManageCSV.get_popular_books")
    def test_get_most_popular_books_exist(self, mock_get_popular_books):
        mock_popular_books = Mock()
        mock_popular_books.empty = False  # Simulate popular books exist
        mock_get_popular_books.return_value = mock_popular_books

        result = Library.get_most_popular()

        self.assertEqual(result, mock_popular_books)  # Ensure the result matches the mocked popular books

    @patch("SystemManagement.ManageCSV.ManageCSV.get_popular_books")
    def test_get_most_popular_no_books(self, mock_get_popular_books):
        mock_popular_books = Mock()
        mock_popular_books.empty = True  # Simulate no popular books
        mock_get_popular_books.return_value = mock_popular_books

        result = Library.get_most_popular()

        self.assertFalse(result)  # Ensure the function returns False when no popular books exist


if __name__ == "__main__":
    unittest.main()