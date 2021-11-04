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

def setupUploadsTable():
    cur.execute("CREATE TABLE IF NOT EXISTS uploads (uploadID int NOT NULL AUTO_INCREMENT PRIMARY KEY, imagepath TEXT NOT NULL, caption TEXT, likes INT NOT NULL DEFAULT 0)")

def resetUploadsTable():
    cur.execute("DROP TABLE users")
    setupUploadsTable()

def uploadImage(imagePath,caption):
    #First Column will be auto-incremented Image ID
    #May need to add column for number of likes
    cur.execute("INSERT INTO uploads (imagepath,caption) VALUES (%s,%s)", (imagePath,caption))
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
    cur.execute("SELECT imagepath,caption FROM uploads WHERE uploadID = (%s)", (uploadID,))
    image = cur.fetchone()
    return image

def getLikesByID(uploadID):
    cur.execute("SELECT likes FROM uploads WHERE uploadID = (%s)", (uploadID,))
    likes = cur.fetchone()
    print(likes[0])
    return int(likes[0])

def getLastIDNum():
    cur.execute("SELECT max(uploadID) FROM uploads")
    id = cur.fetchone()
    return id[0]

def addLike(uploadID):
    currentLikes = getLikesByID(uploadID)
    newLikes = currentLikes + 1
    print(newLikes)
    cur.execute("UPDATE uploads SET likes = (%s) WHERE uploadID = (%s)", (newLikes, uploadID))
    db.commit()

def setupColorMode():
    cur.execute("CREATE TABLE IF NOT EXISTS colormode (email TEXT NOT NULL, mode TEXT NOT NULL)")

def insertDefaultColor(email):
    cur.execute("INSERT INTO colormode(email,mode) VALUES(%s,%s)",(email,"light"))
    db.commit()

def updateColor(email,color):
    email = email.replace("@","%40")
    cur.execute("UPDATE colormode SET mode= (%s) WHERE email=(%s)",(color,email))
    db.commit()

def getColor(email):
    email = email.replace("@","%40")
    cur.execute("SELECT mode FROM colormode WHERE email=(%s)",(email,))
    color = cur.fetchone()
    return color[0]

if __name__ == '__main__':
    # resetTable()
    setupTable()
    #addUser('email@gmail.com', 'password', 'test')
    setupUploadsTable()
    #uploadImage("/imageuploads/image1.jpg","hi")
    #print(getImageByID(1)[0]#[1])
    #getAllImagePaths()
    #print(cur.fetchall())
    #print(getLastIDNum())
    #getLikesByID(1)
    #addLike(1)
    setupColorMode()
    #print(getColor("da@gmail.com"))
    #updateColor("da@gmail.com","dark")
    #cur.execute("SELECT * FROM users")
    #for x in cur.fetchall(): print(x)
    #print(users)

    db.close()
