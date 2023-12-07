from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)
from pprint import pprint

class Company:
    db = "crm"

    def __init__(self, data):
        self.name = data['name']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.zip_code = data['zip_code']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #Create
    # @classmethod
    # def create(cls, data):
    #     if not cls.validate_sighting_data(data):
    #         pprint(data['number_of_sasquatches'])
    #         return False
    #     query = """INSERT INTO sightings (location, what_happened, date_of_sighting, number_of_sasquatches, user_id) 
    #     VALUES (%(location)s, %(what_happened)s, %(date_of_sighting)s, %(number_of_sasquatches)s, %(user_id)s)
    #     ;
    #     """
    #     result = connectToMySQL(cls.db).query_db(query, data)
        # return result
    #Read

    #Update
    #Delete