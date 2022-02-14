from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book


class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.favorite_books = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors"
        authors = []
        results = connectToMySQL("books_flask").query_db(query)
        for row in results:
            authors.append(cls(row))
        return authors

    @classmethod
    def create(cls, data):
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        results = connectToMySQL(
            'books_flask').query_db(query, data)
        return results

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.authors_id LEFT JOIN books ON books.id = favorites.books_id WHERE authors.id = %(id)s;"
        results = connectToMySQL(
            'books_flask').query_db(query, data)

        author = cls(results[0])
        for row in results:
            if row['books.id'] == None:
                break
            data = {
                "id": row['books.id'],
                "title": row['title'],
                "num_of_pages": row['num_of_pages'],
                "created_at": row['books.created_at'],
                "updated_at": row['books.updated_at']
            }
            author.favorite_books.append(book.Book(data))
        return author

    @classmethod
    def unfavorited_authors(cls, data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN ( SELECT authors_id FROM favorites WHERE books_id = %(id)s );"
        authors = []
        results = connectToMySQL('books_flask').query_db(query, data)
        for row in results:
            authors.append(cls(row))
        return authors

    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (authors_id,books_id) VALUES (%(author_id)s,%(book_id)s);"
        return connectToMySQL('books_flask').query_db(query, data)
