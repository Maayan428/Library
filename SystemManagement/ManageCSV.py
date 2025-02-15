import pickle
from symtable import Class
import csv

from werkzeug.security import check_password_hash, generate_password_hash
from SystemManagement.Book.FileCSV import FileCSV
import pandas as pd


class ManageCSV:
    """
    Class for managing CSV operations related to books, users, and library functionalities.
    """

    @staticmethod
    def add_book_to_csv(filename, book):
        """
        Appends a book's details to the specified CSV file.

        Args:
            filename (str): The path to the CSV file.
            book: A book object with details to be added.
        """
        book_dict = book.to_dict()
        book_df = pd.DataFrame([book_dict])
        try:
            book_df.to_csv(filename, mode='a', index=False, encoding='utf-8',
                           header=not pd.io.common.file_exists(filename))
        except Exception as e:
            print(f"Error writing to {filename}: {e}")

    @staticmethod
    def add_new_book(book):
        """
        Adds a new book to the main books CSV file.

        Args:
            book: A book object with details to be added.
        """
        book_filename = FileCSV.file_book.value
        book_dict = book.new_to_dict()
        book_df = pd.DataFrame([book_dict])
        try:
            book_df.to_csv(book_filename, mode='a', index=False, encoding='utf-8',
                           header=not pd.io.common.file_exists(book_filename))
        except Exception as e:
            print(f"Error writing to {book_filename}: {e}")

    @staticmethod
    def add_users_to_csv(user):
        """
        Appends a user's details to the users CSV file.

        Args:
            user: A user object with details to be added.
        """
        filename = FileCSV.file_users.value
        user_dict = user.to_dict()
        user_df = pd.DataFrame([user_dict])
        try:
            user_df.to_csv(filename, mode='a', index=False, encoding='utf-8',
                           header=not pd.io.common.file_exists(filename))
        except Exception as e:
            print(f"Error writing to {filename}: {e}")

    @staticmethod
    def delete_user_from_csv(user):
        """
        Deletes a user from the users CSV file.

        Args:
            user: A user object to be removed.
        """
        user_deleted = False
        filename = FileCSV.file_users.value
        df = pd.read_csv(filename)

        for index, row in df.iterrows():
            if not user_deleted and row["user_name"] == user.to_dict()["user_name"]:
                user_deleted = True
                df = df.drop(index)

        df.to_csv(filename, index=False, encoding='utf-8')

    @staticmethod
    def return_appearances(filename, book):
        """
        Counts the number of appearances of a specific book in the CSV file.

        Args:
            filename (str): The path to the CSV file.
            book: The book object to search for.

        Returns:
            int: Number of appearances of the book.
        """
        df = pd.read_csv(filename)
        count = df[df['title'] == book.to_dict()['title']].shape[0]
        return count

    @staticmethod
    def user_exists(user_name):
        """
        Checks if a user exists in the users CSV file.

        Args:
            user_name (str): The username to search for.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        filename = FileCSV.file_users.value
        try:
            df = pd.read_csv(filename)
            df.columns = df.columns.str.strip()
            df["user_name"] = df["user_name"].astype(str).str.strip()
            return not df[df["user_name"] == user_name].empty
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return False
        except KeyError as e:
            print(f"Error: Column not found in file - {str(e)}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return False

    @staticmethod
    def delete_book_from_csv(filename, book):
        """
        Deletes a specific book from a CSV file.

        Args:
            filename (str): The path to the CSV file.
            book: The book object to be removed.
        """
        book_deleted = False
        df = pd.read_csv(filename)

        for index, row in df.iterrows():
            if not book_deleted and row["title"] == book.to_dict()["title"]:
                book_deleted = True
                df = df.drop(index)

        df.to_csv(filename, index=False, encoding='utf-8')

    @staticmethod
    def add_to_parameter(filename, book, parameter):
        """
        Increments the value of a specified parameter for a book in the CSV file.

        Args:
            filename (str): The path to the CSV file.
            book: The book object.
            parameter (str): The parameter to update.
        """
        df = pd.read_csv(filename)
        current_value = df.loc[df["title"] == book.new_to_dict()["title"], parameter].iloc[0]
        try:
            current_value_int = int(current_value)
            new_value = current_value_int + 1
            df.loc[df["title"] == book.new_to_dict()["title"], parameter] = new_value
        except ValueError:
            raise ValueError(
                f"The value of '{parameter}' for the book '{book.to_dict()['title']}' is not a valid integer.")

        df.to_csv(filename, index=False, encoding='utf-8')

    @staticmethod
    def sub_from_parameter(filename, book, parameter):
        """
        Decreases the value of a specified parameter for a book in the CSV file.

        Args:
            filename (str): The path to the CSV file.
            book: The book object.
            parameter (str): The parameter to update.
        """
        df = pd.read_csv(filename)
        current_value = df.loc[df["title"] == book.new_to_dict()["title"], parameter].iloc[0]
        try:
            current_value_int = int(current_value)
            new_value = current_value_int - 1
            df.loc[df["title"] == book.new_to_dict()["title"], parameter] = new_value
        except ValueError:
            raise ValueError(
                f"The value of '{parameter}' for the book '{book.to_dict()['title']}' is not a valid integer.")
        df.to_csv(filename, index=False, encoding='utf-8')

    @staticmethod
    def update_is_loaned(book):
        """
        Updates the 'is_loaned' status for a book in the CSV file based on the copies loaned.

        Args:
            book: The book object.
        """
        filename = FileCSV.file_book.value
        df = pd.read_csv(filename)
        condition = df["title"] == book.to_dict()["title"]
        if df.loc[condition, "copies"].iloc[0] == df.loc[condition, "currently_loaned"].iloc[0]:
            df.loc[condition, "is_loaned"] = "Yes"
        else:
            df.loc[condition, "is_loaned"] = "No"
        df.to_csv(filename, index=False, encoding='utf-8')

    @staticmethod
    def get_value_books(book, column):
        filename = FileCSV.file_book.value
        df = pd.read_csv(filename)
        value = df.loc[df["title"] == book.new_to_dict()["title"], column].iloc[0]
        return value

    @staticmethod
    def get_value_other(filename, book, column):
        df = pd.read_csv(filename, encoding='utf-8-sig')
        value = df.loc[df["title"] == book.to_dict()["title"], column].iloc[0]
        return value

    @staticmethod
    def log_in_librarian(user_name, password):
        """
        Validates the login credentials for a librarian.

        Args:
            user_name (str): The username entered by the librarian.
            password (str): The password entered by the librarian.

        Returns:
            str: A message indicating the result of the login attempt ("Login successful", "Invalid password", etc.).
        """
        filename = FileCSV.file_users.value
        try:
            df = pd.read_csv(filename)
            df.columns = df.columns.str.strip()
            df["user_name"] = df["user_name"].astype(str).str.strip()
            df["password"] = df["password"].astype(str).str.strip()

            user_row = df[df["user_name"] == user_name]

            if not user_row.empty:
                stored_password_hash = user_row.iloc[0]["password"]
                if check_password_hash(stored_password_hash, password):
                    return "Login successful"
                else:
                    return "Invalid password"
            else:
                return "Username not found"
        except FileNotFoundError:
            return "Error: User file not found"
        except KeyError as e:
            return f"Error: Column not found in file - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def get_popular_books():
        """
        Retrieves the most popular books based on the number of requests.

        Returns:
            DataFrame: A DataFrame containing the top N popular books, sorted by request count.
        """
        file_name = FileCSV.file_book.value
        top_n = 10
        min_requests = 10
        try:
            df = pd.read_csv(file_name)
            if "requests" not in df.columns:
                raise ValueError("The column 'requests' does not exist in the CSV file.")
            df["requests"] = pd.to_numeric(df["requests"], errors="coerce").fillna(0)
            filtered_df = df[df["requests"] >= min_requests]
            sorted_df = filtered_df.sort_values(by="requests", ascending=False)
            return sorted_df.head(top_n)
        except FileNotFoundError:
            print("Error: File not found.")
        except Exception as e:
            print(f"Error: {str(e)}")

    @staticmethod
    def add_to_waiting_list(book_title, member):
        """
        Adds a member to the waiting list for a specific book.

        Args:
            book_title (str): The title of the book.
            member: The member to be added to the waiting list.
        """
        file_name = FileCSV.file_book.value
        try:
            df = pd.read_csv(file_name)
            if "waiting_list" not in df.columns:
                raise ValueError("The column 'waiting_list' does not exist in the CSV file.")

            condition = df["title"] == book_title
            if condition.sum() == 0:
                raise ValueError(f"Book '{book_title}' not found.")

            waiting_list = df.loc[condition, "waiting_list"].iloc[0]

            if pd.isna(waiting_list) or waiting_list == "":
                waiting_list = []
            else:
                waiting_list = pickle.loads(eval(waiting_list))
            waiting_list.append(member)
            df.loc[condition, "waiting_list"] = str(pickle.dumps(waiting_list))

            df.to_csv(file_name, index=False, encoding="utf-8")
            print(f"Member {member.name} added to the waiting list for book '{book_title}'.")
        except Exception as e:
            print(f"Error: {str(e)}")

    @staticmethod
    def pop_from_waiting_list(book_title):
        """
        Removes the first member from the waiting list for a specific book and returns the member.

        Args:
            book_title (str): The title of the book.

        Returns:
            member: The first member from the waiting list or None if the list is empty.
        """
        file_name = FileCSV.file_book.value
        try:
            df = pd.read_csv(file_name)
            if "waiting_list" not in df.columns:
                raise ValueError("The column 'waiting_list' does not exist in the CSV file.")

            condition = df["title"] == book_title
            if condition.sum() == 0:
                raise ValueError(f"Book '{book_title}' not found.")

            waiting_list_serialized = df.loc[condition, "waiting_list"].iloc[0]

            if pd.isna(waiting_list_serialized) or waiting_list_serialized == "":
                print(f"No members in the waiting list for book '{book_title}'.")
                return None

            waiting_list = pickle.loads(eval(waiting_list_serialized))

            if not waiting_list:
                print(f"No members in the waiting list for book '{book_title}'.")
                return None

            first_member = waiting_list.pop(0)
            df.loc[condition, "waiting_list"] = str(pickle.dumps(waiting_list))
            df.to_csv(file_name, index=False, encoding="utf-8")
            print(f"Member {first_member.to_dict()['name']} removed from the waiting list for book '{book_title}'.")
            return first_member
        except Exception as e:
            print(f"Error: {str(e)}")
            return None