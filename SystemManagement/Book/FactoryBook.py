from SystemManagement.Book.Book import Book

class FactoryBook:

    @staticmethod
    def create_book(title,author, is_loaned, copies, genre, year):
        return Book(title,author, is_loaned, copies, genre, year)



