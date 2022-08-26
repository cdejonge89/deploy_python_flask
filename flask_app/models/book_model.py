from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE # import database defined in __init__
from flask_app.models import user_model # import the award model to complete join
from flask import flash

class Books:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    # CREATE LIST
    @classmethod 
    def create(cls, data):
        query = "INSERT INTO books (title, author, user_id) VALUES (%(title)s, %(author)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    #UPDATE/EDIT LIST
    @classmethod
    def update(cls, data):
        query = "UPDATE books SET title = %(title)s, author = %(author)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # GET ALL
    @classmethod 
    def get_all(cls):
        query = "SELECT * FROM books JOIN users on users.id = books.user_id;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results: 
            all_books = []
            for row in results:
                this_book = cls(row)
                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                this_book = user_model.User(user_data)
                this_book.planner = this_user
                all_books.append(this_book)
            return all_books
        return results

    # DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # GET ONE 
    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM users JOIN books on users.id = books.user_id  WHERE users.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1: 
            return False
        return cls(results[0])

    # GET BOOK BY ID
    @classmethod 
    def get_book_by_id(cls, data):
        query = "SELECT * FROM books WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1: 
            return False
        return cls(results[0])

    # FORM VALIDATION
    @staticmethod 
    def validator(form_data):
        is_valid = True
        if len(form_data['title']) < 2:
            is_valid = False
            flash("Please enter a Title/Author")
        return is_valid