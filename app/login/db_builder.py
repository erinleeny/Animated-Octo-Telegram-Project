#Team LachOn

import sqlite3
import random

#open db if exists, otherwise create
db = sqlite3.connect("blog")

c = db.cursor() #facilitate db ops

#c.execute("CREATE TABLE users(user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT, password TEXT)")
#c.execute("CREATE TABLE blogs(blog_id INTEGER PRIMARY KEY, name TEXT, description TEXT, user_id INTEGER, creation_date TEXT)")
#c.execute("CREATE TABLE entries(entry_id INTEGER PRIMARY KEY, blog_id INTEGER, title TEXT, content TEXT, creation_date TEXT)")
#c.execute("INSERT INTO users VALUES(0, 'LachOn', 'Team', 'LachOn', 'tester')")

def create_user(first_name, last_name, username, password, user_id):
	db = sqlite3.connect("blog")

	c = db.cursor() #facilitate db ops

	c.execute("INSERT INTO entries VALUES(?, ?, ?, ?, ?)", (user_id, username, first_name, last_name, password))
	db.commit() #save changes
	db.close()

def authenticate_user(username, password):
	db = sqlite3.connect("blog")
	c = db.cursor() #facilitate db ops
	print("hello")
	result_set = c.execute("SELECT user_id, first_name, last_name FROM users WHERE username= ? AND password = ? ", (username, password))
	db.commit() #save changes
	db.close()
	return result_set

def create_blog(blog_id, name, description, user_id, creation_date):
    db = sqlite3.connect("blog")

    c = db.cursor() #facilitate db ops

    c.execute("INSERT INTO blogs VALUES(?, ?, ?, ?, ?)", (blog_id, name, description, user_id, creation_date))

    db.commit() #save changes
    db.close()


def create_entry(entry_id, blog_id, title, content, creation_date):
    db = sqlite3.connect("blog")

    c = db.cursor() #facilitate db ops

    c.execute("INSERT INTO entries VALUES(?, ?, ?, ?, ?)", (entry_id, blog_id, title, content, creation_date))

    db.commit() #save changes
    db.close()

def list_blogs(user_id):
    db = sqlite3.connect("blog")
    c = db.cursor() #facilitate db ops
    c.execute("SELECT blog_id, name, description FROM blogs WHERE user_id= " + str(user_id))
    data = c.fetchall()
    blogs = []
    for d in data:
        blog = {}
        blog["blog_id"]=d[0]
        blog["name"]=d[1]
        blog["description"]=d[2]
        blogs.append(blog)
    db.commit() #save changes
    db.close()
    return blogs

def list_entries(blog_id):
    db = sqlite3.connect("blog")
    c = db.cursor() #facilitate db ops
    c.execute("SELECT blog_id, title, content FROM entries WHERE blog_id= " + str(blog_id))
    data = c.fetchall()
    entries = []
    for d in data:
        entry = {}
        entry["blog_id"]=d[0]
        entry["title"]=d[1]
        entry["content"]=d[2]
        entries.append(entry)
    db.commit() #save changes
    db.close()
    return entries
