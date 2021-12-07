import database as db
import responses as r
import secrets
import bcrypt

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

            return r.response301("/home", "token="+str(userToken)+"; Max-Age=3600; HttpOnly")
        else:
            print('Login failed')
    else:
        print('Email is not registered')
    return r.response301("/")


def signup(name, email, password, confirm_password):
    if db.userExists(email): print('Email was already registered')
    else:
        if password == confirm_password:
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

            return r.response301("/home", "token="+str(userToken)+"; Max-Age=3600; HttpOnly")
        else: print('Passwords do not match')
    return r. response301("/")

