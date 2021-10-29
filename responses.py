import util
import database as db

def response200(con_type, length, content):  # input content has to be encoded
    return b"HTTP/1.1 200 OK\r\nContent-Type:" + con_type.encode() + b"\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(length).encode() + b"\r\n\r\n" + content + b"\r\n"

def response404():
    return b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: " + str(len("The requested content does not exist")).encode() + b"\r\n\r\nThe requested content does not exist\r\n"

def response301(location):
    return b"HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0\r\nLocation: " + location + b"\r\n"



def getResponse(path):
    print("GET" + path)

    if path == "/":
        content = util.readBytes("templates/login.html")
        return response200("text/html", len(content), content)
    elif path == "/login.css":
        content = util.readBytes("static/login.css")
        return response200("text/css", len(content), content)
    elif path == "/login.js":
        content = util.readBytes("static/login.js")
        return response200("text/javascript", len(content), content)
    elif path == "/jessehartloff.jpeg":
        content = util.readBytes("static/jessehartloff.jpeg")
        return response200("image/jpeg", len(content), content)
    else:
        return response404()






def postResponse(server, path, received_data):
    print("POST" + path)
    header, data = util.buffering(server, received_data)
    print(data)
    form = util.parsing(data.decode())
    print(form)

    if path == "/login":
        email, password = form['email'], form['password']
        if db.userExists(email):
            user = db.getUser(email)
            if user.password == password: content = 'Logged in successfully'
            else: content = 'Login failed'
        else: content = 'Email is not registered'
        content = content.encode()
        return response200("text/plain", len(content), content)
    elif path == '/signUp':
        name, email, password, confirm_password = form['name'], form['email'], form['password'], form['confirm_password']
        if db.userExists(email): content = 'Email was already registered'
        else:
            if password == confirm_password:
                db.addUser(email, password, name)
                content = 'Created account successfully'
            else: content = 'Passwords do not match'
        content = content.encode()
        return response200("text/plain", len(content), content)
    elif path == "/image-upload":
        return response301("/")
    else:
        return response404()
