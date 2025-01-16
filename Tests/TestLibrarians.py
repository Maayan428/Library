from unittest.mock import patch, Mock
import unittest
from SystemManagement.Librarians import Librarians
from SystemManagement.ManageCSV import ManageCSV
from SystemManagement.Book.FileCSV import FileCSV
from SystemManagement.Library import Library

class TestLibrarians(unittest.TestCase):

    @patch("SystemManagement.ManageCSV.ManageCSV.return_appearances")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_new_book")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_book_to_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.get_value_books")
    @patch("SystemManagement.Library.Library.get_instance")
    def test_add_new_book_new_book(
            self,
            mock_get_instance,
            mock_get_value_books,
            mock_add_book_to_csv,
            mock_add_new_book,
            mock_return_appearances,
    ):
        mock_notification_system = Mock()
        mock_get_instance.return_value.notification_system = mock_notification_system
        mock_return_appearances.return_value = 0
        mock_get_value_books.side_effect = lambda book, field: {"is_loaned": "No", "copies": 2}.get(field)
        book = Mock()
        book.to_dict.return_value = {"title": "Test Book", "author": "Author Name"}

        Librarians.add_new_book(book)

        mock_add_new_book.assert_called_once_with(book)
        mock_get_value_books.assert_any_call(book, "is_loaned")
        self.assertEqual(mock_add_book_to_csv.call_count, 2)
        mock_add_book_to_csv.assert_any_call(FileCSV.file_available.value, book)

    @patch("SystemManagement.ManageCSV.ManageCSV.add_to_parameter")
    @patch("SystemManagement.ManageCSV.ManageCSV.update_is_loaned")
    @patch("SystemManagement.ManageCSV.ManageCSV.return_appearances")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_new_book")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_book_to_csv")
    @patch("SystemManagement.Library.Library.get_instance")
    def test_add_new_book_existing_book(
            self,
            mock_get_instance,
            mock_add_book_to_csv,
            mock_add_new_book,
            mock_return_appearances,
            mock_update_is_loaned,
            mock_add_to_parameter
    ):
        mock_notification_system = Mock()
        mock_get_instance.return_value.notification_system = mock_notification_system
        mock_return_appearances.return_value = 1
        book = Mock()
        book.to_dict.return_value = {"title": "Test Book", "author": "Author Name", "copies": 2}

        Librarians.add_new_book(book)

        mock_add_to_parameter.assert_called_once_with(FileCSV.file_book.value, book, "copies")
        mock_update_is_loaned.assert_called_once_with(book)
        mock_add_new_book.assert_not_called()
        self.assertEqual(mock_add_book_to_csv.call_count, 1)
        mock_add_book_to_csv.assert_called_once_with(FileCSV.file_available.value,book)

    @patch("SystemManagement.ManageCSV.ManageCSV.delete_book_from_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.sub_from_parameter")
    @patch("SystemManagement.ManageCSV.ManageCSV.get_value_books")
    @patch("SystemManagement.ManageCSV.ManageCSV.return_appearances")
    @patch("SystemManagement.Library.Library.get_instance")
    def test_remove_book(
            self,
            mock_get_instance,
            mock_return_appearances,
            mock_get_value_books,
            mock_sub_from_parameter,
            mock_delete_book_from_csv
    ):
        # Mock setup
        mock_notification_system = Mock()
        mock_get_instance.return_value.notification_system = mock_notification_system

        book = Mock()
        book.to_dict.return_value = {"title": "Test Book", "author": "Author Name", "copies": 2}

        # Case 1: Book does not exist
        mock_return_appearances.return_value = 0
        result = Librarians.remove_book(book)
        mock_return_appearances.assert_called_once_with(FileCSV.file_book.value, book)
        self.assertEqual(result, None)
        mock_delete_book_from_csv.assert_not_called()
        mock_sub_from_parameter.assert_not_called()
        mock_notification_system.notify_observers.assert_not_called()

        # Reset mocks for the next case
        mock_return_appearances.reset_mock()
        mock_get_value_books.reset_mock()
        mock_delete_book_from_csv.reset_mock()
        mock_sub_from_parameter.reset_mock()
        mock_notification_system.notify_observers.reset_mock()

        # Case 2: All copies are loaned
        mock_return_appearances.return_value = 1
        mock_get_value_books.side_effect = lambda book, field: {"copies": 2, "currently_loaned": 2}[field]
        result = Librarians.remove_book(book)
        mock_get_value_books.assert_any_call(book, "copies")
        mock_get_value_books.assert_any_call(book, "currently_loaned")
        self.assertEqual(result, False)  # All books loaned, should return False
        mock_delete_book_from_csv.assert_not_called()
        mock_sub_from_parameter.assert_not_called()
        mock_notification_system.notify_observers.assert_not_called()

        # Reset mocks for the next case
        mock_return_appearances.reset_mock()
        mock_get_value_books.reset_mock()
        mock_delete_book_from_csv.reset_mock()
        mock_sub_from_parameter.reset_mock()
        mock_notification_system.notify_observers.reset_mock()

        # Case 3: Book exists and copies are available
        mock_return_appearances.return_value = 1
        mock_get_value_books.side_effect = lambda book, field: {"copies": 2, "currently_loaned": 1}[field]
        result = Librarians.remove_book(book)
        mock_get_value_books.assert_any_call(book, "copies")
        mock_get_value_books.assert_any_call(book, "currently_loaned")
        self.assertEqual(result, True)
        mock_sub_from_parameter.assert_called_once_with(FileCSV.file_book.value, book, "copies")
        mock_delete_book_from_csv.assert_called_once_with(FileCSV.file_available.value, book)
        mock_notification_system.notify_observers.assert_called_once_with(
            f"The book: {book.to_dict()['title']} has been removed from the library"
        )

    @patch("SystemManagement.ManageCSV.ManageCSV.add_to_waiting_list")
    @patch("SystemManagement.ManageCSV.ManageCSV.update_is_loaned")
    @patch("SystemManagement.ManageCSV.ManageCSV.delete_book_from_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_book_to_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.return_appearances")
    def test_lend_book_not_found(
            self,
            mock_return_appearances,
            mock_add_book_to_csv,
            mock_delete_book_from_csv,
            mock_update_is_loaned,
            mock_add_to_waiting_list
    ):
        book = Mock()
        book.to_dict.return_value = {"title": "Test Book"}
        member = Mock()
        member.to_dict.return_value = {"name": "Test Member"}

        mock_return_appearances.return_value = 0
        result = Librarians.lend_book_to_member(member, book)
        self.assertIsNone(result)
        mock_add_to_waiting_list.assert_not_called()
        mock_add_book_to_csv.assert_not_called()
        mock_delete_book_from_csv.assert_not_called()
        mock_update_is_loaned.assert_not_called()

    @patch("SystemManagement.ManageCSV.ManageCSV.add_to_waiting_list")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_to_parameter")
    @patch("SystemManagement.ManageCSV.ManageCSV.update_is_loaned")
    @patch("SystemManagement.ManageCSV.ManageCSV.delete_book_from_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_book_to_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.get_value_books")
    @patch("SystemManagement.ManageCSV.ManageCSV.return_appearances")
    def test_lend_book_available(
            self,
            mock_return_appearances,
            mock_get_value_books,
            mock_add_book_to_csv,
            mock_delete_book_from_csv,
            mock_update_is_loaned,
            mock_add_to_parameter,
            mock_add_to_waiting_list
    ):
        # Arrange
        book = Mock()
        book.to_dict.return_value = {"title": "Test Book"}
        member = Mock()
        member.to_dict.return_value = {"name": "Test Member"}

        mock_return_appearances.return_value = 1
        mock_get_value_books.side_effect = lambda b, field: {"is_loaned": "No", "copies": 1}[field]

        # Act
        result = Librarians.lend_book_to_member(member, book)

        # Assert
        self.assertTrue(result)
        mock_add_to_parameter.assert_has_calls([
            unittest.mock.call(FileCSV.file_book.value, book, "requests"),
            unittest.mock.call(FileCSV.file_book.value, book, "currently_loaned")
        ], any_order=False)
        mock_delete_book_from_csv.assert_called_once_with(FileCSV.file_available.value, book)
        mock_add_book_to_csv.assert_called_once_with(FileCSV.file_loaned.value, book)
        mock_update_is_loaned.assert_called_once_with(book)
        mock_add_to_waiting_list.assert_not_called()

    @patch("SystemManagement.ManageCSV.ManageCSV.add_to_waiting_list")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_to_parameter")
    @patch("SystemManagement.ManageCSV.ManageCSV.update_is_loaned")
    @patch("SystemManagement.ManageCSV.ManageCSV.delete_book_from_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_book_to_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.get_value_books")
    @patch("SystemManagement.ManageCSV.ManageCSV.return_appearances")
    @patch("SystemManagement.Library.Library.get_instance")
    def test_lend_book_loaned(
            self,
            mock_get_instance,
            mock_return_appearances,
            mock_get_value_books,
            mock_add_book_to_csv,
            mock_delete_book_from_csv,
            mock_update_is_loaned,
            mock_add_to_parameter,
            mock_add_to_waiting_list
    ):
        # Arrange
        book = Mock()
        book.to_dict.return_value = {"title": "Test Book"}
        member = Mock()
        member.to_dict.return_value = {"name": "Test Member"}

        mock_return_appearances.return_value = 1
        mock_get_value_books.side_effect = lambda b, field: {"is_loaned": "Yes", "copies": 1}[field]

        # Act
        result = Librarians.lend_book_to_member(member, book)

        # Assert
        self.assertFalse(result)
        mock_add_to_parameter.assert_called_with(FileCSV.file_book.value, book, "requests")
        mock_add_to_waiting_list.assert_called_once_with("Test Book", member)
        mock_get_instance.return_value.notification_system.notify_observers.assert_called_once_with(
            "Member: Test Member added to the waiting list of the book: Test Book"
        )
        mock_delete_book_from_csv.assert_not_called()
        mock_add_book_to_csv.assert_not_called()
        mock_update_is_loaned.assert_not_called()

    @patch("SystemManagement.ManageCSV.ManageCSV.return_appearances", return_value=0)
    def test_return_book_not_found(self, mock_return_appearances):
        # Arrange
        book = Mock()
        book.to_dict.return_value = {"title": "Test Book"}

        # Act
        result = Librarians.return_book_to_library(book)

        # Assert
        self.assertEqual(result, 0)
        mock_return_appearances.assert_called_once_with(FileCSV.file_loaned.value, book)

    @patch("SystemManagement.ManageCSV.ManageCSV.pop_from_waiting_list", return_value=None)
    @patch("SystemManagement.ManageCSV.ManageCSV.update_is_loaned")
    @patch("SystemManagement.ManageCSV.ManageCSV.sub_from_parameter")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_book_to_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.delete_book_from_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.return_appearances", return_value=1)
    def test_return_book_no_waiting_list(
            self, mock_return_appearances, mock_delete_book_from_csv,
            mock_add_book_to_csv, mock_sub_from_parameter, mock_update_is_loaned,
            mock_pop_from_waiting_list):
        # Arrange
        book = Mock()
        book.to_dict.return_value = {"title": "Test Book"}

        # Act
        result = Librarians.return_book_to_library(book)

        # Assert
        self.assertEqual(result, 2)
        mock_return_appearances.assert_called_once_with(FileCSV.file_loaned.value, book)
        mock_delete_book_from_csv.assert_called_once_with(FileCSV.file_loaned.value, book)
        mock_add_book_to_csv.assert_called_once_with(FileCSV.file_available.value, book)
        mock_sub_from_parameter.assert_called_once_with(FileCSV.file_book.value, book, "currently_loaned")
        mock_update_is_loaned.assert_called_once_with(book)
        mock_pop_from_waiting_list.assert_called_once_with("Test Book")

    @patch("SystemManagement.Librarians.Librarians.lend_book_to_member")
    @patch("SystemManagement.Library.Library.get_instance")
    @patch("SystemManagement.ManageCSV.ManageCSV.pop_from_waiting_list")
    @patch("SystemManagement.ManageCSV.ManageCSV.update_is_loaned")
    @patch("SystemManagement.ManageCSV.ManageCSV.sub_from_parameter")
    @patch("SystemManagement.ManageCSV.ManageCSV.add_book_to_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.delete_book_from_csv")
    @patch("SystemManagement.ManageCSV.ManageCSV.return_appearances", return_value=1)
    def test_return_book_with_waiting_list(
            self, mock_return_appearances, mock_delete_book_from_csv,
            mock_add_book_to_csv, mock_sub_from_parameter, mock_update_is_loaned,
            mock_pop_from_waiting_list, mock_get_instance, mock_lend_book_to_member):
        # Arrange
        mock_notification_system = Mock()
        mock_get_instance.return_value.notification_system = mock_notification_system
        person = Mock()
        person.to_dict.return_value = {"name": "John Doe", "phone_number": "123456789"}
        mock_pop_from_waiting_list.return_value = person

        book = Mock()
        book.to_dict.return_value = {"title": "Test Book"}

        # Act
        result = Librarians.return_book_to_library(book)

        # Assert
        self.assertEqual(result, 1)
        mock_return_appearances.assert_called_once_with(FileCSV.file_loaned.value, book)
        mock_delete_book_from_csv.assert_called_once_with(FileCSV.file_loaned.value, book)
        mock_add_book_to_csv.assert_called_once_with(FileCSV.file_available.value, book)
        mock_sub_from_parameter.assert_called_once_with(FileCSV.file_book.value, book, "currently_loaned")
        mock_update_is_loaned.assert_called_once_with(book)
        mock_pop_from_waiting_list.assert_called_once_with("Test Book")
        mock_notification_system.notify_observers.assert_called_once_with(
            "The book: Test Book has been returned.\n"
            " Member: John Doe is waiting for it:) \n Notify at: 123456789"
        )
        mock_lend_book_to_member.assert_called_once_with(person, book)


if __name__ == "__main__":
    unittest.main()