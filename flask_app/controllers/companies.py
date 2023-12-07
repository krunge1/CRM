from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models import user, company, contact

    #Create
@app.route('/company/new', methods=['POST'])
def create_company ():
    data = request.form
    if company.Company.create(data):
        return redirect('/dashboard')
    return redirect('/company/new')

    #Read
@app.route('company/new')
def new_company():
    return render_template('new_company.html')

    #Update
    #Delete
