import csv
from collections import deque
from SystemManagement.Book.BookGenre import BookGenre
from SystemManagement.Book.FileCSV import FileCSV
from SystemManagement.Book.ManageCSV import ManageCSV


class Book:

    def __init__(self, title, author, is_loaned, copies, genre, year):
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year
        self.requests = 0
        self.currently_loaned = 0
        self.waiting_list = deque()

    def new_to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "is_loaned": self.is_loaned,
            "copies": self.copies,
            "genre": self.genre,
            "year": self.year,
            "requests": self.requests,
            "currently_loaned": self.currently_loaned
        }
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "year": self.year
        }


    def add_waiting_list(self, member):
        self.waiting_list.append(member)

    def pop_first_member(self):
        if not self.waiting_list:
            raise ValueError("Cannot pop from an empty waiting list")
        return self.waiting_list.popleft()






















