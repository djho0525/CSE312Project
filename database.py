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
cur.execute("CREATE TABLE IF NOT EXISTS uploads (uploadID int NOT NULL AUTO_INCREMENT PRIMARY KEY, imagepath TEXT NOT NULL, caption TEXT, likes INT NOT NULL DEFAULT 0)")
cur.execute("CREATE TABLE IF NOT EXISTS colormode (email TEXT NOT NULL, mode TEXT NOT NULL)")

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

def addMessage(sender, receiver, message):
    if receiver not in users[sender].messages or sender not in users[receiver].messages:
        users[sender].messages[receiver], users[receiver].messages[sender] = [], []
    users[sender].messages[receiver].append({'user': sender, 'content': message})
    users[receiver].messages[sender].append({'user': sender, 'content': message})

def getMessages(sender, receiver):
    if sender not in users[receiver].messages or receiver not in users[sender].messages:
        users[receiver].messages[sender], users[sender].messages[receiver] = [], []
    return users[receiver].messages[sender]

def setupUploadsTable():
    cur.execute("CREATE TABLE IF NOT EXISTS uploads (uploadID int NOT NULL AUTO_INCREMENT PRIMARY KEY, imagepath TEXT NOT NULL, caption TEXT, likes INT NOT NULL DEFAULT 0)")

def resetUploadsTable():
    cur.execute("DROP TABLE uploads")
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
    if id[0] is not None:
        return id[0]
    else:
        return 0

def getLatest10Uploads():
    cur.execute("SELECT * FROM cse312_project.uploads ORDER BY uploadID desc LIMIT 10")
    latestUploads = cur.fetchall()
    return latestUploads

def addLike(uploadID):
    currentLikes = getLikesByID(uploadID)
    newLikes = currentLikes + 1
    print(newLikes)
    cur.execute("UPDATE uploads SET likes = (%s) WHERE uploadID = (%s)", (newLikes, uploadID))
    db.commit()

def addLikeLive(uploadID, newNumLikes):
    print(newNumLikes)
    cur.execute("UPDATE uploads SET likes = (%s) WHERE uploadID = (%s)", (newNumLikes, uploadID))
    db.commit()

def setupColorMode():
    cur.execute("CREATE TABLE IF NOT EXISTS colormode (email TEXT NOT NULL, mode TEXT NOT NULL)")

def resetColorModeTable():
    cur.execute("DROP TABLE colormode")
    setupColorMode()

def insertDefaultColor(email):
    cur.execute("INSERT INTO colormode(email,mode) VALUES(%s,%s)",(email,"light"))
    db.commit()

def updateColor(email,color):
    # email = email.replace("@","%40")
    cur.execute("UPDATE colormode SET mode= (%s) WHERE email=(%s)",(color,email))
    db.commit()

def getColor(email):
    # email = email.replace("@","%40")
    cur.execute("SELECT mode FROM colormode WHERE email=(%s)",(email,))
    color = cur.fetchone()
    if color is not None:
        return color[0]
    else:
        return 0

if __name__ == '__main__':
    # dropUserTable()
    # addUser('email@gmail.com', 'password', 'test')
    # removeUser('email@gmail.com')
    setupUploadsTable()
    #uploadImage("/imageuploads/image1.jpg","hi")
    #print(getImageByID(1)[0]#[1])
    #getAllImagePaths()
    #print(cur.fetchall())
    #print(getLastIDNum())
    #getLikesByID(1)
    #addLike(1)
    #resetColorModeTable()
    setupColorMode()
    #print(getColor("da@gmail.com"))
    #updateColor("da@gmail.com","dark")
    #cur.execute("SELECT * FROM users")
    #for x in cur.fetchall(): print(x)
    #print(users)
    # print(getLatest10Uploads())
    db.close()
