import mysql.connector as mysql
import os
from User import User
import bcrypt

#host = 'localhost' #Change host to "localhost" for local testing, "mysql" for docker
host = 'localhost'
u = 'sqluser'   # os.environ['DB_USERNAME']
p = 'sqluserpassword'   # os.environ['DB_PASSWORD']
database = 'cse312_project'

db = mysql.connect(host=host, user=u, password=p, database=database)
cur = db.cursor(prepared=True)

def initDB():
    # INITIALIZE DATABASE AND TABLES
    cur.execute("CREATE DATABASE IF NOT EXISTS " + database)
    db.database = database
    cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS uploads (uploadID int NOT NULL AUTO_INCREMENT PRIMARY KEY, imagepath TEXT NOT NULL, caption TEXT, likes INT NOT NULL DEFAULT 0)")
    cur.execute("CREATE TABLE IF NOT EXISTS colormode (email TEXT NOT NULL, mode TEXT NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS register(email VARCHAR(256) UNIQUE NOT NULL ,name TEXT NOT NULL,token TEXT)")

users = {}      # {email: User object}

def hashPassword(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def dropUserTable():
    cur.execute("DROP TABLE users")

def addUser(email, password, name):
    password = hashPassword(password)
    cur.execute("INSERT INTO users (email, password, name) VALUES (%s, %s, %s)", (email, password, name))
    db.commit()

def removeUser(email):
    cur.execute("DELETE FROM users WHERE email=%s", (email,))
    db.commit()

def userExists(email):
    cur.execute("SELECT * FROM users WHERE email=%s",(email,))
    row = cur.fetchone()
    if row is not None:
        return True
    else:
        return False

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

def getLastIDNum():
    cur.execute("SELECT max(uploadID) FROM uploads")
    id = cur.fetchone()
    if id[0] is not None:
        return id[0]
    else:
        return False

def getLatest10Uploads():
    cur.execute("SELECT * FROM uploads ORDER BY uploadID desc LIMIT 10")
    latestUploads = cur.fetchall()
    return latestUploads

def addLike(uploadID):
    currentLikes = getLikesByID(uploadID)
    newLikes = currentLikes + 1
    #print(newLikes)
    cur.execute("UPDATE uploads SET likes = (%s) WHERE uploadID = (%s)", (newLikes, uploadID))
    db.commit()

def addLikeLive(uploadID, newNumLikes):
    #print(newNumLikes)
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
        print("getting color for: "+email)
        return color[0]
    else:
        return 0

def addUserToRegister(email,name):
    cur.execute("INSERT INTO register(email,name) VALUES(%s,%s)",(email,name,))
    db.commit()

def addTokenToUser(email,token):
    cur.execute("UPDATE register SET token=%s WHERE email=%s",(token,email,))
    db.commit()

def getNameFromToken(token):
    cur.execute("SELECT name,token FROM register")
    data = cur.fetchall()
    for row in data:
        if row[1] != None:
            if bcrypt.checkpw(token.encode("utf-8"),row[1].encode("utf-8")) == True:
                return row[0]
        else:
            return False

def checkToken(token):
    cur.execute("SELECT email,token FROM register")
    data = cur.fetchall()
    print(data)
    for row in data:
        if row[1] != None:
            if bcrypt.checkpw(token.encode("utf-8"),row[1].encode("utf-8")) == True:
                return row[0]
        else:
            return False
    return False

if __name__ == '__main__':
    initDB()

    # dropUserTable()
    # addUser('email@gmail.com', 'password', 'test')
    # removeUser('email@gmail.com')
    #setupUploadsTable()
    #uploadImage("/imageuploads/image1.jpg","hi")
    #print(getImageByID(1)[0]#[1])
    #getAllImagePaths()
    #print(cur.fetchall())
    #print(getLastIDNum())
    #getLikesByID(1)
    #addLike(1)
    #resetColorModeTable()
    #setupColorMode()
    #print(getColor("da@gmail.com"))
    #updateColor("da@gmail.com","dark")
    #cur.execute("SELECT * FROM users")
    #for x in cur.fetchall(): print(x)
    #print(users)
    # print(getLatest10Uploads())
    #db.close()
