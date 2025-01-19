import tkinter as tk
from tkinter import ttk
import pandas as pd
import logging
from SystemManagement.Logger import Logger
from SystemManagement.Book.FileCSV import FileCSV
from Subscriptions.Members import Members
from SystemManagement.Book.Book import Book
from SystemManagement.Librarians import Librarians
from SystemManagement.Book.FactoryBook import FactoryBook
from SystemManagement.Library import Library
from SystemManagement.ManageCSV import ManageCSV
from SystemManagement.Book.BookGenre import BookGenre

welcome_page = tk.Tk()
welcome_page.geometry("1500x1000")
welcome_page.title("Welcome to the E&M Library")
welcome_page.configure(bg='#ffe6f0')

log_in_page = tk.Toplevel(welcome_page)
log_in_page.geometry("1500x1000")
log_in_page.title("E&M Library")
log_in_page.configure(bg='white')
log_in_page.withdraw()

home_page = tk.Toplevel(log_in_page)
home_page.geometry("1500x1000")
home_page.title("E&M Home Page")
home_page.configure(bg='white')
home_page.withdraw()

sign_in_page = tk.Toplevel(log_in_page)
sign_in_page.geometry("1500x1000")
sign_in_page.title("E&M Home Page")
sign_in_page.configure(bg='white')
sign_in_page.withdraw()


def clear_main_content():
    for widget in home_page.winfo_children():
        if widget not in [top_bar, side_frame]:
            widget.destroy()

def clear_entries(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
        elif isinstance(widget, tk.Text):
            widget.delete("1.0", tk.END)
def open_sign_in_page():
    clear_main_content()
    welcome_page.withdraw()
    sign_in_page.deiconify()

def open_log_in_page():
    clear_main_content()
    welcome_page.withdraw()
    log_in_page.deiconify()

def open_home_page():
    clear_main_content()
    log_in_page.withdraw()
    sign_in_page.withdraw()
    home_page.deiconify()

def open_welcome():
    home_page.withdraw()
    log_in_page.withdraw()
    sign_in_page.withdraw()
    welcome_page.deiconify()

def close_welcome_page():
    welcome_page.withdraw()
    welcome_page.destroy()

@Logger.log_decorator(
    success_message="log out successful",
    fail_message="log out fail"
)
def log_out():
    clear_main_content()
    home_page.withdraw()
    welcome_page.deiconify()

@Logger.log_decorator(
    success_message="logged in successfully",
    fail_message="logged in fail"
)
def log_in():
    clear_main_content()
    username = e1.get().strip()
    password = e2.get().strip()
    result = ManageCSV.log_in_librarian(username, password)
    if result == "Login successful":
        clear_entries(frame)
        open_home_page()
    else:
        error_label.config(text=result, fg="black", highlightbackground='#ffe6f0')
        raise ValueError("Login failed")

@Logger.log_decorator(
    success_message="registered successfully",
    fail_message="registered fail"
)
def register_librarian_from_gui():
    clear_main_content()
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    user_name = username_entry.get().strip()
    password = password_entry.get().strip()
    conf_password = conf_password_entry.get().strip()

    first_name_error_label.config(text="")
    last_name_error_label.config(text="")
    username_error_label.config(text="")
    password_error_label.config(text="")
    conf_password_error_label.config(text="")

    if not first_name:
        first_name_error_label.config(text="First name is required", fg="black")
    if not last_name:
        last_name_error_label.config(text="Last name is required", fg="black")
    if not user_name:
        username_error_label.config(text="Username is required", fg="black")
    elif ManageCSV.user_exists(user_name):
        username_error_label.config(text="Username already exists", fg="black")
    if not password:
        password_error_label.config(text="Password is required", fg="black")
    if not conf_password:
        conf_password_error_label.config(text="Confirm password is required", fg="black")
    elif password != conf_password:
        conf_password_error_label.config(text="Passwords do not match", fg="black")

    if first_name and last_name and user_name and password and conf_password and password == conf_password and not ManageCSV.user_exists(
            user_name):
        librarian = Librarians(first_name, last_name, user_name, password)
        result = Library.register_librarian(librarian)
        if result != "Librarian added successfully":
            raise ValueError("Registration failed")
        clear_entries(sign_in_frame)
        show_registration_success_message()


def open_add_book_window():
    clear_main_content()
    add_book_window = tk.Toplevel(log_in_page)
    add_book_window.geometry("600x800")
    add_book_window.title("Add Book")
    add_book_window.configure(bg='#b30047')

    add_book_frame = tk.Frame(add_book_window, bg='#b30047', padx=20, pady=20)
    add_book_frame.pack(fill='both', expand=True)

    global title_entry, author_entry, copies_entry, genre_var, year_entry
    global title_error_label, author_error_label, copies_error_label, genre_error_label, year_error_label

    title_label = tk.Label(add_book_frame, text="Title:", font=('Helvetica', 16), bg='#b30047', fg='white')
    title_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    title_entry = tk.Entry(add_book_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
    title_entry.grid(row=1, column=0, padx=5, pady=5)
    title_error_label = tk.Label(add_book_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
    title_error_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

    author_label = tk.Label(add_book_frame, text="Author:", font=('Helvetica', 16), bg='#b30047', fg='white')
    author_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
    author_entry = tk.Entry(add_book_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
    author_entry.grid(row=4, column=0, padx=5, pady=5)
    author_error_label = tk.Label(add_book_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
    author_error_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')

    copies_label = tk.Label(add_book_frame, text="Copies:", font=('Helvetica', 16), bg='#b30047', fg='white')
    copies_label.grid(row=6, column=0, padx=5, pady=5, sticky='w')
    copies_entry = tk.Entry(add_book_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
    copies_entry.grid(row=7, column=0, padx=5, pady=5)
    copies_error_label = tk.Label(add_book_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
    copies_error_label.grid(row=8, column=0, padx=5, pady=5, sticky='w')

    genre_label = tk.Label(add_book_frame, text="Genre:", font=('Helvetica', 16), bg='#b30047', fg='white')
    genre_label.grid(row=9, column=0, padx=5, pady=5, sticky='w')
    genre_var = tk.StringVar(add_book_frame)
    genre_var.set(list(BookGenre)[0].value)
    genre_dropdown = tk.OptionMenu(add_book_frame, genre_var, *[genre.value for genre in BookGenre])
    genre_dropdown.config(font=('Helvetica', 16), bg='#ffe6f0', fg='black', width=35)
    genre_dropdown.grid(row=10, column=0, padx=5, pady=5)
    genre_error_label = tk.Label(add_book_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
    genre_error_label.grid(row=11, column=0, padx=5, pady=5, sticky='w')


    year_label = tk.Label(add_book_frame, text="Year:", font=('Helvetica', 16), bg='#b30047', fg='white')
    year_label.grid(row=12, column=0, padx=5, pady=5, sticky='w')
    year_entry = tk.Entry(add_book_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
    year_entry.grid(row=13, column=0, padx=5, pady=5)
    year_error_label = tk.Label(add_book_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
    year_error_label.grid(row=14, column=0, padx=5, pady=5, sticky='w')

    submit_button = tk.Button(add_book_frame, text="Add Book", font=('Helvetica', 18, 'bold'), width=10, height=2,
                              fg='#b30047', bg='#ffe6f0', borderwidth=1, highlightbackground='#ffe6f0',
                              command=lambda: add_book(add_book_window))
    submit_button.grid(row=15, column=0, padx=10, pady=10)

@Logger.log_decorator(
    success_message="book added successfully",
    fail_message="book added fail"
)
def add_book(parent_window):
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    copies = copies_entry.get().strip()
    genre = genre_var.get().strip()
    year = year_entry.get().strip()

    title_error_label.config(text="")
    author_error_label.config(text="")
    copies_error_label.config(text="")
    genre_error_label.config(text="")
    year_error_label.config(text="")

    if not title:
        title_error_label.config(text="Title is required", fg="black")
    if not author:
        author_error_label.config(text="Author is required", fg="black")
    if not copies or not copies.isdigit():
        copies_error_label.config(text="Copies must be a number", fg="black")
    if not genre:
        genre_error_label.config(text="Genre is required", fg="black")
    if not year or not year.isdigit():
        year_error_label.config(text="Year must be a number", fg="black")

    if title and author and copies.isdigit() and genre and year.isdigit():
        new_book = FactoryBook.create_book(title, author, "No", int(copies), genre, int(year))
        Librarians.add_new_book(new_book)
        parent_window.destroy()
        show_book_added_message()
        new_notification_popup()
    else:
        raise ValueError("Invalid data for adding a book")


def search_books_view():
    clear_main_content()
    for widget in home_page.winfo_children():
        if isinstance(widget, ttk.Treeview) or widget.winfo_name() in ["excel_frame", "button_frame"]:
            widget.destroy()
    try:
        current_file = FileCSV.file_book
        df = pd.read_csv(current_file.value)

        file_switch_frame = tk.Frame(home_page, bg='#b30047', padx=10, pady=10, name="button_frame")
        file_switch_frame.pack(fill='x', pady=10)

        def load_file(file_type):
            nonlocal df
            try:
                df = pd.read_csv(file_type.value)
                if file_type in [FileCSV.file_loaned, FileCSV.file_available]:
                    df = df[["title", "author", "genre", "year"]]
                refresh_table(tree, df)
            except FileNotFoundError:
                show_error_message(f"Error: {file_type.name}.csv file not found!")
            except Exception as e:
                show_error_message(f"Error: {str(e)}")

        all_files_buttons = {
            "Books": FileCSV.file_book,
            "Loaned Books": FileCSV.file_loaned,
            "Available Books": FileCSV.file_available,
        }

        for label, file_enum in all_files_buttons.items():
            file_button = tk.Button(file_switch_frame, text=label, font=('Helvetica', 12), bg='#ffccdf', fg='#b30047',
                                    width=15, command=lambda f=file_enum: load_file(f))
            file_button.pack(side='left', padx=5)

        filter_frame = tk.Frame(home_page, bg='#ffccdf', padx=10, pady=10, name="filter_frame")
        filter_frame.pack(fill='x', pady=10)

        filters = ["Title", "Author", "Genre", "Year"]
        entries = {}

        for filter_name in filters:
            tk.Label(filter_frame, text=filter_name, font=('Helvetica', 12), bg='#ffccdf', fg='#b30047').pack(
                side='left', padx=5)

            if filter_name == "Genre":
                genre_var = tk.StringVar(filter_frame)
                genre_dropdown = tk.OptionMenu(filter_frame, genre_var, *[genre.value for genre in BookGenre])
                genre_dropdown.config(font=('Helvetica', 12), bg='#ffe6f0', fg='black')
                genre_dropdown.pack(side='left', padx=5)
                entries["Genre"] = genre_var
            else:
                entry = tk.Entry(filter_frame, font=('Helvetica', 12), bg='#ffe6f0', fg='black')
                entry.pack(side='left', padx=5)
                entries[filter_name] = entry

        filter_button = tk.Button(filter_frame, text="Filter", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047',
                                  command=lambda:  search_books(entries, tree, df))
        filter_button.pack(side='left', padx=5)

        tree_frame = tk.Frame(home_page, bg='#ffe6f0', name="excel_frame")
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        tree = ttk.Treeview(tree_frame, style="Custom.Treeview")
        tree.pack(side='left', fill='both', expand=True)

        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        for column in df.columns:
            tree.heading(column, text=column, anchor="center", command=lambda c=column: sort_column(tree, c, False))
            tree.column(column, width=100, anchor="center")

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side='right', fill='y')

        style = ttk.Style()
        style.configure("Custom.Treeview", background="#ffe6f0", fieldbackground="#ffe6f0", font=('Helvetica', 12), foreground="black")
        style.map("Custom.Treeview", background=[("selected", "#ffccdf")], foreground=[("selected", "black")])
        style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'), foreground="black")

    except FileNotFoundError:
        show_error_message("Error: books.csv file not found!")
    except Exception as e:
        show_error_message(f"Error: {str(e)}")


@Logger.log_decorator(
    success_message="Search book completed successfully",
    fail_message="Search book completed fail"
)
def search_books(entries, tree, df):
    try:
        search_criteria = get_search_criteria(entries)
        if not search_criteria:
            raise ValueError("No search criteria provided!")
        filtered_df = apply_search_criteria(df, search_criteria)
        if filtered_df.empty:
            raise ValueError("No results found for the given search criteria.")
        refresh_table(tree, filtered_df)
        success_message = build_log_message(search_criteria, success=True)
        Logger.get_logger().info(success_message)

    except Exception:
        fail_message = build_log_message(search_criteria, success=False)
        Logger.get_logger().error(f"{fail_message}")
        raise

def get_search_criteria(entries):
    return {key: value.get().strip() for key, value in entries.items() if value.get().strip()}

def apply_search_criteria(df, search_criteria):
    filtered_df = df
    for field, value in search_criteria.items():
        if field.lower() == "title":
            filtered_df = filtered_df[filtered_df["title"].str.contains(value, case=False)]
        elif field.lower() == "author":
            filtered_df = filtered_df[filtered_df["author"].str.contains(value, case=False)]
        elif field.lower() == "genre":
            filtered_df = filtered_df[filtered_df["genre"].str.contains(value, case=False)]
        elif field.lower() == "year":
            filtered_df = filtered_df[filtered_df["year"].astype(str).str.contains(value, case=False)]
    return filtered_df

def build_log_message(search_criteria, success):
    criteria_messages = []
    for field, value in search_criteria.items():
        if field.lower() == "title":
            criteria_messages.append(f"'{value}' by name")
        elif field.lower() == "author":
            criteria_messages.append(f"'{value}' author name")
        elif field.lower() == "genre":
            criteria_messages.append(f"'{value}' by genre")
        elif field.lower() == "year":
            criteria_messages.append(f"'{value}' by year")

    criteria_text = " and ".join(criteria_messages)
    if success:
        return f"Search book {criteria_text} completed successfully"
    else:
        return f"Search book {criteria_text} fail"

def refresh_table(tree, df):
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"
    for column in df.columns:
        tree.heading(column, text=column, anchor="center")
        tree.column(column, width=100, anchor="center")
    for row in tree.get_children():
        tree.delete(row)
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

def apply_filters(tree, df, entries):
    filtered_df = df
    for key, value in entries.items():
        if key == "Genre":
            selected_genre = value.get()
            if selected_genre:
                filtered_df = filtered_df[filtered_df["genre"] == selected_genre]
        else:
            query = value.get().strip().lower()
            if query:
                filtered_df = filtered_df[filtered_df[key.lower()].astype(str).str.contains(query, case=False)]

    for row in tree.get_children():
        tree.delete(row)

    for index, row in filtered_df.iterrows():
        tree.insert("", "end", values=list(row))

@Logger.log_decorator(
    success_message="Displayed books by successfully",
    fail_message="Displayed book failed"
)
def view_books(file_type="file_book"):
    clear_main_content()
    for widget in home_page.winfo_children():
        if isinstance(widget, ttk.Treeview) or widget.winfo_name() == "excel_frame":
            widget.destroy()

    try:
        filename = FileCSV[file_type].value
        df = pd.read_csv(filename)
        if file_type=="file_book":
            logging.info("Displayed all books successfully")
        elif file_type=="file_loaned":
            logging.info("Displayed borrowed books successfully")
        else:
            logging.info("Displayed available books successfully")

        button_frame = tk.Frame(home_page, bg='#b30047', padx=10, pady=10, name="button_frame")
        button_frame.pack(fill='x', pady=10)

        books_button = tk.Button(button_frame, text="View Books", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=15,
                                 command=lambda: view_books("file_book"))
        books_button.pack(side='left', padx=5)


        loaned_button = tk.Button(button_frame, text="View Loaned Books", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=15,
                                  command=lambda: view_books("file_loaned"))
        loaned_button.pack(side='left', padx=5)


        available_button = tk.Button(button_frame, text="View Available Books", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=15,
                                     command=lambda: view_books("file_available"))
        available_button.pack(side='left', padx=5)

        genre_var = tk.StringVar(button_frame)
        genre_var.set("Select Genre")
        genre_dropdown = tk.OptionMenu(button_frame, genre_var, *[genre.value for genre in BookGenre],
                                       command=lambda selected_genre: filter_by_genre(selected_genre, tree, df))
        genre_dropdown.config(font=('Helvetica', 12), bg='#ffe6f0', fg='black')
        genre_dropdown.pack(side='left', padx=5)

        tree_frame = tk.Frame(home_page, bg='#ffe6f0', name="excel_frame")
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        tree = ttk.Treeview(tree_frame, style="Custom.Treeview")
        tree.pack(side='left', fill='both', expand=True)

        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        for column in df.columns:
            tree.heading(column, text=column, anchor="center", command=lambda c=column: sort_column(tree, c, False))
            tree.column(column, width=100, anchor="center")

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side='right', fill='y')

        style = ttk.Style()
        style.configure("Custom.Treeview", background="#ffe6f0", fieldbackground="#ffe6f0", font=('Helvetica', 12), foreground="black")
        style.map("Custom.Treeview", background=[("selected", "#ffccdf")], foreground=[("selected", "black")])
        style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'), foreground="black")  # כותרות בולטות


    except FileNotFoundError:
        error_label = tk.Label(home_page, text=f"Error: {file_type}.csv file not found!", fg="red", bg="white",
                               font=('Helvetica', 16))
        error_label.pack(pady=20)
        Logger.get_logger().error("Displayed all books fail")
    except Exception as e:
        error_label = tk.Label(home_page, text=f"Error: {str(e)}", fg="red", bg="white", font=('Helvetica', 16))
        error_label.pack(pady=20)
        Logger.get_logger().error(f"Error while displaying books: {str(e)}")

def filter_by_genre(selected_genre, tree, df):
    try:
        if selected_genre == "Select Genre":
            raise ValueError("No genre selected.")
        filtered_df = df[df["genre"].str.contains(selected_genre, case=False, na=False)]
        if filtered_df.empty:
            raise ValueError(f"No books found for genre '{selected_genre}'.")
        refresh_table(tree, filtered_df)
        Logger.get_logger().info(f"Displayed books for genre '{selected_genre}' successfully.")
    except Exception as e:
        show_error_message(f"Error: {str(e)}")
        Logger.get_logger().error(f"Failed to display books for genre '{selected_genre}': {str(e)}")


def remove_books_view():
    clear_main_content()
    for widget in home_page.winfo_children():
        if isinstance(widget, ttk.Treeview) or widget.winfo_name() == "excel_frame":
            widget.destroy()
    try:
        df = pd.read_csv(FileCSV.file_book.value)

        action_frame = tk.Frame(home_page, bg='#b30047', padx=10, pady=10, name="action_frame")
        action_frame.pack(fill='x', pady=10)

        search_label = tk.Label(action_frame, text="Search:", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047')
        search_label.pack(side='left', padx=5)

        search_entry = tk.Entry(action_frame, font=('Helvetica', 12), bg='#ffe6f0', fg='black')
        search_entry.pack(side='left', fill='x', expand=True, padx=5)

        search_button = tk.Button(action_frame, text="Search", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047',
                                  command=lambda: filter_books(tree, search_entry.get(), df))
        search_button.pack(side='left', padx=5)

        delete_button = tk.Button(action_frame, text="Delete", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047',
                                  command=lambda: delete_selected_book(tree))
        delete_button.pack(side='left', padx=5)

        tree_frame = tk.Frame(home_page, bg='#ffe6f0', name="excel_frame")
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        tree = ttk.Treeview(tree_frame, style="Custom.Treeview")
        tree.pack(side='left', fill='both', expand=True)

        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        for column in df.columns:
            tree.heading(column, text=column, anchor="center")
            tree.column(column, width=100, anchor="center")

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side='right', fill='y')

        style = ttk.Style()
        style.configure("Custom.Treeview", background="#ffe6f0", fieldbackground="#ffe6f0", font=('Helvetica', 12),
                        foreground="black")
        style.map("Custom.Treeview", background=[("selected", "#ffccdf")], foreground=[("selected", "black")])
        style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'), foreground="black")  # כותרות בולטות

    except FileNotFoundError:
        error_label = tk.Label(home_page, text="Error: books.csv file not found!", fg="red", bg="white",
                               font=('Helvetica', 16))
        error_label.pack(pady=20)


def filter_books(tree, query, df):
    query = query.strip().lower()
    filtered_df = df[df.apply(lambda row: query in row.astype(str).str.lower().to_string(), axis=1)]

    for row in tree.get_children():
        tree.delete(row)

    for index, row in filtered_df.iterrows():
        tree.insert("", "end", values=list(row))

@Logger.log_decorator(
    success_message="book removed successfully",
    fail_message="book removed fail"
)
def delete_selected_book(tree):
    selected_item = tree.selection()
    if not selected_item:
        error_label = tk.Label(home_page, text="Error: No book selected!", fg="red", bg="white",
                               font=('Helvetica', 12))
        error_label.pack(pady=10)
        return
    selected_book = tree.item(selected_item)["values"]
    title = str(selected_book[0])
    author = selected_book[1]
    is_loaned = selected_book[2]
    copies = selected_book[3]
    genre = selected_book[4]
    year = selected_book[5]

    book_to_delete = FactoryBook.create_book(title=title, author=author, is_loaned=is_loaned, copies=copies, genre=genre,year=year)
    result = Librarians.remove_book(book_to_delete)
    if not result:
        show_error_message("Error!\nAll books are lent!")
        raise ValueError("")

    else:
        df = pd.read_csv(FileCSV.file_book.value)
        for row in tree.get_children():
            tree.delete(row)

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))
        show_success_message("Book deleted successfully!")

def lend_books_view():
    clear_main_content()

    try:
        df = pd.read_csv(FileCSV.file_book.value)
        tree_frame = tk.Frame(home_page, bg='#ffe6f0', name="excel_frame")
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        tree = ttk.Treeview(tree_frame, style="Custom.Treeview")
        tree.pack(side='left', fill='both', expand=True)

        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        for column in df.columns:
            tree.heading(column, text=column, anchor="center")
            tree.column(column, width=100, anchor="center")

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side='right', fill='y')

        style = ttk.Style()
        style.configure("Custom.Treeview", background="#ffe6f0", fieldbackground="#ffe6f0", font=('Helvetica', 12),
                        foreground="black")
        style.map("Custom.Treeview", background=[("selected", "#ffccdf")], foreground=[("selected", "black")])
        style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'), foreground="black")

        lend_button = tk.Button(home_page, text="Lend", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047', width=15,
                                command=lambda: open_lend_popup(tree))
        lend_button.pack(pady=10)

    except FileNotFoundError:
        show_error_message("Error: books.csv file not found!")
    except Exception as e:
        show_error_message(f"Error: {str(e)}")


def open_lend_popup(tree):
    selected_item = tree.selection()
    if not selected_item:
        show_error_message("Error: No book selected!")
        return

    selected_book = tree.item(selected_item)["values"]

    lend_window = tk.Toplevel(log_in_page)
    lend_window.geometry("400x300")
    lend_window.title("Lend Book")
    lend_window.configure(bg='white')

    tk.Label(lend_window, text="Name:", font=('Helvetica', 12), bg='white', fg='black').pack(pady=10)
    name_entry = tk.Entry(lend_window, font=('Helvetica', 12), bg='#ffe6f0', fg='black')
    name_entry.pack(pady=5)

    tk.Label(lend_window, text="Phone Number:", font=('Helvetica', 12), bg='white', fg='black').pack(pady=10)
    phone_entry = tk.Entry(lend_window, font=('Helvetica', 12), bg='#ffe6f0', fg='black')
    phone_entry.pack(pady=5)

    tk.Button(lend_window, text="Confirm", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047',
              command=lambda: lend_book_action(lend_window, name_entry.get(), phone_entry.get(), selected_book)).pack(
        pady=20)

@Logger.log_decorator(
    success_message="book borrowed successfully",
    fail_message="book borrowed fail"
)
def lend_book_action(lend_window, name, phone, selected_book):
    if not name or not phone:
        show_error_message("Error: Name and phone number are required!")
        raise ValueError("Name and phone number are required!")

    book = FactoryBook.create_book(
        title=str(selected_book[0]),
        author=selected_book[1],
        is_loaned=selected_book[2],
        copies=selected_book[3],
        genre=selected_book[4],
        year=selected_book[5]
    )
    member = Members(name, phone)
    result = Librarians.lend_book_to_member(member, book)
    if result:
        show_success_message(f"Book '{book.title}' lent successfully to {name}!")
        new_notification_popup()
    else:
        show_error_message(f"Book '{book.title}' is not available. Added to the waiting list.")
        new_notification_popup()
        raise ValueError("")
    lend_window.destroy()

def return_book_view():
    clear_main_content()
    try:
        df = pd.read_csv(FileCSV.file_book.value)

        action_frame = tk.Frame(home_page, bg='#b30047', padx=10, pady=10, name="action_frame")
        action_frame.pack(fill='x', pady=10)

        search_label = tk.Label(action_frame, text="Search:", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047')
        search_label.pack(side='left', padx=5)

        search_entry = tk.Entry(action_frame, font=('Helvetica', 12), bg='#ffe6f0', fg='black')
        search_entry.pack(side='left', fill='x', expand=True, padx=5)

        search_button = tk.Button(action_frame, text="Search", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047',
                                  command=lambda: filter_books(tree, search_entry.get(), df))
        search_button.pack(side='left', padx=5)

        tree_frame = tk.Frame(home_page, bg='#ffe6f0', name="excel_frame")
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        tree = ttk.Treeview(tree_frame, style="Custom.Treeview")
        tree.pack(side='left', fill='both', expand=True)

        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        for column in df.columns:
            tree.heading(column, text=column, anchor="center")
            tree.column(column, width=100, anchor="center")

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side='right', fill='y')

        style = ttk.Style()
        style.configure("Custom.Treeview", background="#ffe6f0", fieldbackground="#ffe6f0", font=('Helvetica', 12),
                        foreground="black")
        style.map("Custom.Treeview", background=[("selected", "#ffccdf")], foreground=[("selected", "black")])
        style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'), foreground="black")  # כותרות בולטות

        return_button = tk.Button(home_page, text="Return Selected Book", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047',
                                  command=lambda: return_selected_book(tree, df))
        return_button.pack(pady=10)

    except FileNotFoundError:
        show_error_message("Error: loaned_books.csv file not found!")
    except Exception as e:
        show_error_message(f"Error: {str(e)}")

@Logger.log_decorator(
    success_message="book returned successfully",
    fail_message="book returned fail"
)
def return_selected_book(tree, df):
    selected_item = tree.selection()
    if not selected_item:
        show_error_message("Error: No book selected!")
        raise ValueError("No book selected!")

    selected_book = tree.item(selected_item)["values"]
    try:
        book = FactoryBook.create_book(
            title=str(selected_book[0]),
            author=selected_book[1],
            is_loaned=selected_book[2],
            copies=selected_book[3],
            genre=selected_book[4],
            year=selected_book[5]
        )

        result = Librarians.return_book_to_library(book)
        if result==0:
            show_error_message(f"Book '{book.title}' is not currently loaned.")
            raise ValueError("Failed to return the book.")
        elif result==1:
            show_success_message(f"The book '{book.title}' has been returned successfully and lent to the next member in line!")
            new_notification_popup()
        else:
            show_success_message(f"The book '{book.title}' has been returned successfully!")


        df = pd.read_csv(FileCSV.file_book.value)
        for row in tree.get_children():
            tree.delete(row)
        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    except Exception as e:
        show_error_message(f"Error: Failed to return the book")
        raise ValueError("Failed to return the book.")


@Logger.log_decorator(
    success_message="displayed successfully",
    fail_message="displayed fail"
)
def show_popular_books():
    clear_main_content()
    for widget in home_page.winfo_children():
        if isinstance(widget, ttk.Treeview) or widget.winfo_name() in ["excel_frame", "button_frame"]:
            widget.destroy()
    popular_books = Library.get_instance().get_most_popular()
    if popular_books is False or popular_books.empty:
        show_error_message("No books have reached the 'popular' status yet!")
        raise ValueError("No popular books found!")

    action_frame = tk.Frame(home_page, bg='#ffc3e3', padx=10, pady=10, name="action_frame")
    action_frame.pack(fill='x', pady=10)

    search_label = tk.Label(action_frame, text="👑 Most popular books 👑", font=('Arial', 18, 'bold'), bg='#ffc3e3', fg='black')
    search_label.pack(side='top', padx=5)

    table_frame = tk.Frame(home_page, bg='#ffe6f0', padx=10, pady=10, name="excel_frame")
    table_frame.pack(fill='both', expand=True, padx=10, pady=10)

    tree = ttk.Treeview(table_frame, style="Custom.Treeview")
    tree.pack(side='left', fill='both', expand=True)

    tree["columns"] = list(popular_books.columns)
    tree["show"] = "headings"

    for column in popular_books.columns:
        tree.heading(column, text=column, anchor="center", command=lambda c=column: sort_column(tree, c, False))
        tree.column(column, width=150, anchor="center")

    for index, row in popular_books.iterrows():
        tree.insert("", "end", values=list(row))

    scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side='right', fill='y')

    style = ttk.Style()
    style.configure("Custom.Treeview", background="#ffe6f0", fieldbackground="#ffe6f0", font=('Helvetica', 12), foreground="black")
    style.map("Custom.Treeview", background=[("selected", "#ffccdf")], foreground=[("selected", "black")])
    style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'), foreground="black")

def show_notifications():
    clear_main_content()
    notification_frame = tk.Frame(home_page, bg='#ffe6f0', padx=20, pady=20)
    notification_frame.pack(fill='both', expand=True, padx=10, pady=10)

    notifications = Library.get_instance().get_notifications()
    if notifications == "No notifications available.":
        tk.Label(notification_frame, text=notifications, font=('Helvetica', 14), bg='#ffe6f0', fg='#b30047').pack(pady=10)
    else:
        for message in notifications.split("Notification: ")[1:]:
            message_frame = tk.Frame(notification_frame, bg='#ffcce0', padx=10, pady=10, relief='groove', borderwidth=2)
            message_frame.pack(fill='x', pady=5)

            tk.Label(message_frame, text=message, font=('Helvetica', 12), bg='#ffcce0', fg='#b30047', anchor='w').pack(side='left', fill='x', expand=True)
            delete_button = tk.Button(message_frame, text="Delete", font=('Helvetica', 10), bg='#ffccdf', fg='#b30047',
                                       command=lambda m=message: delete_notification(m, notification_frame))
            delete_button.pack(side='right', padx=5)

def delete_notification(message, notification_frame):
    library_instance = Library.get_instance()
    library_instance.notification_system._messages.remove(message.strip())
    for widget in notification_frame.winfo_children():
        widget.destroy()
    show_notifications()

def new_notification_popup():
    if not (home_page.winfo_exists() or log_in_page.winfo_exists() or welcome_page.winfo_exists()):
        print("Error: Application windows have been destroyed. Cannot show notification.")
        return
    parent_window = None
    if home_page.winfo_exists():
        parent_window = home_page
    elif log_in_page.winfo_exists():
        parent_window = log_in_page
    elif welcome_page.winfo_exists():
        parent_window = welcome_page

    popup = tk.Toplevel(parent_window)
    popup.geometry("300x200")
    popup.title("New Notification")
    popup.configure(bg="white")
    message_label = tk.Label(popup, text="A new notification has arrived!", font=('Helvetica', 12), bg="white", fg="black")
    message_label.pack(pady=10)

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    position_right = int((screen_width / 2) - (300 / 2))
    position_down = int((screen_height / 2) - (200 / 2))
    popup.geometry(f"300x200+{position_right}+{position_down}")

    view_button = tk.Button(popup, text="View Notifications", font=('Helvetica', 12), bg="#ffe6f0", fg="#b30047",
                            highlightbackground='#ffe6f0', command=lambda: [popup.destroy(), show_notifications()])
    view_button.pack(pady=5)

    close_button = tk.Button(popup, text="Close", font=('Helvetica', 12), bg="#ffe6f0", fg="#b30047",
                             highlightbackground='#ffe6f0', command=popup.destroy)
    close_button.pack(pady=5)

def show_success_message(message):
    success_window = tk.Toplevel(log_in_page)
    success_window.geometry("600x200")
    success_window.title("Success")
    success_window.configure(bg='white')

    message_label = tk.Label(success_window, text=message, font=('Helvetica', 16, 'bold'), fg='#b30047', bg='white')
    message_label.pack(pady=20)

    close_button = tk.Button(success_window, text="OK", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047', width=15,
                             command=success_window.destroy)
    close_button.pack(pady=10)

def show_error_message(message):
    error_window = tk.Toplevel(log_in_page)
    error_window.geometry("600x200")
    error_window.title("Error")
    error_window.configure(bg='white')

    message_label = tk.Label(error_window, text=message, font=('Helvetica', 16, 'bold'), fg='#b30047', bg='white')
    message_label.pack(pady=20)

    close_button = tk.Button(error_window, text="OK", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047', width=15,
                             command=error_window.destroy)
    close_button.pack(pady=10)

def sort_column(tree, col, reverse):
    data = [(tree.set(k, col), k) for k in tree.get_children("")]
    data.sort(reverse=reverse)

    for index, (val, k) in enumerate(data):
        tree.move(k, '', index)

    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))


def show_registration_success_message():
    success_window = tk.Toplevel(log_in_page)
    success_window.geometry("400x200")
    success_window.title("Registration Successful")
    success_window.configure(bg='white')

    message_label = tk.Label(success_window, text="Registration Successful!", font=('Helvetica', 16, 'bold'), fg='#b30047', bg='white')
    message_label.pack(pady=20)

    back_button = tk.Button(success_window, text="Back to Log In", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047', width=15,
                            command=lambda: [success_window.destroy(), open_welcome()])
    back_button.pack(pady=10)

def show_book_added_message():
    success_window = tk.Toplevel(log_in_page)
    success_window.geometry("400x200")
    success_window.title("Book Added Successfully")
    success_window.configure(bg='white')

    message_label = tk.Label(success_window, text="Book Added Successfully!", font=('Helvetica', 16, 'bold'), fg='#b30047', bg='white')
    message_label.pack(pady=20)

    back_button = tk.Button(success_window, text="Back to Home", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047', width=15,
                            command=lambda: [success_window.destroy(), open_home_page()])
    back_button.pack(pady=10)
welcome_label = tk.Label(welcome_page, text="Welcome to the E&M Library",
                             font=('Arial', 50, 'bold'), bg='#ffe6f0', fg='#b30047')
welcome_label.pack(pady=50)
heart_icon = tk.Label(welcome_page, text="❤️", font=('Arial', 50), bg='#ffe6f0', fg='#b30047')
heart_icon.pack(pady=50)
s_register_button = tk.Button(welcome_page, text="Register", font=('Helvetica', 18, 'bold'), width=15, height=2,
                                 bg='#b30047', fg='black', command= open_sign_in_page)
s_register_button.pack(pady=10)
s_login_button = tk.Button(welcome_page, text="Log In", font=('Helvetica', 18, 'bold'), width=15, height=2,
                              bg='#b30047', fg='black', command=open_log_in_page)
s_login_button.pack(pady=10)

back_button_top = tk.Button(sign_in_page, text="Back", font=('Helvetica', 16), bg='#ffe6f0', fg='#b30047', relief='flat',
                            highlightbackground='#ffe6f0', command=open_welcome)
back_button_top.pack(side='top', anchor='ne', padx=10, pady=10)

back_button_top = tk.Button(log_in_page, text="Back", font=('Helvetica', 16), bg='#ffe6f0', fg='#b30047', relief='flat',
                            highlightbackground='#ffe6f0', command=open_welcome)
back_button_top.pack(side='top', anchor='ne', padx=10, pady=10)

frame = tk.Frame(log_in_page, bg='#b30047', width=200, height=800)
frame.place(relx=0.5, rely=0.5, anchor='center')

top_bar = tk.Frame(home_page, bg='#b30047', height=70)
top_bar.pack(side='top', fill='x')

top_label = tk.Label(top_bar, text="E&M Library", font=('Arial', 20, 'bold'), bg='#b30047', fg='white')
top_label.place(relx=0.5, rely=0.5, anchor='center')

log_out_button = tk.Button(top_bar, text="Log Out", font=('Arial', 12), bg='#ffccdf', fg='#b30047', relief='flat',
                           highlightbackground='#ffe6f0', command=log_out)
log_out_button.pack(side='right', padx=10, pady=10)


username_label = tk.Label(frame, text="Username:", font=('Helvetica', 20), bg='#b30047', fg='white')
username_label.grid(row=0, column=0, padx=20, pady=20, sticky='w')

e1 = tk.Entry(frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
e1.grid(row=1, column=0, padx=20, pady=20)

password_label = tk.Label(frame, text="Password:", font=('Helvetica', 20), bg='#b30047', fg='white')
password_label.grid(row=2, column=0, padx=20, pady=20, sticky='w')

e2 = tk.Entry(frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2, show="*")
e2.grid(row=3, column=0, padx=20, pady=20)

log_in_button = tk.Button(frame, text="Log In", font=('Ariel ', 18, 'bold'), width=10, height=2,
                          fg='#b30047', bg='#ffe6f0', borderwidth=1, highlightbackground='#ffe6f0',
                          command=log_in)
log_in_button.grid(row=4, column=0, padx=10, pady=10)

error_label = tk.Label(frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
error_label.grid(row=6, column=0, padx=10, pady=10)

sign_in_frame = tk.Frame(sign_in_page, bg='#b30047', padx=20, pady=20)
sign_in_frame.place(relx=0.5, rely=0.5, anchor='center')

first_name_label = tk.Label(sign_in_frame, text="First name:", font=('Helvetica', 20), bg='#b30047', fg='white')
first_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
first_name_entry = tk.Entry(sign_in_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
first_name_entry.grid(row=1, column=0, padx=5, pady=5)
first_name_error_label = tk.Label(sign_in_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
first_name_error_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

last_name_label = tk.Label(sign_in_frame, text="Last name:", font=('Helvetica', 20), bg='#b30047', fg='white')
last_name_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
last_name_entry = tk.Entry(sign_in_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
last_name_entry.grid(row=4, column=0, padx=5, pady=5)
last_name_error_label = tk.Label(sign_in_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
last_name_error_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')

username_label = tk.Label(sign_in_frame, text="Username:", font=('Helvetica', 20), bg='#b30047', fg='white')
username_label.grid(row=6, column=0, padx=5, pady=5, sticky='w')
username_entry = tk.Entry(sign_in_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
username_entry.grid(row=7, column=0, padx=5, pady=5)
username_error_label = tk.Label(sign_in_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
username_error_label.grid(row=8, column=0, padx=5, pady=5, sticky='w')

password_label = tk.Label(sign_in_frame, text="Password:", font=('Helvetica', 20), bg='#b30047', fg='white')
password_label.grid(row=9, column=0, padx=5, pady=5, sticky='w')
password_entry = tk.Entry(sign_in_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2, show="*")
password_entry.grid(row=10, column=0, padx=5, pady=5)
password_error_label = tk.Label(sign_in_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
password_error_label.grid(row=11, column=0, padx=5, pady=5, sticky='w')

conf_password_label = tk.Label(sign_in_frame, text="Confirm Password:", font=('Helvetica', 20), bg='#b30047', fg='white')
conf_password_label.grid(row=12, column=0, padx=5, pady=5, sticky='w')
conf_password_entry = tk.Entry(sign_in_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2, show="*")
conf_password_entry.grid(row=13, column=0, padx=5, pady=5)
conf_password_error_label = tk.Label(sign_in_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
conf_password_error_label.grid(row=14, column=0, padx=5, pady=5, sticky='w')

submit_button = tk.Button(sign_in_frame, text="Submit", font=('Helvetica', 18, 'bold'), width=10, height=2,
                           fg='#b30047', bg='#ffe6f0', borderwidth=1, highlightbackground='#ffe6f0',
                           command=register_librarian_from_gui)
submit_button.grid(row=15, column=0, padx=10, pady=10)

side_frame = tk.Frame(home_page, bg='#ffe6f0', width=200)
side_frame.pack(side='left', fill='y')

button_frame1 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame1.pack(fill='x', pady=5)
add_book_button = tk.Button(button_frame1, text="Add Book", font=('Helvetica', 16), bg='#ffccdf', fg='#b30047', width=18, height=2,
                            highlightbackground='#ffe6f0', relief='flat', command=open_add_book_window)
add_book_button.pack()

button_frame2 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame2.pack(fill='x', pady=5)
remove_book_button = tk.Button(button_frame2, text="Remove Book", font=('Helvetica', 16), bg='#ffccdf', fg='#b30047', width=18, height=2,
                               highlightbackground='#ffe6f0', relief='flat', command=remove_books_view)
remove_book_button.pack()

button_frame3 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame3.pack(fill='x', pady=5)
search_book_button = tk.Button(button_frame3, text="Search Book", font=('Helvetica', 16), bg='#ffccdf', fg='#b30047', width=18, height=2,
                               highlightbackground='#ffe6f0', relief='flat', command=search_books_view)
search_book_button.pack()

button_frame4 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame4.pack(fill='x', pady=5)
view_book_button = tk.Button(button_frame4, text="View Books", font=('Helvetica', 16), bg='#ffccdf', fg='#b30047', width=18, height=2,
                             highlightbackground='#ffe6f0', relief='flat', command=view_books)
view_book_button.pack()

button_frame5 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame5.pack(fill='x', pady=5)
lend_book_button = tk.Button(button_frame5, text="Lend Book", font=('Helvetica', 16), bg='#ffccdf', fg='#b30047', width=18, height=2,
                             highlightbackground='#ffe6f0', relief='flat', command= lend_books_view)
lend_book_button.pack()

button_frame6 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame6.pack(fill='x', pady=5)
return_book_button = tk.Button(button_frame6, text="Return Book", font=('Helvetica', 16), bg='#ffccdf', fg='#b30047', width=18, height=2,
                               highlightbackground='#ffe6f0', relief='flat', command= return_book_view)
return_book_button.pack()

button_frame7 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame7.pack(fill='x', pady=5)
popular_books_button = tk.Button(button_frame7, text="Popular Books", font=('Helvetica', 16), bg='#ffccdf', fg='#b30047', width=18, height=2,
                                 highlightbackground='#ffe6f0', relief='flat', command= show_popular_books)
popular_books_button.pack()

button_frame8 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame8.pack(fill='x', pady=5)
notification_button = tk.Button(button_frame8, text="Notification", font=('Helvetica', 16), bg='#ffccdf', fg='#b30047', width=18, height=2,
                                 highlightbackground='#ffe6f0', relief='flat', command=show_notifications)
notification_button.pack()

welcome_page.mainloop()