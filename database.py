import mysql.connector as mysql
import os
from User import User

u = 'sqluser'   # os.environ['DB_USERNAME']
p = 'sqluserpassword'   # os.environ['DB_PASSWORD']
db = mysql.connect(user=u, password=p, database='cse312_project')
cur = db.cursor(prepared=True)

users = {}      # {email: User object}

def setupTable():
    cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT, name TEXT)")

def resetTable():
    cur.execute("DROP TABLE users")
    setupTable()


def addUser(email, password, name):
    cur.execute("INSERT INTO users (email, password, name) VALUES (%s, %s, %s)", (email, password, name))
    db.commit()
    userSetup(email)

def removeUser(email):
    cur.execute("DELETE FROM users WHERE email=%s", (email,))
    db.commit()


def userExists(email):
    cur.execute("SELECT email FROM users")
    emails = list(i[0] for i in cur.fetchall())
    return email in emails

def userSetup(email):
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    row = cur.fetchone()
    if email not in users: users[email] = User(row[0], row[1], row[2])

def getUser(email):
    userSetup(email)
    return users[email]

def addMessage(receiver, sender, message):
    if receiver not in users[sender].messages: users[sender].messages[receiver] = []
    users[sender].messages[receiver].append(message)
    if sender not in users[receiver].messages: users[receiver].messages[sender] = []
    users[receiver].messages[sender].append(message)


if __name__ == '__main__':
    # resetTable()
    # addUser('email@gmail.com', 'password', 'test')
    cur.execute("SELECT * FROM users")
    for x in cur.fetchall(): print(x)
    print(users)

    db.close()
