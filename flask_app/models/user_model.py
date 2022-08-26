from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE # import database defined in __init__
from flask_app.models import user_model # import the award model to complete join
from flask_app.models import book_model 
from flask import flash # needs to be called upon for validation
import re       
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$")

class User: # DONT EDIT
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # CREATE/REGISTER/ DONT EDIT
    @classmethod 
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # CHECKING IF EMAILS ALREADY EXIST
    @classmethod 
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1: 
            return False
        return cls(results[0])

    # GET ONE 
    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM users JOIN books on users.id = books.user_id  WHERE users.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1: 
            return False
        user = cls(results[0])
        list_of_books = []
        for row in results:
            book_data = {
                **row,
                'id': row['books.id'],
                'created_at': row['books.created_at'],
                'updated_at': row['books.updated_at']
            }
            this_book = book_model.Books(book_data)
            list_of_books.append(this_book)
        user.books = list_of_books
        return user

    # VALIDATION
    @staticmethod
    def validate_reg(register, category):
        is_valid=True
        if len(register['first_name']) < 2:
            is_valid=False
            flash("First name must be at least 2 characters", "err_first")
        if len(register['last_name']) < 2:
            is_valid=False
            flash("Last name must be at least 2 characters", "err_last")
        if len(register['email']) < 1:
            is_valid = False
            flash("Please provide your email", "err_email")
        elif not EMAIL_REGEX.match(register['email']):
            is_valid = False
            flash("Invalid email", "err_invalid")
        else:
            data = {
                'email': register['email']
            }
            potential_user = User.get_by_email(data)
            if potential_user: # if we have a user, dont let them register with this email
                is_valid = False
                flash("Email already taken", "err_taken")
        if len(register['password']) < 8: # validating password
            is_valid = False
            flash("Password must be at least 8 characters", "err_pass")
        elif not register['password'] == register['confirm_password']: # comparing password to confirm it's the same
            is_valid = False
            flash("passwords don't match", "err_match")
        return is_valid

