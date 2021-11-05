import mysql.connector as mysql
import os
from User import User

u = 'sqluser'   # os.environ['DB_USERNAME']
p = 'sqluserpassword'   # os.environ['DB_PASSWORD']
database = 'cse312_project'

db = mysql.connect(user=u, password=p)
cur = db.cursor(prepared=True)
# INITIALIZE DATABASE AND TABLES
cur.execute("CREATE DATABASE IF NOT EXISTS " + database)
db.database = database
cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT, name TEXT)")

users = {}      # {email: User object}

def dropUserTable():
    cur.execute("DROP TABLE users")

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

def loginUser(email):
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    row = cur.fetchone()
    users[email] = User(row[0], row[1], row[2])

def addMessage(receiver, sender, message):
    if receiver not in users[sender].messages: users[sender].messages[receiver] = []
    users[sender].messages[receiver].append(message)
    if sender not in users[receiver].messages: users[receiver].messages[sender] = []
    users[receiver].messages[sender].append(message)

def setupUploadsTable():
    cur.execute("CREATE TABLE IF NOT EXISTS uploads (uploadID int NOT NULL AUTO_INCREMENT PRIMARY KEY, imagepath TEXT NOT NULL, likes INT NOT NULL DEFAULT 0)")

def resetUploadsTable():
    cur.execute("DROP TABLE users")
    setupUploadsTable()

def uploadImage(imagePath):
    #First Column will be auto-incremented Image ID
    #May need to add column for number of likes
    cur.execute("INSERT INTO uploads (imagepath) VALUES (%s)", (imagePath,))
    db.commit()

def getAllImages():
    #Can limit the amount of images retrived
    #cur.execute("SELECT * FROM uploads LIMIT 10")
    cur.execute("SELECT * FROM uploads")
    images = cur.fetchall
    return images

def getAllImagePaths():
    #Can limit the amount of imagesPaths retrived
    #cur.execute("SELECT imagepath FROM uploads LIMIT 10")
    cur.execute("SELECT imagepath FROM uploads")
    imagesPaths = cur.fetchall
    return imagesPaths

def getImageByID(uploadID):
    cur.execute("SELECT imagepath FROM uploads WHERE uploadID = (%s)", (uploadID,))
    image = cur.fetchone()
    return image

def getLikesByID(uploadID):
    cur.execute("SELECT likes FROM uploads WHERE uploadID = (%s)", (uploadID,))
    likes = cur.fetchone()
    print(likes[0])
    return int(likes[0])

def addLike(uploadID):
    currentLikes = getLikesByID(uploadID)
    newLikes = currentLikes + 1
    print(newLikes)
    cur.execute("UPDATE uploads SET likes = (%s) WHERE uploadID = (%s)", (newLikes, uploadID))
    db.commit()

if __name__ == '__main__':
    # dropUserTable()
    # addUser('email@gmail.com', 'password', 'test')
    #uploadImage("/imageuploads/image1.jpg")
    #getAllImagePaths()
    #print(cur.fetchall())
    #getLikesByID(1)
    #addLike(1)
    cur.execute("SELECT * FROM users")
    for x in cur.fetchall(): print(x)
    print(users)

    db.close()
