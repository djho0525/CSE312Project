import database as db
import responses as r

def login(server, email, password):
    email = email.replace("%40", "@")
    if db.userExists(email):
        user = db.getUser(email)
        if user.password == password:
            db.loginUser(email)
            r.currentUser.clear()
            r.currentUser.append(email)

            r.serverToUser[server] = email
            r.userToServer[email] = server
            r.activeUsers.append(email)

            return r.response301("/home", "user=" + email)
        else:
            print('Login failed')
    else:
        print('Email is not registered')
    return r.response301("/")


def signup(server, name, email, password, confirm_password):
    email = email.replace("%40", "@")
    if db.userExists(email): print('Email was already registered')
    else:
        if password == confirm_password:
            # r.activeUsers[server] = email
            db.addUser(email, password, name)
            db.loginUser(email)
            db.insertDefaultColor(email)
            r.currentUser.clear()
            r.currentUser.append(email)
            print('Created account successfully')

            r.serverToUser[server] = email
            r.userToServer[email] = server
            r.activeUsers.append(email)

            return r.response301("/home", "user=" + email)
        else: print('Passwords do not match')
    return r. response301("/")

