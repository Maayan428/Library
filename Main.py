from Subscriptions.Members import Members
from SystemManagement.Book.BookGenre import BookGenre
from SystemManagement.Book.FileCSV import FileCSV
from SystemManagement.Book.ManageCSV import ManageCSV
from SystemManagement.Librarians import Librarians
from SystemManagement.Library import Library
from SystemManagement.PopularBooks import PopularBook
from SystemManagement.Book.Book import Book
import sys
import os

class Main:

    library = Library.get_instance()
    Library.sign_in("eden", "hassin", "12345", "password123")
    librarian = Librarians("Anna", "Smith", "67890", "admin123")
    Library.sign_in(librarian.first_name, librarian.last_name, librarian.member_id, librarian.password)
    book1 = Book("the maayan", "J.K. Rowling", "Yes", 3, BookGenre.Satire.value, 1997)
    book2 = Book("the eden", "J.R.R. Tolkien", "No", 1, BookGenre.Classic.value, 1937)

    member = Members("John", "Doe", "12345", "password123")



    # ManageCSV.add_book_to_csv(FileCSV.file_available.value,book1)
    # ManageCSV.add_book_to_csv(FileCSV.file_available.value, book1)
    # ManageCSV.add_book_to_csv(FileCSV.file_available.value, book1)
    # ManageCSV.add_book_to_csv(FileCSV.file_available.value,book2)
    # ManageCSV.delete_book_from_csv(FileCSV.file_available.value,book1)
    # count=ManageCSV.return_appearances(FileCSV.file_available.value,book2)
    # print(count)
    # ManageCSV.add_to_parameter(FileCSV.file_book.value,book2,"copies")
    # ManageCSV.sub_from_parameter(FileCSV.file_book.value,book2,"copies")
    # librarian.add_new_book(book2)
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
    # librarian.lend_book_to_member(member, book1)
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
