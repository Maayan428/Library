from symtable import Class
import csv

from werkzeug.security import check_password_hash, generate_password_hash

from SystemManagement.Book.FileCSV import FileCSV
import pandas as pd


class ManageCSV:


    @staticmethod
    def add_book_to_csv(filename, book):
        book_dict = book.to_dict()
        book_df = pd.DataFrame([book_dict])
        try:
            book_df.to_csv(filename, mode='a', index=False, encoding='utf-8',
                           header=not pd.io.common.file_exists(filename))
        except Exception as e:
            print(f"Error writing to {filename}: {e}")

    @staticmethod
    def add_new_book(book):
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
        filename=FileCSV.file_users.value
        user_dict= user.to_dict()
        user_df = pd.DataFrame([user_dict])
        try:
            user_df.to_csv(filename, mode='a', index=False, encoding='utf-8',
                           header=not pd.io.common.file_exists(filename))
        except Exception as e:
            print(f"Error writing to {filename}: {e}")

    @staticmethod
    def delete_user_from_csv(user):
        user_deleted = False
        filename=FileCSV.file_users.value
        df = pd.read_csv(filename)

        for index, row in df.iterrows():
            if not user_deleted and row["user_name"] == user.to_dict()["user_name"]:
                user_deleted = True
                df = df.drop(index)

        df.to_csv(filename, index=False, encoding='utf-8')


    @staticmethod
    def return_appearances(filename, book):
        df = pd.read_csv(filename)
        count = df[df["title"] == book.to_dict()["title"]].shape[0]
        return count

    @staticmethod
    def user_exists(user_name):
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
        book_deleted = False
        df = pd.read_csv(filename)

        for index, row in df.iterrows():
            if not book_deleted and row["title"] == book.to_dict()["title"]:
                book_deleted = True
                df = df.drop(index)

        df.to_csv(filename, index=False, encoding='utf-8')

    @staticmethod
    def add_to_parameter(filename, book, parameter):
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
        filename=FileCSV.file_book.value
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
        file_name = FileCSV.file_book.value
        top_n=10
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

