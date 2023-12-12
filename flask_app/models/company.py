from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re
from pprint import pprint

from flask_app.models import user, contact

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
        self.user_id = data['user_id']
        self.account_representative = None
        self.contacts = []

    #Create
    @classmethod
    def create(cls, data):
        if not cls.validate_company_data(data):
            pprint(data['name'])
            return False
        query = """INSERT INTO companies (name, address, city, state, zip_code, user_id) 
        VALUES (%(name)s, %(address)s, %(city)s, %(state)s, %(zip_code)s, %(user_id)s)
        ;
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @staticmethod # VALIDATE company
    def validate_company_data(data): 
        is_valid = True
        if len(data['name'])<1:
            flash('Name of company must be provided.')
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
        return is_valid
    #Read
    @classmethod # Get all companies
    def get_all_companies(cls):
        query = """SELECT * from companies
        LEFT JOIN users
        ON companies.user_id = users.id

        LEFT JOIN contacts
        ON companies.id = contacts.company_id
        ;
        """
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return []
        all_companies = []
        for i in range(len(results)):
            if results[i]["id"] != results[i-1]["id"] or i == 0:
                this_company = cls(results[i])
                all_companies.append(this_company)

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
            this_company.account_representative = account_representative
            if results[i]['contacts.id'] is not None:
                contact_data = {
                    "id": results[i]['contacts.id'],
                    "first_name": results[i]['contacts.first_name'],
                    "last_name": results[i]['contacts.last_name'],
                    "email": results[i]['contacts.email'],
                    "phone_number" : results[i]['contacts.phone_number'],
                    "address" : results[i]['contacts.address'],
                    "city" : results[i]['contacts.city'],
                    "state" : results[i]['state'],
                    "zip_code" : results[i]['contacts.zip_code'],
                    "user_id" : results[i]['user_id'],
                    "company_id" : results[i]['company_id'],
                    "created_at": results[i]['users2.created_at'],
                    "updated_at": results[i]['users2.updated_at'],
                    }
                contact = user.User(contact_data)
                this_company.contacts.append(contact)
        return all_companies


    #Update
    #Delete