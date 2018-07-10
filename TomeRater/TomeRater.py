class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {} #Book as key, rating as value

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("{n}'s email has been updated to {e}".format(n=self.name, e=self.email))

    def __repr__(self):
        print("User {name}, email: {email}, books read: {books}".format(name=self.name, email=self.email, books=len(self.books)))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating=None):
        if rating == None or (rating >= 0 and rating <= 4):
            self.books[book] = rating
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        sum_rating = 0
        count = 0
        for book in self.books.values():
            if book != None:
                sum_rating += book
                count += 1
        try: #For if and when the user hasn't rated any books
            rating_avg = sum_rating / count
        except ZeroDivisionError:
            rating_avg = 0
        return rating_avg

class Book(object):
    def __init__(self, title, isbn, price=None):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def get_price(self):
        return self.price

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("The ISBN of this book has been updated to {}".format(self.isbn))

    def add_rating(self, rating):
        if rating == None or (rating >= 0 and rating <= 4):
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_average_rating(self):
        sum_rating = 0
        count = 0
        for rating in self.ratings:
            if rating != None:
                sum_rating += rating
                count += 1
        try:
            rating_avg = sum_rating / count
        except ZeroDivisionError:
            rating_avg = 0
        return rating_avg

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn, price=None):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        print("{title} by {author}".format(title=self.title, author=self.author))

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price=None):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        print("{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject))

class TomeRater:
    def __init__(self):
        self.users = {} #email as key and user as value
        self.books = {} #book as key and number of reads as value
        self.isbn_list = [] #used to check for unique isbns

    def __repr__(self):
        self.print_catalog()
        self.print_users()

    def __eq__(self, other_rater):
        return self.users == other_rater.users and self.books == other_rater.books

    def create_book(self, title, isbn, price=None):
        if not isbn in self.isbn_list:
            self.isbn_list.append(isbn)
            return Book(title, isbn, price)
        else:
            print("Duplicate ISBN")

    def create_novel(self, title, author, isbn, price=None):
        if not isbn in self.isbn_list:
            self.isbn_list.append(isbn)
            return Fiction(title, author, isbn, price)
        else:
            print("Duplicate ISBN")

    def create_non_fiction(self, title, subject, level, isbn, price=None):
        if not isbn in self.isbn_list:
            self.isbn_list.append(isbn)
            return Non_Fiction(title, subject, level, isbn, price)
        else:
            print("Duplicate ISBN")

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users.keys():
            if rating == None or (rating >= 0 and rating <= 4):
                self.users[email].read_book(book, rating)
                book.add_rating(rating)
                if not book in self.books:
                    self.books[book] = 1
                elif book in self.books:
                    self.books[book] += 1
            else:
                print("Invalid Rating")
        else:
            print("No user with email {}".format(email))

    def add_user(self, name, email, user_books=None):
        if not email in self.users.keys():
            if '@' in email and ('.com' in email or '.edu' in email or '.org' in email):
                self.users[email] = User(name, email)
                if user_books != None:
                    for book in user_books:
                        self.add_book_to_user(book, email)
            else:
                print("Invalid email address.")
        else:
            print("User already exists.")

    def print_catalog(self):
        print("TomeRater catalog has the following books:")
        for book in self.books.keys():
            if type(book) == Book:
                book.get_title()
            if type(book) == Fiction or type(book) == Non_Fiction:
                book.__repr__()

    def print_users(self):
        print("The users of TomeRater are:")
        for user in self.users.values():
            user.__repr__()

    def get_most_read_book(self):
        bk = None
        num_read = float('-inf')
        for book, num in self.books.items():
            if num > num_read:
                num_read = num
                bk = book
        return bk.title

    def highest_rated_book(self):
        bk = None
        avg_rt = float('-inf')
        for book in self.books.keys():
            if book.get_average_rating() > avg_rt:
                avg_rt = book.get_average_rating()
                bk = book
        return bk.title

    def most_positive_user(self):
        positive_user = None
        avg_rt = float('-inf')
        for user in self.users.values():
            if user.get_average_rating() > avg_rt:
                avg_rt = user.get_average_rating()
                positive_user = user
        return positive_user.name

    def get_n_most_read_books(self, n):
        unsorted = []
        for key, value in self.books.items():
            unsorted += [[value, key.title]]
        unsorted.sort(reverse=True)
        sorted = []
        for i in range(int(n)):
            sorted.append(unsorted[i][1])
        if len(sorted) > 1:
            return "The {n} most read books are {book1} and {book2}.".format(n=n, book1=', '.join(sorted[0:len(sorted)-1]), book2=sorted[-1])
        else:
            return "The most read book is {}.".format(sorted)

    def get_n_most_prolific_readers(self, n):
        unsorted = []
        for user in self.users.values():
            unsorted += [[len(user.books), user.name]]
        unsorted.sort(reverse=True)
        sorted = []
        for i in range(int(n)):
            sorted.append(unsorted[i][1])
        if len(sorted) > 1:
            return "The {n} most prolific readers are {user1} and {user2}.".format(n=n, user1=', '.join(sorted[0:len(sorted)-1]), user2=sorted[-1])
        else:
            return "The most prolific reader is {}.".format(sorted[0])

    def get_n_most_expensive_books(self, n):
        unsorted = []
        for book in self.books.keys():
            unsorted += [[book.price, book.title]]
        unsorted.sort(reverse=True)
        sorted = []
        for i in range(int(n)):
            sorted.append(unsorted[i][1])
        if len(sorted) > 1:
            return "The {n} most expensive books are {book1} and {book2}.".format(n=n, book1=', '.join(sorted[0:len(sorted)-1]), book2=sorted[-1])
        else:
            return "The most expensive book is {}.".format(sorted)

    def get_worth_of_user(self, user_email):
        sum = 0
        for book in self.users[user_email].books.keys():
            sum += book.price
        return "Cost of all the books read by {name} is ${sum}.".format(sum=sum, name=self.users[user_email].name)

    def add_rating_to_book(self, email, book, rating): #Used to add rating in TomeRater
        if email in self.users.keys(): #Check if uesr exist
            if book in self.users[email].books.keys(): #Check if user read the book
                if self.users[email].books[book] == None: #Check if user has rated the book
                    if rating == None or (rating >= 0 and rating <= 4):
                        self.users[email].read_book(book, rating) #Add rating to user
                        book.add_rating(rating) #Add rating to book
                        print("{name} now gave {book} a rating of {rating}".format(name=self.users[email].name, book=book.title, rating=rating))
                    else:
                        print("Invalid Rating")
            else:
                print("User haven't read {}.".format(book.title))
        else:
            print("No such user.")

    def change_rating(self, email, book, new_rating): #Used to change rating in TomeRater
        if new_rating == None or (new_rating >= 0 and new_rating <= 4):
            if email in self.users.keys(): #Check if uesr exist
                if book in self.users[email].books.keys(): #Check if user read the book
                    if self.users[email].books[book] != None: #Check if user has rated the book
                        old_rating = self.users[email].books[book] #Retrive old rating in order to locate rating in book object
                        self.users[email].books[book] = new_rating #Replace rating in user
                        book.ratings[book.ratings.index(old_rating)] = new_rating #Replace rating in book
                        print("{name} now changed the rating of {book} from {old_rating} to {rating}".format(name=self.users[email].name, book=book.title, rating=new_rating, old_rating=old_rating))
                    else:
                        print("User hasn't rated the book yet")
                        self.users[email].read_book(book, rating) #Add rating to user
                        book.add_rating(rating)
                        print("{name} now gave {book} a rating of {rating}".format(name=self.users[email].name, book=book.title, rating=new_rating))
                else:
                    print("User hasn't read {}.".format(book.title))
            else:
                print("No such user.")
        else:
            print("Invalid Rating")
        #Find user's original rating and book's original rating
        #Update the list
