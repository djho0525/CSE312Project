import mysql.connector as mysql
import os
import util
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
    cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT, name TEXT, token TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS uploads (uploadID int NOT NULL AUTO_INCREMENT PRIMARY KEY, imagepath TEXT NOT NULL, caption TEXT, likes INT NOT NULL DEFAULT 0)")
    cur.execute("CREATE TABLE IF NOT EXISTS colormode (email TEXT NOT NULL, mode TEXT NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS register (email VARCHAR(256) UNIQUE NOT NULL ,name TEXT NOT NULL,token TEXT)")

def dropAllTables():
    cur.execute("DROP TABLE users")
    cur.execute("DROP TABLE uploads")
    cur.execute("DROP TABLE colormode")
    cur.execute("DROP TABLE register")

email_to_users = {}      # {email: User object}
token_to_user = {}      # {token: User object}

def hashPassword(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def addUser(email, password, name, token):
    password = hashPassword(password)
    cur.execute("INSERT INTO users (email, password, name, token) VALUES (%s, %s, %s, %s)", (email, password, name, token))
    db.commit()

def removeUser(email):
    cur.execute("DELETE FROM users WHERE email=%s", (email,))
    db.commit()

def userExists(email):
    cur.execute("SELECT * FROM users WHERE email=%s",(email,))
    row = cur.fetchone()
    return row

def getUser(email):
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    row = cur.fetchone()
    return User(row[0], row[1], row[2], row[3])

def loginUser(email):
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    row = cur.fetchone()
    email_to_users[email] = User(row[0], row[1], row[2], row[3])
    token_to_user[row[3]] = User(row[0], row[1], row[2], row[3])
    # print(users[email].token, token_to_user)

def logoutUser(token):
    if util.computeHash(token).decode() in token_to_user:
        user = token_to_user.pop(util.computeHash(token).decode())
        email_to_users.pop(user.email)
        cur.execute("UPDATE users SET token=%s WHERE token=%s",('',token,))
        db.commit()

def addMessage(sender, receiver, message):
    if receiver not in email_to_users[sender].messages or sender not in email_to_users[receiver].messages:
        email_to_users[sender].messages[receiver], email_to_users[receiver].messages[sender] = [], []
    email_to_users[sender].messages[receiver].append({'user': sender, 'content': message})
    email_to_users[receiver].messages[sender].append({'user': sender, 'content': message})

def getMessages(sender, receiver):
    if sender not in email_to_users[receiver].messages or receiver not in email_to_users[sender].messages:
        email_to_users[receiver].messages[sender], email_to_users[sender].messages[receiver] = [], []
    return email_to_users[receiver].messages[sender]

def addTokenToUser(email,token):
    cur.execute("UPDATE users SET token=%s WHERE email=%s",(token,email,))
    db.commit()

def getUserFromDBByToken(token):
    cur.execute("SELECT * FROM users WHERE token=%s", (util.computeHash(token).decode(),))
    row = cur.fetchone()
    return User(row[0], row[1], row[2], row[3]) if row else None

def getUserByToken(token):
    if util.computeHash(token).decode() in token_to_user:
        return token_to_user[util.computeHash(token).decode()]
    else: return None

def getEmailFromToken(token):
    user = getUserByToken(token)
    return user.email if user else ''

def getNameFromToken(token):
    user = getUserByToken(token)
    return user.name if user else ''

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

def checkToken(token):
    cur.execute("SELECT email,token FROM register")
    data = cur.fetchall()
    print(data)
    for row in data:
        if row[1] != None:
            if bcrypt.checkpw(token.encode("utf-8"),row[1].encode("utf-8")) == True:
                return row[0]
        else:
            return ''
    return ''

if __name__ == '__main__':
    initDB()
    # print(getEmailFromToken("wRJSV3tFylpqgEIKjKZDPuzOi7GdbpeYoTJdA5UwuG4"))
    # dropUserTable()
    # dropAllTables()
    # print(getEmailFromToken("wRJSV3tFylpqgEIKjKZDPuzOi7GdbpeYoTJdA5UwuG4"))
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
