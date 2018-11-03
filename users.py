from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import connectToMySQL

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+$')

mysql = connectToMySQL('users_flask')

app = Flask(__name__)
app.secret_key = "Secretusers"

@app.route('/')
@app.route('/users')
def index():
    query = f"SELECT * FROM users;"
    users = mysql.query_db(query)
    return render_template("userindex.html", users = users)

@app.route('/users/new')
def new():
    return render_template("newuser.html")

@app.route('/users/create', methods = ['POST'])
def create():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']

    if len(first_name) < 2:
        flash(u"The first name should be two or more characters long.", 'first_name')
    elif not name_regex.match(first_name):
        flash(u"The first name should not contain any numbers"
        " or any special characters.", 'first_name')
    
    if len(last_name) < 2:
        flash(u"The last name should be two or more characters long.", 'last_name')
    elif not name_regex.match(last_name):
        flash(u"The last name should not contain any numbers"
        " or any special characters.", 'last_name')
    
    query = "SELECT EXISTS (SELECT * FROM users WHERE email = %(email)s) AS email"
    data = {
        'email': email
    }
    emailisthere = mysql.query_db(query, data)
        
    if len(email) < 1:
        flash(u"Email cannot be blank.", 'email')
    elif not EMAIL_REGEX.match(email):
        flash(u"Invalid Email Address.", 'email')
    elif emailisthere[0]['email'] != 0:
        flash("The email already exists in the system. Please type another one.")
    
    if '_flashes' in session.keys():
        return redirect("/users/new")
    else:
        query_new = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        mysql.query_db(query_new, data)

        return redirect("/users")

@app.route('/users/<id>')
def show(id):
    query = f"select * from users where id = {id}"
    user = mysql.query_db(query)
    return render_template("showuser.html", user = user)

@app.route('/users/<id>/edit')
def edit(id):
    query = f"select * from users where id = {id}"
    user = mysql.query_db(query)
    return render_template("edituser.html", user = user)

@app.route('/users/<id>/delete')
def delete(id):
    query = f"delete from users where id = {id}"
    mysql.query_db(query)
    return redirect("/users")

@app.route('/users/<id>', methods = ['POST'])
def edituser(id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']

    if len(first_name) < 2:
        flash(u"The first name should be two or more characters long.", 'first_name')
    elif not name_regex.match(first_name):
        flash(u"The first name should not contain any numbers"
        " or any special characters.", 'first_name')
    
    if len(last_name) < 2:
        flash(u"The last name should be two or more characters long.", 'last_name')
    elif not name_regex.match(last_name):
        flash(u"The last name should not contain any numbers"
        " or any special characters.", 'last_name')
    
    query = "SELECT EXISTS (SELECT * FROM users WHERE email = %(email)s) AS email"
    data = {
        'email': email
    }
    emailisthere = mysql.query_db(query, data)
        
    if len(email) < 1:
        flash(u"Email cannot be blank.", 'email')
    elif not EMAIL_REGEX.match(email):
        flash(u"Invalid Email Address.", 'email')
    elif emailisthere[0]['email'] != 0:
        flash("The email already exists in the system. Please type another one.")
    
    if '_flashes' in session.keys():
        return redirect("/users/" + id + "/edit") 
    else:
        query_edit= f"update users set first_name = '{first_name}', last_name = '{last_name}', email = '{email}', updated_at = NOW() where id = {id}"
        mysql.query_db(query_edit)

        return redirect("/users")

if __name__=="__main__":
    app.run(debug = True) 

