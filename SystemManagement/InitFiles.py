import pickle
from symtable import Class
import csv
from SystemManagement.Book.FileCSV import FileCSV
import pandas as pd


class InitFiles:
    @staticmethod
    def init_books_csv():
        """
        Initializes the books.csv file.
        - If the file does not exist, it creates a new file with default headers.
        - Ensures required columns ('is_loaned', 'requests', 'currently_loaned', 'copies') exist.
        - Initializes 'requests' and 'currently_loaned' columns based on the 'is_loaned' column.
        """
        try:
            file_name = FileCSV.file_book.value
            try:
                df = pd.read_csv(file_name)
            except FileNotFoundError:
                # Create a new file if not found
                headers = ["title", "author", "is_loaned", "copies", "genre", "year", "requests", "currently_loaned"]
                df = pd.DataFrame(columns=headers)
                df.to_csv(file_name, index=False)
                print(f"{file_name} was not found. A new file was created with the necessary headers.")
                return
            required_columns = {"is_loaned", "requests", "currently_loaned", "copies"}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Missing one or more required columns: {required_columns - set(df.columns)}")
            # Initialize 'requests' and 'currently_loaned'
            df["requests"] = df.apply(
                lambda row: 0 if row["is_loaned"] == "No" else row["copies"], axis=1
            )
            df["currently_loaned"] = df.apply(
                lambda row: 0 if row["is_loaned"] == "No" else row["copies"], axis=1
            )
            df.to_csv(file_name, index=False)
            print("books.csv file initialized successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def ensure_required_columns():
        """
        Ensures that the required columns ('requests', 'currently_loaned') exist in the books.csv file.
        - If missing, adds the columns with default None values.
        """
        file_name = FileCSV.file_book.value
        try:
            df = pd.read_csv(file_name)
            required_columns = ["requests", "currently_loaned"]
            for column in required_columns:
                if column not in df.columns:
                    df[column] = None
                    print(f"Added missing column: '{column}'.")
            df.to_csv(file_name, index=False, encoding="utf-8")
            print(f"Required columns ensured successfully in {file_name}.")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def initialize_waiting_list():
        """
        Initializes the 'waiting_list' column in books.csv.
        - If the column does not exist, adds it with empty lists.
        - If the column exists, resets all values to empty lists.
        """
        file_name = FileCSV.file_book.value
        try:
            df = pd.read_csv(file_name)
            if "waiting_list" not in df.columns:
                df["waiting_list"] = [str(pickle.dumps([])) for _ in range(len(df))]
                print("Added 'waiting_list' column with empty lists.")
            else:
                df["waiting_list"] = [str(pickle.dumps([])) for _ in range(len(df))]
                print("Reset 'waiting_list' column to empty lists.")
            df.to_csv(file_name, index=False, encoding="utf-8")
            print(f"'waiting_list' column initialized successfully in {file_name}.")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def initialize_csv_files():
        """
        Creates empty CSV files for loaned_books.csv and available_books.csv.
        - Each file is initialized with the headers: 'title', 'author', 'genre', 'year'.
        """
        headers = ["title", "author", "genre", "year"]
        for file in [FileCSV.file_loaned.value, FileCSV.file_available.value]:
            try:
                df = pd.DataFrame(columns=headers)
                df.to_csv(file, index=False)
                print(f"File '{file}' initialized successfully.")
            except Exception as e:
                print(f"An error occurred while initializing file '{file}': {e}")

    @staticmethod
    def sort_books():
        """
        Sorts books into loaned_books.csv and available_books.csv based on their 'is_loaned' status.
        - Books with 'is_loaned' = 'Yes' are written to loaned_books.csv.
        - Books with 'is_loaned' = 'No' are written to available_books.csv.
        - The number of rows reflects the number of copies.
        """
        try:
            file_name = FileCSV.file_book.value
            df_books = pd.read_csv(file_name)
            required_columns = {"title", "author", "genre", "year", "is_loaned", "copies"}
            if not required_columns.issubset(df_books.columns):
                raise ValueError(f"Missing required columns: {required_columns - set(df_books.columns)}")
            # Filters and repeats rows based on copies
            loaned_books = df_books[df_books["is_loaned"] == "Yes"].loc[:, ["title", "author", "genre", "year"]]
            available_books = df_books[df_books["is_loaned"] == "No"].loc[:, ["title", "author", "genre", "year"]]
            loaned_books = loaned_books.loc[loaned_books.index.repeat(df_books.loc[loaned_books.index, "copies"])]
            available_books = available_books.loc[
                available_books.index.repeat(df_books.loc[available_books.index, "copies"])]
            # Save to files
            loaned_books.to_csv(FileCSV.file_loaned.value, index=False)
            available_books.to_csv(FileCSV.file_available.value, index=False)
            print("Books distributed successfully into loaned_books.csv and available_books.csv.")
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def init_users_csv():
        """
        Initializes the users.csv file.
        - If the file does not exist, it creates a new file with default headers.
        - Ensures the required columns ('first_name', 'last_name', 'user_name', 'password') exist.
        """
        try:
            file_name = FileCSV.file_users.value
            try:
                df = pd.read_csv(file_name)
            except FileNotFoundError:
                # Create a new file if not found
                headers = ["first_name", "last_name", "user_name", "password"]
                df = pd.DataFrame(columns=headers)
                df.to_csv(file_name, index=False)
                print(f"{file_name} was not found. A new file was created with the necessary headers.")
                return
            required_columns = {"first_name", "last_name", "user_name", "password"}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Missing one or more required columns: {required_columns - set(df.columns)}")
            df.to_csv(file_name, index=False)
            print("users.csv file initialized successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")