#Team LachOn

import sqlite3
import random

#open db if exists, otherwise create
db = sqlite3.connect("blog")

c = db.cursor() #facilitate db ops

#c.execute("CREATE TABLE users(user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT)")
#c.execute("CREATE TABLE blogs(blog_id INTEGER PRIMARY KEY, name TEXT, user_id INTEGER, creation_date TEXT)")
#c.execute("CREATE TABLE entries(entry_id INTEGER PRIMARY KEY, blog_id INTEGER, title TEXT, content TEXT)")
#c.execute("INSERT INTO users VALUES(0, 'LachOn', 'Team', 'LachOn', 'tester')")

def create_user(first_name, last_name, username, password): 
	user_id = str(random.randint(0,10000000))
	db = sqlite3.connect("blog")

	c = db.cursor() #facilitate db ops

	c.execute("INSERT INTO users VALUES(" + user_id + ",'" + first_name + "','" + last_name + 
	"','" + username + "','" + password + "');")

	db.commit() #save changes
	db.close()


def create_blog(name, user_id, creation_date):
        blog_id = str(random.randint(0,10000000))
        db = sqlite3.connect("blog")

        c = db.cursor() #facilitate db ops

        c.execute("INSERT INTO users VALUES('" + name + "'," + user_id + ",'" + creation_date + "');")

        db.commit() #save changes
        db.close()


def create_entry(blog_id, title, creation_date):
        entry_id = str(random.randint(0,10000000))
        db = sqlite3.connect("blog")

        c = db.cursor() #facilitate db ops

        c.execute("INSERT INTO users VALUES(" + entry_id + "," + user_id + ",'" + title +
        "', '', '" + creation_date + "');")

        db.commit() #save changes
        db.close()
