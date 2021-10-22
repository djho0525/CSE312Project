import mysql.connector as mysql
import os
from User import User

u = 'sqluser'   # os.environ['DB_USERNAME']
p = 'sqluserpassword'   # os.environ['DB_PASSWORD']
db = mysql.connect(user=u, password=p, database='cse312_project')
cur = db.cursor()


def setupTable():
    cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT, name TEXT)")

def resetTable():
    cur.execute("DROP TABLE users")
    setupTable()


def addUser(email, password, name):
    cur.execute("INSERT INTO users (email, password, name) VALUES (%s, %s, %s)", (email, password, name))
    db.commit()

def removeUser(email):
    cur.execute("DELETE FROM users WHERE email=%s", (email,))
    db.commit()


def userExists(email):
    cur.execute("SELECT email FROM users")
    emails = list(i[0] for i in cur.fetchall())
    return email in emails

def getUser(email):
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    row = cur.fetchone()
    return User(row[0], row[1], row[2])


if __name__ == '__main__':
    resetTable()
    addUser('email@gmail.com', 'password', 'test')
    cur.execute("SELECT * FROM users")
    for x in cur.fetchall(): print(x)

    db.close()
