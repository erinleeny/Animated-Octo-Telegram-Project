#Team Lach On (Maddy Andersen, Dean Carey, Kelly Huang, Erin Lee)
#SoftDev -- Rona Ed.
#Due 01-04-2021

import sqlite3
from flask import Flask, render_template, session
from flask import request  
import os
from db_builder import create_user

app = Flask(__name__)
app.secret_key = os.urandom(32) #set up session secret key

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
    create_user(first_name, last_name, username, password)
    session["username"] = username
    session["password"] = password
    session["method"] = method
    return render_template('profile.html', fName=first_name, lName=last_name, name=username, password=password, method=method)

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

   # if(username != user): 
   #     if(password != passw): #both password and username wrong
   #           return render_template('error.html', message="Incorrect username and password")
   #     return render_template('error.html', message="Incorrect username")
   # if(password != passw):
   #     return render_template('error.html', message="Incorrect password")
    session["username"] = username
    session["password"] = password
    session["method"] = method
    return render_template('profile.html', name=username, password=password, method=method)  #response to a form submission

if __name__ == "__main__":  # true if this file NOT imported
  app.debug = True        # enable auto-reload upon code change
  app.run()









