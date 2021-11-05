import login_signup
import util
import database as db

activeUsers = []

def response200(con_type, length, content):  # input content has to be encoded
    return b"HTTP/1.1 200 OK\r\nContent-Type:" + con_type.encode() + b"\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(length).encode() + b"\r\n\r\n" + content + b"\r\n"

def response404():
    return b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: " + str(len("The requested content does not exist")).encode() + b"\r\n\r\nThe requested content does not exist\r\n"

def response301(location):
    return b"HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0\r\nLocation: " + location + b"\r\n"



def getResponse(path):
    print("GET" + path)
    path, queries = util.querying(path)

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
    elif path == "/messages":
        receiver, sender = queries['receiver'], queries['sender']
        content = util.readBytes("templates/messages.html")
        content = content.decode().replace('{{message}}', '').replace('{{receiver}}', receiver).replace("{{sender}}", sender).encode()
        return response200("text/html", len(content), content)
    elif path == "/home":
        content = ""
        idxFile = open('templates/index.html', 'rt').readlines()
        for line in idxFile:
            if line.find("<!--ActiveUsers-->") != -1:
                for x in activeUsers:
                    line = line + x
            content = content + line
        return response200("text/html",len(content),content.encode())
    elif path == "/home.css":
        content = util.readBytes("static/home.css")
        return response200("text/css", len(content), content)
    else:
        return response404()






def postResponse(server, path, received_data):
    print("POST" + path)
    header, data = util.buffering(server, received_data)
    print(data)
    form = util.parsing(data.decode())
    print(form)
    path, queries = util.querying(path)

    if path == "/login":
        return login_signup.login(email=form['email'], password=form['password'])
    elif path == '/signUp':
        return login_signup.signup(name=form['name'], email=form['email'], password=form['password'], confirm_password=form['confirm_password'])
    elif path == "/image-upload":
        return response301("/")
    elif path == '/messages':
        receiver, sender, message = queries['receiver'], queries['sender'], form['message']
        db.addMessage(receiver, sender, message)
        messages = ''
        for i in db.users[receiver].messages[sender]: messages += i + '<br/>'
        content = util.readBytes("templates/messages.html")
        content = content.decode().replace('{{message}}', messages).replace('{{receiver}}', receiver).replace("{{sender}}", sender).encode()
        return response200("text/html", len(content), content)
    else:
        return response404()
