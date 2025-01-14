import tkinter as tk
from tkinter import ttk
import pandas as pd
from multiprocessing.resource_tracker import register

from SystemManagement.Book.FileCSV import FileCSV
from SystemManagement.Book.Book import Book
from SystemManagement import Librarians
from SystemManagement.Book.FactoryBook import FactoryBook
from SystemManagement.Library import Library
from SystemManagement.Book.ManageCSV import ManageCSV
from SystemManagement.Book.BookGenre import BookGenre
from werkzeug.security import check_password_hash

def open_home_page():
    root.withdraw()
    home_page.deiconify()

def back_to_root():
    home_page.withdraw()
    root.deiconify()

def open_sign_in_page():
    root.withdraw()
    sign_in_page.deiconify()

def log_out():
    home_page.withdraw()
    root.deiconify()

def log_in():
    username = e1.get().strip()
    password = e2.get().strip()
    result = ManageCSV.log_in_librarian(username, password)
    if result == "Login successful":
        open_home_page()
    else:
        error_label.config(text=result, fg="black", highlightbackground='#ffe6f0')

def register_librarian_from_gui():
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

    if first_name and last_name and user_name and password and conf_password and password == conf_password and not ManageCSV.user_exists(user_name):
        result = Library.register_librarian(first_name, last_name, user_name, password, conf_password)
        if result == "Librarian added successfully":
            show_registration_success_message(sign_in_page)

def open_add_book_window():
    add_book_window = tk.Toplevel(root)
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
        Librarians.Librarians.add_new_book(new_book)
        parent_window.destroy()
        show_book_added_message()

def view_books(file_type="file_book"):
    for widget in home_page.winfo_children():
        if isinstance(widget, ttk.Treeview) or widget.winfo_name() == "excel_frame":
            widget.destroy()

    try:
        filename = FileCSV[file_type].value
        df = pd.read_csv(filename)

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
        error_label = tk.Label(home_page, text=f"Error: {file_type}.csv file not found!", fg="red", bg="white", font=('Helvetica', 16))
        error_label.pack(pady=20)
    except Exception as e:
        error_label = tk.Label(home_page, text=f"Error: {str(e)}", fg="red", bg="white", font=('Helvetica', 16))
        error_label.pack(pady=20)

def remove_books_view():
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


def delete_selected_book(tree):
    selected_item = tree.selection()
    if not selected_item:
        error_label = tk.Label(home_page, text="Error: No book selected!", fg="red", bg="white",
                               font=('Helvetica', 12))
        error_label.pack(pady=10)
        return
    selected_book = tree.item(selected_item)["values"]
    title = selected_book[0]
    author = selected_book[1]
    is_loaned = selected_book[2]
    copies = selected_book[3]
    genre = selected_book[4]
    year = selected_book[5]

    book_to_delete = FactoryBook.create_book(title=title, author=author, is_loaned=is_loaned, copies=copies, genre=genre,year=year)
    result = Librarians.Librarians.remove_book(book_to_delete)
    if not result:
        show_error_message("Error!\nAll books are lent!")
    else:
        df = pd.read_csv(FileCSV.file_book.value)
        for row in tree.get_children():
            tree.delete(row)

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))
        show_success_message("Book deleted successfully!")

def show_success_message(message):
    success_window = tk.Toplevel(root)
    success_window.geometry("400x200")
    success_window.title("Success")
    success_window.configure(bg='white')

    message_label = tk.Label(success_window, text=message, font=('Helvetica', 16, 'bold'), fg='#b30047', bg='white')
    message_label.pack(pady=20)

    close_button = tk.Button(success_window, text="OK", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047', width=15,
                             command=success_window.destroy)
    close_button.pack(pady=10)

def show_error_message(message):
    error_window = tk.Toplevel(root)
    error_window.geometry("400x200")
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
    success_window = tk.Toplevel(root)
    success_window.geometry("400x200")
    success_window.title("Registration Successful")
    success_window.configure(bg='white')

    message_label = tk.Label(success_window, text="Registration Successful!", font=('Helvetica', 16, 'bold'), fg='#b30047', bg='white')
    message_label.pack(pady=20)

    back_button = tk.Button(success_window, text="Back to Log In", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047', width=15,
                            command=lambda: [success_window.destroy(), back_to_root()])
    back_button.pack(pady=10)

def show_book_added_message():
    success_window = tk.Toplevel(root)
    success_window.geometry("400x200")
    success_window.title("Book Added Successfully")
    success_window.configure(bg='white')

    message_label = tk.Label(success_window, text="Book Added Successfully!", font=('Helvetica', 16, 'bold'), fg='#b30047', bg='white')
    message_label.pack(pady=20)

    back_button = tk.Button(success_window, text="Back to Home", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047', width=15,
                            command=lambda: [success_window.destroy(), open_home_page()])
    back_button.pack(pady=10)

root = tk.Tk()
root.geometry("1200x800")
root.title("E&M Library")
root.configure(bg='white')

home_page = tk.Toplevel(root)
home_page.geometry("1200x800")
home_page.title("E&M Home Page")
home_page.configure(bg='white')
home_page.withdraw()

sign_in_page = tk.Toplevel(root)
sign_in_page.geometry("1200x800")
sign_in_page.title("E&M Home Page")
sign_in_page.configure(bg='white')
sign_in_page.withdraw()

back_button_top = tk.Button(sign_in_page, text="Back", font=('Helvetica', 16), bg='#ffe6f0', fg='#b30047', relief='flat',
                            highlightbackground='#ffe6f0', command=back_to_root)
back_button_top.pack(side='top', anchor='ne', padx=10, pady=10)

frame = tk.Frame(root, bg='#b30047')
frame.place(relx=0.5, rely=0.5, anchor='center')

top_bar = tk.Frame(home_page, bg='#b30047', height=70)
top_bar.pack(side='top', fill='x')

top_label = tk.Label(top_bar, text="E&M Library", font=('Arial', 20, 'bold'), bg='#b30047', fg='white')
top_label.place(relx=0.5, rely=0.5, anchor='center')

log_out_button = tk.Button(top_bar, text="Log Out", font=('Arial', 12), bg='#ffccdf', fg='#b30047', relief='flat',
                           highlightbackground='#ffe6f0', command=back_to_root)
log_out_button.pack(side='right', padx=10, pady=10)


username_label = tk.Label(frame, text="Username:", font=('Helvetica', 16), bg='#b30047', fg='white')
username_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

e1 = tk.Entry(frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
e1.grid(row=1, column=0, padx=5, pady=5)

password_label = tk.Label(frame, text="Password:", font=('Helvetica', 16), bg='#b30047', fg='white')
password_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

e2 = tk.Entry(frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2, show="*")
e2.grid(row=3, column=0, padx=5, pady=5)

log_in_button = tk.Button(frame, text="Log In", font=('Ariel ', 18, 'bold'), width=10, height=2,
                          fg='#b30047', bg='#ffe6f0', borderwidth=1, highlightbackground='#ffe6f0',
                          command=log_in)
log_in_button.grid(row=4, column=0, padx=10, pady=10)

register_button = tk.Button(frame, text="Register", font=('Helvetica', 18, 'bold'), width=10, height=2,
                            fg='#b30047', bg='#ffe6f0', borderwidth=1, highlightbackground='#ffe6f0',
                            command=open_sign_in_page)
register_button.grid(row=5, column=0, padx=10, pady=10)

error_label = tk.Label(frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
error_label.grid(row=6, column=0, padx=10, pady=10)

sign_in_frame = tk.Frame(sign_in_page, bg='#b30047', padx=20, pady=20)
sign_in_frame.place(relx=0.5, rely=0.5, anchor='center')

first_name_label = tk.Label(sign_in_frame, text="First name:", font=('Helvetica', 16), bg='#b30047', fg='white')
first_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
first_name_entry = tk.Entry(sign_in_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
first_name_entry.grid(row=1, column=0, padx=5, pady=5)
first_name_error_label = tk.Label(sign_in_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
first_name_error_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

last_name_label = tk.Label(sign_in_frame, text="Last name:", font=('Helvetica', 16), bg='#b30047', fg='white')
last_name_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
last_name_entry = tk.Entry(sign_in_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
last_name_entry.grid(row=4, column=0, padx=5, pady=5)
last_name_error_label = tk.Label(sign_in_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
last_name_error_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')

username_label = tk.Label(sign_in_frame, text="Username:", font=('Helvetica', 16), bg='#b30047', fg='white')
username_label.grid(row=6, column=0, padx=5, pady=5, sticky='w')
username_entry = tk.Entry(sign_in_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2)
username_entry.grid(row=7, column=0, padx=5, pady=5)
username_error_label = tk.Label(sign_in_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
username_error_label.grid(row=8, column=0, padx=5, pady=5, sticky='w')

password_label = tk.Label(sign_in_frame, text="Password:", font=('Helvetica', 16), bg='#b30047', fg='white')
password_label.grid(row=9, column=0, padx=5, pady=5, sticky='w')
password_entry = tk.Entry(sign_in_frame, width=40, bg='#ffe6f0', fg='black', font=('Helvetica', 16), borderwidth=2, show="*")
password_entry.grid(row=10, column=0, padx=5, pady=5)
password_error_label = tk.Label(sign_in_frame, text="", font=('Helvetica', 16), fg="black", bg='#b30047')
password_error_label.grid(row=11, column=0, padx=5, pady=5, sticky='w')

conf_password_label = tk.Label(sign_in_frame, text="Confirm Password:", font=('Helvetica', 16), bg='#b30047', fg='white')
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
add_book_button = tk.Button(button_frame1, text="Add Book", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                            highlightbackground='#ffe6f0', relief='flat', command=open_add_book_window)
add_book_button.pack()

button_frame2 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame2.pack(fill='x', pady=5)
remove_book_button = tk.Button(button_frame2, text="Remove Book", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                               highlightbackground='#ffe6f0', relief='flat', command=remove_books_view)
remove_book_button.pack()

button_frame3 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame3.pack(fill='x', pady=5)
search_book_button = tk.Button(button_frame3, text="Search Book", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                               highlightbackground='#ffe6f0', relief='flat')
search_book_button.pack()

button_frame4 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame4.pack(fill='x', pady=5)
view_book_button = tk.Button(button_frame4, text="View Books", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                             highlightbackground='#ffe6f0', relief='flat', command=view_books)
view_book_button.pack()

button_frame5 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame5.pack(fill='x', pady=5)
lend_book_button = tk.Button(button_frame5, text="Lend Book", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                             highlightbackground='#ffe6f0', relief='flat')
lend_book_button.pack()

button_frame6 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame6.pack(fill='x', pady=5)
return_book_button = tk.Button(button_frame6, text="Return Book", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                               highlightbackground='#ffe6f0', relief='flat')
return_book_button.pack()

button_frame7 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame7.pack(fill='x', pady=5)
popular_books_button = tk.Button(button_frame7, text="Popular Books", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                                 highlightbackground='#ffe6f0', relief='flat')
popular_books_button.pack()

root.mainloop()

