from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

class User:
    db = "crm"

    def __init__(self,data):
        self.id = data['id']
        self.user_name = data['user_name']
        self.email = data['email']
        self.password = data['password']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.user_level = data['user_level']
        self.user_status = data['user_status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#Create
    @classmethod
    def create(cls, data):
        if not cls.validate_user_registration_data(data):
            return False
        parsed_data = cls.parse_user_registration_data(data)
        query = """INSERT INTO users (user_name, email, password, first_name, last_name)
        VALUES (%(user_name)s, %(email)s, %(password)s, %(first_name)s, %(last_name)s);"""
        results = connectToMySQL(cls.db).query_db(query, parsed_data)
        this_user = User.get_user_by_email(data['email'].lower())
        session['first_name'] = this_user.first_name
        session['last_name'] = this_user.last_name
        session['id'] = this_user.id
        return True

    @staticmethod # VALIDATE user
    def validate_user_registration_data(data): 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^.{8}$')
        is_valid = True
        if len(data['first_name'])<2:
            flash('Your first name must be at least two characters long.')
            is_valid = False
        if len(data['last_name'])<2:
            flash('Your last name must be at least two characters long.')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Please use a real email address.')
            is_valid = False
        if User.get_user_by_email(data['email'].lower()):
            flash("That email is already in use")
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash('Your password must be at least eight characters long.')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Your passwords do not match')
            is_valid = False
        return is_valid
    
    @staticmethod
    def parse_user_registration_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data ['first_name']
        parsed_data['last_name'] = data ['last_name']
        parsed_data['user_name'] = data ['user_name'].lower()
        parsed_data['email'] = data['email'].lower()
        parsed_data['password'] = bcrypt.generate_password_hash(data ['password'])
        return parsed_data

#Read
    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'].lower())
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['first_name'] = this_user.first_name
                session['last_name'] = this_user.last_name
                session['id'] = this_user.id
                return True
        else:
            flash('Your login information is incorrect.')

    @classmethod
    def get_user_by_email(cls, email):
        data = {
            'email': email
        }
        query = """SELECT * 
        FROM users 
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result
#Update
#Delete