import database as db
import responses as r

def login(email, password):
    if db.userExists(email):
        user = db.getUser(email)
        if user.password == password:
            email = email.replace("%40", "@")
            r.activeUsers.append('<a class ="dropdown-item" href="#" >' + email + '</a>')
            db.loginUser(email)
            r.currentUser.clear()
            r.currentUser.append(email)
            return r.response301("/home".encode())
        else:
            content = 'Login failed'
    else:
        content = 'Email is not registered'
    content = content.encode()
    return r.response200("text/plain", len(content), content)


def signup(name, email, password, confirm_password):
    if db.userExists(email): content = 'Email was already registered'
    else:
        if password == confirm_password:
            db.addUser(email, password, name)
            db.loginUser(email)
            db.insertDefaultColor(email)
            content = 'Created account successfully'
        else: content = 'Passwords do not match'
    content = content.encode()
    return r. response200("text/plain", len(content), content)

