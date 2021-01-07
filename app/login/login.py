#Team Lach On (Maddy Andersen, Dean Carey, Kelly Huang, Erin Lee)
#SoftDev -- Rona Ed.
#Due 01-04-2021

import sqlite3
from flask import Flask, render_template, session
from flask import request  
import os
import random
from db_builder import create_user, authenticate_user, create_blog

app = Flask(__name__)
app.secret_key = os.urandom(32) #set up session secret key
#c = db.cursor() #facilitate db ops
user = "lacher"
passw = "pass"

@app.route("/") 
def test_tmplt():
    if "username" in session:
        return render_template('profile.html', name=session['username'], password=session['password'],method=session['method'])
    return render_template('login.html', message="")

@app.route("/register", methods=['POST','GET'])
def register():
    return render_template('register.html')

@app.route("/create_user", methods=['POST','GET'])
def user():
    method=request.method
    if method == "POST":
        first_name=request.form["first_name"]
        last_name=request.form["last_name"]
        username=request.form["username"]
        password=request.form["password"]
    else:
        first_name=request.args['first_name']
        last_name=request.args['last_name']
        username=request.args['username']
        password=request.args['password']
    user_id = str(random.randint(0,10000000))
    create_user(first_name, last_name, username, password, user_id)
    session["username"] = username
    session["password"] = password
    session["method"] = method
    session["user_id"] = user_id
    return render_template('profile.html', fName=first_name, lName=last_name, name=username, password=password, user_id=user_id, method=method)

@app.route(("/register_blog"), methods=["POST", "GET"])
def blog_register():
    print(session["user_id"])
    return render_template('create_blog.html')
# @app.route("users/" + user_id, methods=['POST', 'GET'])
# def profile(user_id):
#     c = db.cursor()
#     c.execute("SELECT first_name, last_name, username FROM users WHERE user_id= ? ", (user_id))
@app.route(("/create_blog"), methods=["POST", "GET"])
def blog():
    #todo: some way to catch error if blog is blank or something
    method=request.method
    if method == "POST":
        name=request.form["blog_name"]
        description=request.form['description']
    else:
        name=request.args['name']
        description=request.args['description']
    blog_id = str(random.randint(0,10000000))
    create_blog(blog_id, name, description, session["user_id"], "2021-01-06")
    return render_template('blog.html', blog_id=blog_id, name=name, description=description, username=session["username"])
    
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop("username")
    session.pop("password")
    session.pop("method")
    return render_template('login.html', message="You have been successfully logged out.")

@app.route("/auth", methods=['POST', 'GET'])
def authenticate():
    method=request.method
    if method == "POST": 
        username=request.form["username"] 
        password=request.form["password"]
    else:
        username=request.args['username'] 
        password=request.args['password']

    ## todo: authenticate against the actual table of users, not hard-coded
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request.method)
    print("***DIAG: request.args ***")
    print(request.args)
    print("***DIAG: request.headers ***")
    print(request.headers)
    print("hello")
    db = sqlite3.connect("blog")
    c = db.cursor()
    c.execute("SELECT user_id, first_name, last_name FROM users WHERE username= ? AND password = ? ", (username, password))
    data = c.fetchall()
    # note to catch errors here
    if len(data) == 0:
        return render_template('error.html', message="user and password do not exist")
    for d in data:
        user_id = d[0]
        first_name = d[1]
        last_name = d[2]
   # if(username != user): 
   #     if(password != passw): #both password and username wrong
   #           return render_template('error.html', message="Incorrect username and password")
   #     return render_template('error.html', message="Incorrect username")
   # if(password != passw):
   #     return render_template('error.html', message="Incorrect password")
    session["username"] = username
    session["password"] = password
    session["method"] = method
    session["user_id"] = user_id
    return render_template('profile.html', user_id=user_id, name=username, fName=first_name, lName=last_name, password=password, method=method)  #response to a form submission

if __name__ == "__main__":  # true if this file NOT imported
  app.debug = True        # enable auto-reload upon code change
  app.run()









