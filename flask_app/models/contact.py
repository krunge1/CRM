from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re
from pprint import pprint

from flask_app.models import user, company

class Contact:
    db = "crm"

    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone_number = data['phone_number']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.zip_code = data['zip_code']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.company_id = data['company_id']

    #Create
    @classmethod
    def create_contact(cls, data):
        if not cls.validate_contact_data(data):
            pprint(data['first_name'])
            return False
        query = """INSERT INTO contacts (first_name, last_name, email, phone_number, address, city, state, zip_code, user_id, company_id) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(address)s, %(city)s, %(state)s, %(zip_code)s, %(user_id)s, %(company_id)s)
        ;
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @staticmethod # VALIDATE contact
    def validate_contact_data(data): 
        is_valid = True
        if len(data['first_name'])<1:
            flash('First name must be provided.')
            is_valid = False
        if len(data['last_name'])<1:
            flash('Last name must be provided.')
            is_valid = False
        if len(data['email'])<1:
            flash('An email must be provided.')
            is_valid = False
        if len(data['phone_number'])<1:
            flash('A phone number must be provided.')
            is_valid = False
        if len(data['address'])<1:
            flash('Address must be provided.')
            is_valid = False
        if len(data['city'])<1:
            flash('City must be provided.')
            is_valid = False
        if len(data['state'])<1:
            flash('State must be provided.')
            is_valid = False
        if len(data['zip_code'])<1:
            flash('Zip code must be provided.')
            is_valid = False
        if len(data['company_id'])<1:
            flash('A company must be chosen.')
            is_valid = False
        return is_valid

    # Read
    @classmethod # Get all contacts
    def get_all_contacts(cls):
        query = """SELECT * from contacts
        LEFT JOIN users
        ON contacts.user_id = users.id

        LEFT JOIN companies
        ON contacts.id = companies.contact_id
        ;
        """
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return []
        all_contacts = []
        for i in range(len(results)):
            if results[i]["id"] != results[i-1]["id"] or i == 0:
                this_contact = cls(results[i])
                all_contacts.append(this_contact)

            account_rep_data = {
                    "id": results[i]['users.id'],
                    "user_name" : results[i]['user_name'],
                    "first_name": results[i]['first_name'],
                    "last_name": results[i]['last_name'],
                    "email": results[i]['email'],
                    "password": results[i]['password'],
                    "user_level" : results[i]['user_level'],
                    "user_status" : results[i]['user_status'],
                    "created_at": results[i]['users.created_at'],
                    "updated_at": results[i]['users.updated_at'],
                    }
            account_representative = user.User(account_rep_data)
            this_contact.user_id = account_representative
            company_data = {
                "id": results[i]['companies.id'],
                "name": results[i]['companies.name'],
                "address" : results[i]['companies.address'],
                "city" : results[i]['companies.city'],
                "state" : results[i]['companies.state'],
                "zip_code" : results[i]['companies.zip_code'],
                "password": results[i]['companies.password'],
                "created_at": results[i]['companies.created_at'],
                "updated_at": results[i]['companies.updated_at'],
                "user_id" : results[i]['companies.user_id']
                }
            this_company = company.Company(company_data)
            this_contact.company_id = this_company
        return all_contacts

    #Update
    #Delete