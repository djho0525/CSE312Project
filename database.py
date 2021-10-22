import mysql.connector as mysql
import os

u = 'sqluser'   # os.environ['DB_USERNAME']
p = 'sqluserpassword'   # os.environ['DB_PASSWORD']
db = mysql.connect(user=u, password=p, database='cse312_project')
cur = db.cursor()


def setupTable():
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

def resetTable():
    cur.execute("DROP TABLE users")
    setupTable()


def addUser(username, password):
    if userExists(username): print('username taken')
    else: cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()

def removeUser(username):
    if not userExists(username): print('user does not exist')
    cur.execute("DELETE FROM users WHERE username=%s", (username,))
    db.commit()


def userExists(username):
    cur.execute("SELECT username FROM users")
    usernames = list(i[0] for i in cur.fetchall())
    return username in usernames


if __name__ == '__main__':
    resetTable()
    addUser('test', 'password')
    cur.execute("SELECT * FROM users")
    for x in cur.fetchall(): print(x)

    db.close()
