# E&M Library Management System

Welcome to the **E&M Library Management System**, 
An easy-to-use program designed to help librarians manage their library's daily operations, 
including adding, removing, lending, and returning books. 
The system also provides features such as viewing popular books and managing notifications,
all through a fun, pink graphical user interface (GUI).

---

## 📖 Usage Instructions

1. **Launch the program**:  
   - Start the program by executing `Main.py`.
   - Run the program through `GUI.py`.

2. **On the welcome page, choose**:  
   - **Register**: To register a new librarian.  
   - **Log In**: To access the library system (if already signed in).  

3. **Use the side menu bar to**:  
   - **Add Book**: Add a new books to the library.  
   - **Remove Book**: Delete books from the system.  
   - **Search Book**: Find books by title, author, genre, or year.  
   - **View Books**: See all books, loaned books, or available books.  
   - **Lend Book**: Assign a certain book to a member.  
   - **Return Book**: Return a loaned book.  
   - **Popular Books**: View the most requested books.  
   - **Notifications**: View and manage the system's notifications.

---

## 📋 Features

- **Book Management**:
  - Add, remove, search, and view books.
  - Categorize books by genres, titles, authors, and more.
  - Track the availability of books and loaned copies.

- **Member Management**:
  - Register new librarians.
  - Log-in and Log-out for existing users.
  - Lend books to members and manage their details.
  - Maintain a waiting list for popular books.

- **Notifications**:
  - Notify all librarians at the library about important events, such as new book arrivals or returns.
  - Keep a clear history of notifications.
  - Ability to delete notifications if needed.

- **Statistics**:
  - Identify and display the most popular books based on their requests frequency.
  - Displays books by chosen filters.

---

## 🛠 Design Patterns Used

1. **Singleton**:
   - The `Library` class ensures only one instance of the library system exists.

2. **Factory**:
   - The `FactoryBook` class dynamically creates book objects based on the provided attributes.

3. **Observer**:
   - The notification system alerts users about system events like new arrivals or return of popular books to availability.

4. **Decorator**:
   - Logging functions are decorated to capture success and failure events.
   - All events that are captured are saved into the Action_History.txt file.

---

## 💡 What does Main.py do?

- If the required CSV files for the library system do not exist, `Main.py` will **create and initialize** them.  
- It ensures that all necessary columns are added to the Excel files, resets data, and prepares the system for the first use.

---

## 🛠️ Technologies Used

- **Programming Language**: Python  
- **GUI Library**: Tkinter  
- **Data Storage**: CSV files (for storing several stages of books statuses, and all the system's members)  
- **Password Management**: Hashing using `werkzeug.security`  
- **Logging**: Rotating logs with `logging` module  
- **CSV Management**: handling and storing all the system's data.

---


