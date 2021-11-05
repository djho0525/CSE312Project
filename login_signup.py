import database as db
import responses as r

def login(email, password):
    email = email.replace("%40", "@")
    if db.userExists(email):
        user = db.getUser(email)
        if user.password == password:
            r.activeUsers.append('<a class ="dropdown-item" href="#" data-toggle="modal" data-target="#modalDM">' + email + '</a>')
            db.loginUser(email)
            r.currentUser.clear()
            r.currentUser.append(email)
            return r.response301("/home")
        else:
            print('Login failed')
    else:
        print('Email is not registered')
    return r.response301("/")


def signup(name, email, password, confirm_password):
    email = email.replace("%40", "@")
    if db.userExists(email): print('Email was already registered')
    else:
        if password == confirm_password:
            r.activeUsers.append('<a class ="dropdown-item" href="#" data-toggle="modal" data-target="#modalDM">' + email + '</a>')
            db.addUser(email, password, name)
            db.loginUser(email)
            db.insertDefaultColor(email)
            print('Created account successfully')
            return r.response301("/home")
        else: print('Passwords do not match')
    return r. response301("/")

