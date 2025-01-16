from collections import deque


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























