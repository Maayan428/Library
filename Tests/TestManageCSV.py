import json
import pickle
import unittest
from unittest.mock import patch, Mock
import pandas as pd
from werkzeug.security import generate_password_hash

from SystemManagement.Book.FactoryBook import FactoryBook
from SystemManagement.Book.FileCSV import FileCSV
from SystemManagement.ManageCSV import ManageCSV
from Subscriptions.Members import Members

class TestManageCSV(unittest.TestCase):

    @patch("pandas.DataFrame.to_csv")
    def test_add_book_to_csv_success(self, mock_to_csv):
        filename = "test_books.csv"
        book_mock = Mock()
        book_mock.to_dict.return_value = {
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Fiction",
            "year": 2025,
        }
        mock_to_csv.return_value = None  # Simulate successful CSV write
        ManageCSV.add_book_to_csv(filename, book_mock)
        mock_to_csv.assert_called_once_with(
            filename,
            mode='a',
            index=False,
            encoding='utf-8',
            header=not pd.io.common.file_exists(filename)
        )

    @patch("pandas.DataFrame.to_csv", side_effect=Exception("Test Exception"))
    @patch("builtins.print")
    def test_add_book_to_csv_failure(self, mock_print, mock_to_csv):
        filename = "test_books.csv"
        book_mock = Mock()
        book_mock.to_dict.return_value = {
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Fiction",
            "year": 2025,
        }
        ManageCSV.add_book_to_csv(filename, book_mock)
        mock_to_csv.assert_called_once_with(
            filename,
            mode='a',
            index=False,
            encoding='utf-8',
            header=not pd.io.common.file_exists(filename)
        )
        mock_print.assert_called_once_with(f"Error writing to {filename}: Test Exception")

    @patch("pandas.DataFrame.to_csv")
    def test_add_new_book_success(self, mock_to_csv):
        filename = FileCSV.file_book.value
        book = FactoryBook.create_book(
            title="New Book",
            author="New Author",
            is_loaned="No",
            copies=3,
            genre="Fantasy",
            year=2025
        )
        mock_to_csv.return_value = None  # Simulate successful CSV write
        ManageCSV.add_new_book(book)
        mock_to_csv.assert_called_once_with(
            filename,
            mode='a',
            index=False,
            encoding='utf-8',
            header=not pd.io.common.file_exists(filename)
        )

    @patch("pandas.DataFrame.to_csv", side_effect=Exception("Test Exception"))
    @patch("builtins.print")
    def test_add_new_book_failure(self, mock_print, mock_to_csv):
        filename = FileCSV.file_book.value
        book = FactoryBook.create_book(
            title="New Book",
            author="New Author",
            is_loaned="No",
            copies=3,
            genre="Fantasy",
            year=2025
        )
        ManageCSV.add_new_book(book)
        mock_to_csv.assert_called_once_with(
            filename,
            mode='a',
            index=False,
            encoding='utf-8',
            header=not pd.io.common.file_exists(filename)
        )
        mock_print.assert_called_once_with(f"Error writing to {filename}: Test Exception")

    @patch("pandas.read_csv")
    def test_return_appearances_book_exists(self, mock_read_csv):
        filename = "test_books.csv"
        book = Mock()
        book.to_dict.return_value = {"title": "Test Book"}

        mock_df = pd.DataFrame([
            {"title": "Test Book", "author": "Author 1"},
            {"title": "Test Book", "author": "Author 2"},
        ])
        mock_read_csv.return_value = mock_df
        result = ManageCSV.return_appearances(filename, book)

        self.assertEqual(result, 2)
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv")
    def test_return_appearances_book_not_exists(self, mock_read_csv):
        filename = "test_books.csv"
        book = Mock()
        book.to_dict.return_value = {"title": "Nonexistent Book"}

        mock_df = pd.DataFrame([
            {"title": "Other Book", "author": "Author 1"},
            {"title": "Another Book", "author": "Author 2"},
        ])
        mock_read_csv.return_value = mock_df
        result = ManageCSV.return_appearances(filename, book)

        self.assertEqual(result, 0)
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv")
    def test_user_exists_found(self, mock_read_csv):
        filename = FileCSV.file_users.value
        mock_df = pd.DataFrame([
            {"user_name": "existing_user", "other_column": "data"}
        ])
        mock_read_csv.return_value = mock_df

        result = ManageCSV.user_exists("existing_user")

        self.assertTrue(result)
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv")
    def test_user_exists_not_found(self, mock_read_csv):
        filename = FileCSV.file_users.value
        mock_df = pd.DataFrame([
            {"user_name": "other_user", "other_column": "data"}
        ])
        mock_read_csv.return_value = mock_df

        result = ManageCSV.user_exists("nonexistent_user")

        self.assertFalse(result)
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv", side_effect=FileNotFoundError)
    def test_user_exists_file_not_found(self, mock_read_csv):
        filename = FileCSV.file_users.value

        result = ManageCSV.user_exists("any_user")

        self.assertFalse(result)
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv", side_effect=KeyError("user_name"))
    def test_user_exists_key_error(self, mock_read_csv):
        filename = FileCSV.file_users.value

        result = ManageCSV.user_exists("any_user")

        self.assertFalse(result)
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_delete_book_from_csv_book_exists(self, mock_to_csv, mock_read_csv):
        filename = "test_books.csv"
        book_mock = Mock()
        book_mock.to_dict.return_value = {"title": "Test Book"}
        mock_df = pd.DataFrame([
            {"title": "Test Book", "author": "Author 1"},
            {"title": "Another Book", "author": "Author 2"}
        ])
        mock_read_csv.return_value = mock_df
        ManageCSV.delete_book_from_csv(filename, book_mock)

        updated_df = mock_df[mock_df["title"] != "Test Book"]
        mock_read_csv.assert_called_once_with(filename)
        mock_to_csv.assert_called_once_with(filename, index=False, encoding='utf-8')
        pd.testing.assert_frame_equal(mock_read_csv.return_value[mock_read_csv.return_value["title"] != "Test Book"],
                                      updated_df)

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_delete_book_from_csv_book_not_exists(self, mock_to_csv, mock_read_csv):
        filename = "test_books.csv"
        book_mock = Mock()
        book_mock.to_dict.return_value = {"title": "Nonexistent Book"}
        mock_df = pd.DataFrame([
            {"title": "Test Book", "author": "Author 1"},
            {"title": "Another Book", "author": "Author 2"}
        ])
        mock_read_csv.return_value = mock_df
        ManageCSV.delete_book_from_csv(filename, book_mock)
        mock_read_csv.assert_called_once_with(filename)
        mock_to_csv.assert_called_once_with(filename, index=False, encoding='utf-8')

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_add_to_parameter_success(self, mock_to_csv, mock_read_csv):
        filename = "test_books.csv"
        book_mock = Mock()
        book_mock.new_to_dict.return_value = {"title": "Test Book"}

        mock_df = pd.DataFrame([
            {"title": "Test Book", "requests": 5},
            {"title": "Another Book", "requests": 3}
        ])
        mock_read_csv.return_value = mock_df
        ManageCSV.add_to_parameter(filename, book_mock, "requests")
        updated_df = mock_df.copy()
        updated_df.loc[updated_df["title"] == "Test Book", "requests"] = 6

        mock_read_csv.assert_called_once_with(filename)
        mock_to_csv.assert_called_once_with(filename, index=False, encoding='utf-8')
        pd.testing.assert_frame_equal(mock_read_csv.return_value, updated_df)

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_add_to_parameter_invalid_value(self, mock_to_csv, mock_read_csv):
        filename = "test_books.csv"
        book_mock = Mock()
        book_mock.to_dict.return_value = {"title": "Test Book"}  # Simulate the book dictionary
        book_mock.new_to_dict.return_value = {"title": "Test Book"}  # Ensure compatibility with the function logic

        mock_df = pd.DataFrame([
            {"title": "Test Book", "requests": "invalid"},
            {"title": "Another Book", "requests": 3}
        ])
        mock_read_csv.return_value = mock_df
        with self.assertRaises(ValueError) as context:
            ManageCSV.add_to_parameter(filename, book_mock, "requests")

        self.assertIn("not a valid integer", str(context.exception))
        mock_read_csv.assert_called_once_with(filename)
        mock_to_csv.assert_not_called()

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_sub_from_parameter_success(self, mock_to_csv, mock_read_csv):
        filename = "test_books.csv"
        book_mock = Mock()
        book_mock.new_to_dict.return_value = {"title": "Test Book"}

        mock_df = pd.DataFrame([
            {"title": "Test Book", "requests": 5},
            {"title": "Another Book", "requests": 3}
        ])
        mock_read_csv.return_value = mock_df
        ManageCSV.sub_from_parameter(filename, book_mock, "requests")
        expected_df = pd.DataFrame([
            {"title": "Test Book", "requests": 4},
            {"title": "Another Book", "requests": 3}
        ])
        pd.testing.assert_frame_equal(mock_df, expected_df)
        mock_read_csv.assert_called_once_with(filename)
        mock_to_csv.assert_called_once_with(filename, index=False, encoding='utf-8')

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_update_is_loaned(self, mock_to_csv, mock_read_csv):
        filename = FileCSV.file_book.value
        book_mock = Mock()
        book_mock.to_dict.return_value = {"title": "Test Book"}

        mock_df = pd.DataFrame([
            {"title": "Test Book", "copies": 5, "currently_loaned": 5, "is_loaned": "No"},
            {"title": "Another Book", "copies": 3, "currently_loaned": 1, "is_loaned": "No"}
        ])
        mock_read_csv.return_value = mock_df
        ManageCSV.update_is_loaned(book_mock)
        expected_df = pd.DataFrame([
            {"title": "Test Book", "copies": 5, "currently_loaned": 5, "is_loaned": "Yes"},
            {"title": "Another Book", "copies": 3, "currently_loaned": 1, "is_loaned": "No"}
        ])
        pd.testing.assert_frame_equal(mock_df, expected_df)
        mock_read_csv.assert_called_once_with(filename)
        mock_to_csv.assert_called_once_with(filename, index=False, encoding='utf-8')

    @patch("pandas.read_csv")
    def test_get_value_books_success(self, mock_read_csv):
        filename = FileCSV.file_book.value
        book_mock = Mock()
        book_mock.new_to_dict.return_value = {"title": "Test Book"}

        mock_df = pd.DataFrame([
            {"title": "Test Book", "copies": 5, "currently_loaned": 2},
            {"title": "Another Book", "copies": 3, "currently_loaned": 1}
        ])
        mock_read_csv.return_value = mock_df
        result = ManageCSV.get_value_books(book_mock, "copies")
        self.assertEqual(result, 5)  # Expected value for "copies" column
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv")
    def test_get_value_books_column_not_found(self, mock_read_csv):
        filename = FileCSV.file_book.value
        book_mock = Mock()
        book_mock.new_to_dict.return_value = {"title": "Test Book"}

        mock_df = pd.DataFrame([
            {"title": "Test Book", "currently_loaned": 2},
            {"title": "Another Book", "currently_loaned": 1}
        ])
        mock_read_csv.return_value = mock_df
        with self.assertRaises(KeyError):
            ManageCSV.get_value_books(book_mock, "copies")
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv")
    def test_get_value_books_book_not_found(self, mock_read_csv):
        filename = FileCSV.file_book.value
        book_mock = Mock()
        book_mock.new_to_dict.return_value = {"title": "Nonexistent Book"}

        mock_df = pd.DataFrame([
            {"title": "Test Book", "copies": 5, "currently_loaned": 2},
            {"title": "Another Book", "copies": 3, "currently_loaned": 1}
        ])
        mock_read_csv.return_value = mock_df
        with self.assertRaises(IndexError):
            ManageCSV.get_value_books(book_mock, "copies")
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv")
    def test_log_in_librarian_success(self, mock_read_csv):
        filename = FileCSV.file_users.value
        hashed_password = generate_password_hash("password123")
        mock_df = pd.DataFrame([
            {"user_name": "test_user", "password": hashed_password}
        ])
        mock_read_csv.return_value = mock_df
        result = ManageCSV.log_in_librarian("test_user", "password123")
        self.assertEqual(result, "Login successful")
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv")
    def test_log_in_librarian_invalid_password(self, mock_read_csv):
        filename = FileCSV.file_users.value
        hashed_password = generate_password_hash("password123")
        mock_df = pd.DataFrame([
            {"user_name": "test_user", "password": hashed_password}
        ])
        mock_read_csv.return_value = mock_df
        result = ManageCSV.log_in_librarian("test_user", "wrong_password")
        self.assertEqual(result, "Invalid password")
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv")
    def test_log_in_librarian_user_not_found(self, mock_read_csv):
        filename = FileCSV.file_users.value
        mock_df = pd.DataFrame([
            {"user_name": "another_user", "password": generate_password_hash("password123")}
        ])
        mock_read_csv.return_value = mock_df
        result = ManageCSV.log_in_librarian("test_user", "password123")
        self.assertEqual(result, "Username not found")
        mock_read_csv.assert_called_once_with(filename)

    @patch("pandas.read_csv")
    def test_get_popular_books_success(self, mock_read_csv):
        file_name = FileCSV.file_book.value
        mock_df = pd.DataFrame([
            {"title": "Book 1", "requests": 15},
            {"title": "Book 2", "requests": 20},
            {"title": "Book 3", "requests": 5},
            {"title": "Book 4", "requests": 25}
        ])
        mock_read_csv.return_value = mock_df
        result = ManageCSV.get_popular_books()
        expected_df = mock_df[mock_df["requests"] >= 10].sort_values(by="requests", ascending=False).head(10)
        pd.testing.assert_frame_equal(result, expected_df)
        mock_read_csv.assert_called_once_with(file_name)

    @patch("pandas.read_csv")
    def test_get_popular_books_empty_dataframe(self, mock_read_csv):
        file_name = FileCSV.file_book.value
        mock_df = pd.DataFrame(columns=["title", "requests"])
        mock_read_csv.return_value = mock_df

        result = ManageCSV.get_popular_books()
        self.assertTrue(result.empty)
        mock_read_csv.assert_called_once_with(file_name)

    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_add_to_waiting_list(self, mock_read_csv, mock_to_csv):
        # Arrange
        file_name = FileCSV.file_book.value
        book_title = "Test Book"
        member_mock = Members(name="Test Member", phone_number="00000")  # Member as object

        # Simulate initial data with an empty waiting list
        initial_data = pd.DataFrame({
            "title": ["Test Book"],
            "waiting_list": [str(pickle.dumps([]))]
        })
        mock_read_csv.return_value = initial_data

        updated_data = pd.DataFrame({
            "title": ["Test Book"],
            "waiting_list": [str(pickle.dumps([member_mock]))]
        })

        # Mock the DataFrame that would be passed to to_csv
        def mock_to_csv_side_effect(df, *args, **kwargs):
            # Assert DataFrame was updated correctly before being written
            pd.testing.assert_frame_equal(df, updated_data)

        mock_to_csv.side_effect = mock_to_csv_side_effect

        # Act
        ManageCSV.add_to_waiting_list(book_title, member_mock)

        # Assert
        mock_read_csv.assert_called_once_with(file_name)
        mock_to_csv.assert_called_once()
        print("Test passed: Member added to waiting list.")



if __name__ == "__main__":
    unittest.main()