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

def setupUploadsTable():
    cur.execute("CREATE TABLE IF NOT EXISTS uploads (uploadID int NOT NULL AUTO_INCREMENT PRIMARY KEY, imagepath TEXT NOT NULL, likes INT NOT NULL DEFAULT 0)")

def resetUploadsTable():
    cur.execute("DROP TABLE users")
    setupUploadsTable()

def uploadImage(imagePath):
    #First Column will be auto-incremented Image ID
    #May need to add column for number of likes
    cur.execute("INSERT INTO uploads (imagepath) VALUES (%s)", (imagePath))
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
    cur.execute("SELECT imagepath FROM uploads WHERE uploadID = (%s)", uploadID)
    image = cur.fetchone()
    return image

def getLikesByID(uploadID):
    cur.execute("SELECT likes FROM uploads WHERE uploadID = (%s)", uploadID)
    likes = cur.fetchone()
    return likes

def addLike(uploadID):
    currentLikes = getLikesByID(uploadID)
    newLikes = currentLikes + 1
    cur.execute("UPDATE uploads SET likes = (%s) WHERE uploadID = (%s)", (newLikes, uploadID))
    cur.execute()

if __name__ == '__main__':
    resetTable()
    resetUploadsTable()
    # addUser('email@gmail.com', 'password', 'test')
    cur.execute("SELECT * FROM users")
    for x in cur.fetchall(): print(x)

    db.close()
