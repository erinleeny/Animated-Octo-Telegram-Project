#Team Lach On (Maddy Andersen, Dean Carey, Kelly Huang, Erin Lee)
#SoftDev -- Rona Ed.
#P0 - Da Art of Storytellin'(Pt.2)
#Due 01-08-2021

import sqlite3
from flask import Flask, render_template, session
from flask import request, redirect, url_for
import os
import random
from db_builder import create_user, authenticate_user, create_blog, create_entry, list_blogs, list_entries, update_blog, update_entry, list_users

app = Flask(__name__)
app.secret_key = os.urandom(32) #set up session secret key

@app.route("/", methods=['POST', 'GET'])
def home():
    if "username" in session:
        return render_template('profile.html', user_id=session['user_id'], fName= session["first_name"], lName= session["last_name"], name=session['username'], password=session['password'], blogs=list_blogs(session["user_id"]))
    if "blog_id" in session:
        session.pop("blog_id")
        session.pop("blog_name")
        session.pop("blog_description")
    return render_template('login.html', message="")
@app.route("/register", methods=['POST','GET'])
def register():
    return render_template('register.html')
@app.route("/create_user", methods=['POST','GET'])
def user():
    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    username=request.form["username"]
    password=request.form["password"]
    db = sqlite3.connect("blog")
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = '" + username + "'") #check to see whether user already exists
    check = c.fetchall()
    db.commit()
    db.close()
    if len(check) == 0:
        user_id = str(random.randint(0,10000000))
        create_user(first_name, last_name, username, password, user_id)
    else:
        return render_template('error.html', message="Username already exists")
        ## todo: direct to a different error page that takes you to sign up page
    session["username"] = username
    session["password"] = password
    session["user_id"] = user_id
    session["first_name"] = first_name
    session["last_name"] = last_name
    return render_template('profile.html', fName=first_name, lName=last_name, name=username, password=password, user_id=user_id)
# blog methods
@app.route(("/register_blog"), methods=["POST", "GET"])
def blog_register():
    return render_template('create_blog.html')
@app.route(("/edit_blog"), methods=["POST", "GET"])
def blog_edit():
    return render_template('edit_blog.html', description=session["blog_description"], name=session["blog_name"])
@app.route(("/save_blog"), methods=["POST", "GET"])
def blog_save():
    name=request.form["name"]
    description=request.form['description']
    update_blog(session["blog_id"], name, description)
    return redirect(url_for('show_existing_blog'))
@app.route(("/create_blog"), methods=["POST", "GET"])
def blog():
    #todo: some way to catch error if blog is blank or something
    name=request.form["name"]
    description=request.form['description']
    blog_id = str(random.randint(0,10000000))
    create_blog(blog_id, name, description, session["user_id"])
    return redirect(url_for('show_blog', blog_id=blog_id, name=name, description=description))
@app.route(("/show_blog"), methods=["POST", "GET"])
def show_blog():
    blog_id = request.args["blog_id"]
    name = request.args["name"]
    description = request.args["description"]
    session["blog_id"] = blog_id
    session["blog_name"] = name
    session["blog_description"] = description
    print(session["blog_id"])
    return redirect(url_for('show_existing_blog'))
@app.route(("/show_existing_blog"), methods=["POST", "GET"])
def show_existing_blog():
    if "id" in request.form:
        blog_id=request.form["id"]
    else:
        blog_id = session["blog_id"]
    db = sqlite3.connect("blog")
    c = db.cursor()
    c.execute("SELECT name, description FROM blogs WHERE blog_id=" + blog_id)
    data = c.fetchone()
    session["blog_id"] = blog_id
    session["blog_name"] = data[0]
    session["blog_description"] = data[1]
    return render_template('blog.html', blog_id=blog_id, name=data[0], description=data[1], username=session["username"], entries=list_entries(session["blog_id"]))

# entry methods
@app.route(("/create_entry"), methods=["POST", "GET"])
def entry_register():
    return render_template('create_entry.html')
@app.route(("/update_entry"), methods=["POST", "GET"])
def entry_update():
    title=request.form["entry_title"]
    content=request.form['content']
    update_entry(session["entry_id"], title, content)
    return redirect(url_for('show_existing_blog'))
@app.route(("/edit_entry"), methods=["POST", "GET"])
def entry_edit():
    entry_id=request.form["id"]
    db = sqlite3.connect("blog")
    c = db.cursor()
    c.execute("SELECT title, content FROM entries WHERE entry_id=" + entry_id)
    data_entries = c.fetchone()
    session["entry_id"]=entry_id
    return render_template('edit_entry.html', title=data_entries[0], content=data_entries[1])
@app.route(("/save_entry"), methods=["POST", "GET"])
def entry_save():
    entry_title=request.form["entry_title"]
    content=request.form['content']
    entry_id = str(random.randint(0,10000000))
    create_entry(entry_id, session["blog_id"], entry_title, content, "2021-01-06")
    return redirect(url_for('show_existing_blog'))

@app.route("/all", methods=['POST', 'GET'])
def all():
    if "id" in request.form:
        user_id=request.form["id"]
    else:
        user_id = session["user_id"]
    db = sqlite3.connect("blog")
    c = db.cursor()
    c.execute("SELECT user_id, username, first_name, last_name FROM users WHERE user_id !=" + str(user_id))
    data = c.fetchone()
    print(data[1])
    print(data[2])
    print(data[3])
    return render_template('masterlist.html', user_id = session['user_id'], users=list_users())

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop("username")
    session.pop("password")
    session.pop("first_name")
    session.pop("last_name")
    session.pop("user_id")
    return render_template('login.html', message="You have been successfully logged out.")

@app.route("/auth", methods=['POST', 'GET'])
def authenticate():
    username=request.form["username"]
    password=request.form["password"]
    db = sqlite3.connect("blog")
    c = db.cursor()
    c.execute("SELECT user_id, first_name, last_name FROM users WHERE username= ? AND password = ? ", (username, password))
    data = c.fetchall()
    # note to catch errors here
    if len(data) == 0:
        return render_template('error.html', message="Login Failed")
    for d in data:
        user_id = d[0]
        first_name = d[1]
        last_name = d[2]
    session["username"] = username
    session["password"] = password
    session["user_id"] = user_id
    session["first_name"] = first_name
    session["last_name"] = last_name
    return render_template('profile.html', user_id=user_id, name=username, fName=first_name, lName=last_name, password=password, data=list_blogs(session["user_id"]), blogs=list_blogs(user_id))  #response to a form submission

if __name__ == "__main__":  # true if this file NOT imported
  app.debug = True        # enable auto-reload upon code change
  app.run()
