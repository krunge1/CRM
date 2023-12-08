from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models import user

#Create
@app.route('/', methods = ["POST"])
def loginUser():
    #run login function
    if user.User.login(request.form):
        return redirect('/dashboard')
    return redirect ('/')

@app.route('/register', methods = ["POST"])
def createUser():
    #run registration activity
    if user.User.create(request.form):
        return redirect('/dashboard')
    return redirect('/register')

#Read
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#Update
#Method to update user profile

#Method for admin to update user profile


#Delete
#Method for admin to delete user profile