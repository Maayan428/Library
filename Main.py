from SystemManagement.Book.BookGenre import BookGenre
from SystemManagement.Book.FileCSV import FileCSV
from SystemManagement.Book.ManageCSV import ManageCSV
from SystemManagement.Librarians import Librarians
from SystemManagement.Library import Library
from SystemManagement.PopularBooks import PopularBook
from SystemManagement.Book.Book import Book
from Subscriptions.Members import Members
import sys
import os

class Main:

    library = Library.get_instance()
    librarian= Librarians("anna", "lama", "123", "123")
    Library.register_librarian(librarian)
    book1 = Book("the maayan", "J.K. Rowling", "Yes", 3, BookGenre.Satire.value, 1997)
    book2 = Book("the eden", "J.R.R. Tolkien", "No", 1, BookGenre.Classic.value, 1937)
    member= Members("yael", "0987765")
    #librarian.add_new_book(book1)
    librarian.lend_book_to_member(member, book1)

    librarian.return_book_to_library(book1)
    print(library.get_notifications())
    # t=ManageCSV.get_value_other(FileCSV.file_book.value,book2,"title")
    # c=ManageCSV.get_value_books(book2,"copies")
    # print(t)
    # print(c)
    # #
    #
    # print("\n--- Adding New Books ---")
    # librarian.add_new_book(book1)
    # librarian.add_new_book(book2)
    # print("\n--- Removing a Book ---")
    # librarian.remove_book(book1)
    #
    # num=ManageCSV().get_value_books(book2,"copies")
    # print(num)
    # num2=ManageCSV().get_value_other(FileCSV.file_available.value,book2,"title")
    # print(num2)
    #
    # print("\n--- Lending a Book to a Member ---")

    # if book1.waiting_list:
    #     print(f"\n {book1.pop_first_member().get_member_id()}")
    # else:
    #     print("The waiting list is empty.")
    #
    # print("\n--- Returning a Book to the Library ---")
    # librarian.return_book_to_library(book1)
    #


if __name__ == "__main__":
    Main()
