import responses
import util
import database as db

activeUsers = []

def response200(con_type, length, content):  # input content has to be encoded
    return b"HTTP/1.1 200 OK\r\nContent-Type:" + con_type.encode() + b"\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(length).encode() + b"\r\n\r\n" + content + b"\r\n"

def response404():
    return b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: " + str(len("The requested content does not exist")).encode() + b"\r\n\r\nThe requested content does not exist\r\n"

def response301(location):
    return b"HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0\r\nLocation: " + location.encode() + b"\r\n"



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
        if db.getColor("da@gmail.com")=="light":
            content = content.replace("{{colorMode}}",'lightMode.css')
        else:
            content = content.replace("{{colorMode}}",'darkMode.css')
        return response200("text/html",len(content),content.encode())
    elif path == "/lightMode.css":
        content = util.readBytes("static/lightMode.css")
        return response200("text/css", len(content), content)
    # IMAGE UPLOADS CURRENTLY ONLY ASSUME .JPG FILES WILL BE UPLOADED
    elif path == "/posts":
        content = util.renderImages()
        return response200("text/html", len(content), content.encode())
    elif path.find("/uploadedimage/") != -1:
        content = util.hostImage(path)
        if content is None:
            return response404()
        else:
            return response200("image/jpeg", len(content),content)
    elif path == "/darkMode.css":
        content = util.readBytes("static/darkMode.css")
        return response200("text/css", len(content), content)
    elif path == "/home.js":
        content = util.readBytes("static/home.js")
        return response200("text/javascript", len(content), content)
    else:
        return response404()






def postResponse(server, path, received_data):
    # Body of image must not be decoded, data is decoded below
    if path == "/image-upload":
        util.imageUpload(server, received_data)
        return response301("/posts")

    print("POST" + path)
    header, data = util.buffering(server, received_data)
    print(data)
    form = util.parsing(data.decode())
    print(form)
    path, queries = util.querying(path)
    email = ""

    if path == "/login":
        email, password = form['email'], form['password']
        if db.userExists(email):
            user = db.getUser(email)
            if user.password == password:
                email = email.replace("%40", "@")
                activeUsers.append('<a class ="dropdown-item" href="#" >' + email + '</a>')
                return response301("/home")
            else:
                content = 'Login failed'
        else:
            content = 'Email is not registered'
        content = content.encode()
        return response200("text/plain", len(content), content)
    elif path == '/signUp':
        name, email, password, confirm_password = form['name'], form['email'], form['password'], form['confirm_password']
        if db.userExists(email): content = 'Email was already registered'
        else:
            if password == confirm_password:
                db.addUser(email, password, name)
                db.insertDefaultColor(email)
                content = 'Created account successfully'
            else: content = 'Passwords do not match'
        content = content.encode()
        return response200("text/plain", len(content), content)
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
    elif path == "/mode":
        db.updateColor("da@gmail.com",form["Mode"])
        return response301("/home")
    else:
        return response404()
