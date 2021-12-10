import database as db
import responses as r
import secrets
import bcrypt
import re

import util


def login(email, password):
    if db.userExists(email):
        user = db.getUser(email)
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            userToken = secrets.token_urlsafe(32)
            userTokenHashed = util.computeHash(userToken)
            db.addTokenToUser(email, userTokenHashed)
            db.loginUser(email)
            r.currentUser.clear()
            r.currentUser.append(email)
            r.activeUsers.append(email)

            return r.response302("/home", "token="+str(userToken)+"; Max-Age=3600; HttpOnly")
        else:
            print('Login failed')
    else:
        print('Email is not registered')
    return r.response302("/")


def signup(name, email, password, confirm_password):
    if db.userExists(email): print('Email was already registered')
    else:
        if password == confirm_password and len(password) >= 8 and re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W).+", password):
            # r.activeUsers[server] = email
            # db.addUserToRegister(email,name)
            userToken = secrets.token_urlsafe(32)
            userTokenHashed = util.computeHash(userToken)
            db.addUser(email, password, name, userTokenHashed)

            db.loginUser(email)
            db.insertDefaultColor(email)
            r.currentUser.clear()
            r.currentUser.append(email)
            print('Created account successfully')
            r.activeUsers.append(email)

            return r.response302("/home", "token="+str(userToken)+"; Max-Age=3600; HttpOnly")
        else: print('Passwords do not match or does not meet all requirements')
    return r. response302("/")

