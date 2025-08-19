#Library Management System

from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self._is_available = True  

    def borrow(self):
        if self._is_available:
            self._is_available = False
            return True
        return False

    def return_book(self):
        self._is_available = True

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self._member_id = member_id   
        self.borrowed_books = []     

    def borrow_book(self, book, library):
        if book.borrow():
            due_date = datetime.now() + timedelta(days=14)
            transaction = Transaction(self, book, "borrow", due_date)
            self.borrowed_books.append(transaction)
            library.transactions.append(transaction)
            print(f"{self.name} borrowed {book.title}, due on {due_date.date()}")
        else:
            print(f"{book.title} is not available.")

    def return_book(self, book, library):
        for t in self.borrowed_books:
            if t.book == book and t.action == "borrow":
                book.return_book()
                transaction = Transaction(self, book, "return")
                library.transactions.append(transaction)
                self.borrowed_books.remove(t)
                print(f"{self.name} returned {book.title}")
                return
        print(f"{self.name} has not borrowed {book.title}")

    def __str__(self):
        return f"Member: {self.name} (ID: {self._member_id})"

    def __len__(self):
        return len(self.borrowed_books)

class Librarian(Member):  
    def __init__(self, name, member_id):
        super().__init__(name, member_id)

    def add_book(self, library, book):
        library.books.append(book)
        print(f"Librarian {self.name} added {book.title}")

    def remove_book(self, library, isbn):
        for book in library.books:
            if book.isbn == isbn:
                library.books.remove(book)
                print(f"Librarian {self.name} removed {book.title}")
                return
        print("Book not found.")


class Transaction:
    def __init__(self, member, book, action, due_date=None):
        self.member = member
        self.book = book
        self.action = action  
        self.date = datetime.now()
        self.due_date = due_date

    def __str__(self):
        if self.action == "borrow":
            return f"{self.member.name} borrowed {self.book.title} (Due: {self.due_date.date()})"
        else:
            return f"{self.member.name} returned {self.book.title} on {self.date.date()}"


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.members = []
        self.transactions = []

    def search_book(self, keyword):
        results = [book for book in self.books 
                   if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]
        return results

    def __str__(self):
        return f"Library: {self.name} | Books: {len(self.books)} | Members: {len(self.members)}"

    def __len__(self):
        return len(self.books)



if __name__ == "__main__":
   
    library = Library("Central Library")

    
    librarian = Librarian("Alice", "L001")

    b1 = Book("Python Programming", "Guido van Rossum", "111")
    b2 = Book("Data Structures", "Robert Lafore", "222")
    librarian.add_book(library, b1)
    librarian.add_book(library, b2)

  
    m1 = Member("John", "M001")
    library.members.append(m1)

 
    m1.borrow_book(b1, library)
    m1.return_book(b1, library)

    
    print("\nSearch Results for 'python':")
    for book in library.search_book("python"):
        print(book)

   
    print("\nTransaction History:")
    for t in library.transactions:
        print(t)

