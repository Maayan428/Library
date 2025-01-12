import tkinter as tk

from SystemManagement.Library import Library
from SystemManagement.Book.ManageCSV import ManageCSV
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
            show_success_message()

def show_success_message():
    success_window = tk.Toplevel(root)
    success_window.geometry("400x200")
    success_window.title("Registration Successful")
    success_window.configure(bg='white')

    message_label = tk.Label(success_window, text="Registration Successful!", font=('Helvetica', 16, 'bold'), fg='#b30047', bg='white')
    message_label.pack(pady=20)

    back_button = tk.Button(success_window, text="Back to Log In", font=('Helvetica', 12), bg='#ffe6f0', fg='#b30047', width=15,
                            command=lambda: [success_window.destroy(), back_to_root()])
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

sign_in_button = tk.Button(frame, text="Sign In", font=('Helvetica', 18, 'bold'), width=10, height=2,
                           fg='#b30047', bg='#ffe6f0', borderwidth=1, highlightbackground='#ffe6f0',
                           command=open_sign_in_page)
sign_in_button.grid(row=5, column=0, padx=10, pady=10)

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
button1 = tk.Button(button_frame1, text="Button 1", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                    highlightbackground='#ffe6f0',relief='flat')
button1.pack()

button_frame2 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame2.pack(fill='x', pady=5)
button2 = tk.Button(button_frame2, text="Button 2", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                    highlightbackground='#ffe6f0', relief='flat')
button2.pack()

button_frame3 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame3.pack(fill='x', pady=5)
button3 = tk.Button(button_frame3, text="Button 3", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                    highlightbackground='#ffe6f0', relief='flat')
button3.pack()

button_frame4 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame4.pack(fill='x', pady=5)
button4 = tk.Button(button_frame4, text="Button 4", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                    highlightbackground='#ffe6f0', relief='flat')
button4.pack()

button_frame5 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame5.pack(fill='x', pady=5)
button5 = tk.Button(button_frame5, text="Button 5", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                    highlightbackground='#ffe6f0', relief='flat')
button5.pack()

button_frame6 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame6.pack(fill='x', pady=5)
button6 = tk.Button(button_frame6, text="Button 6", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                    highlightbackground='#ffe6f0', relief='flat')
button6.pack()

button_frame7 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame7.pack(fill='x', pady=5)
button7 = tk.Button(button_frame7, text="Button 7", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                    highlightbackground='#ffe6f0', relief='flat')
button7.pack()

button_frame8 = tk.Frame(side_frame, bg='#ffccdf', padx=5, pady=5)
button_frame8.pack(fill='x', pady=5)
button8 = tk.Button(button_frame8, text="Button 8", font=('Helvetica', 12), bg='#ffccdf', fg='#b30047', width=18, height=2,
                    highlightbackground='#ffe6f0', relief='flat')
button8.pack()

root.mainloop()

