class Book:
    def __init__(self, title, author, isdn):
        self.title = title
        self.author = author
        self.isdn = isdn
        self.load = Loan()

    def __repr__(self):
        return f"(Title: {self.title}, Author: {self.author}, ISDN: {self.isdn}, On Loan Status: {self._is_loaned})"


class Loan:
    def __init__(self):
        self.status = False


class Library:
    def __init__(self):
        self._books = []

    def __repr__(self):
        # main_string = ""
        # for book in self._books:
        #     # main_string = main_string + (f"Title: {book.title}, Author: {book.author}, ISDN: {book.isdn}, \n")
        #     main_string = main_string + str(book)
        # return main_string
        return str(self.get_books())

    def add_new_book(self, title, author, isdn):
        book = Book(title, author, isdn)
        self._books.append(book)

    def add_book(self, book):
        self._books.append(book)

    def get_books(self):
        return self._books

    def remove_book(self, title):
        for _book in self._books:
            if _book.title == title:
                self._books.remove(_book)

    def search_by_title(self, title):
        results = []
        for _book in self._books:
            if _book.title == title:
                results.append(_book)
        return f"Found these books: {results}"


if __name__ == "__main__":
    book1 = Book("name", "amir", "1")
    lib = Library()
    lib.add_book(book1)
    lib.add_new_book("Night of the Dead", "Amir Rashkovsky", "B07148ISDN")
    print(lib)
