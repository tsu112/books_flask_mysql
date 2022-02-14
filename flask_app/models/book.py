from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author


class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_who_favorited = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books"
        books = []
        results = connectToMySQL("books_flask").query_db(query)
        for row in results:
            books.append(cls(row))
        return books

    @classmethod
    def create(cls, data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        results = connectToMySQL(
            'books_flask').query_db(query, data)
        return results

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.books_id LEFT JOIN authors on authors.id = favorites.authors_id WHERE books.id = %(id)s;"
        results = connectToMySQL(
            'books_flask').query_db(query, data)

        favorite_book = cls(results[0])
        print(favorite_book)

        for row in results:
            if row['authors.id'] == None:
                break
            data = {
                "id": row['authors.id'],
                "name": row['name'],
                "created_at": row['authors.created_at'],
                "updated_at": row['authors.updated_at']
            }
            favorite_book.authors_who_favorited.append(author.Author(data))
            return favorite_book

    @classmethod
    def unfavorited_books(cls, data):
        query = "SELECT * FROM books WHERE books.id NOT IN ( SELECT books_id FROM favorites WHERE authors_id = %(id)s );"
        results = connectToMySQL('books_flask').query_db(query, data)
        books = []
        for row in results:
            books.append(cls(row))
        print(books)
        return books
