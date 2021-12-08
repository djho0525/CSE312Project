import base64
import hashlib

import login_signup
import direct_messaging as DM
import util
import database as db
import WebSocketHandler

activeUsers = []
currentUser = []

def response200(con_type, length, content):  # input content has to be encoded
    return b"HTTP/1.1 200 OK\r\nContent-Type:" + con_type.encode() + b"\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(length).encode() + b"\r\n\r\n" + content + b"\r\n"

def response404(content='The requested content does not exist'):
    return b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(content)).encode() + b"\r\n\r\n" + content.encode()

def response302(location, cookie=''):
    return b"HTTP/1.1 302 Moved Temporarily\r\nContent-Length: 0\r\nLocation: " + location.encode() + b"\r\nSet-cookie: " + cookie.encode() + b"\r\n\r\n"


def getResponse(server, path, received_data):
    print("GET " + path)
    path, queries = util.querying(path)
    header, form = util.buffering(server, received_data)
    print(form)
    if "token" in util.parseCookies(header).keys():
        token = util.parseCookies(header)["token"]
        userFromCookie = db.getEmailFromToken(token)
        if userFromCookie != "":
            print(userFromCookie + " requested the data above")
    else: token, userFromCookie = "", ""


    if path == "/":
        user = db.getUserFromDBByToken(token)
        stored_token = user.token if user else ''
        if user and stored_token != '': return response302("/home")

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
    elif path == "/messages" and "user" in queries:
        user = db.getUserFromDBByToken(token)
        stored_token = user.token if user else ''
        if not user or stored_token == '': return response302("/")

        if userFromCookie not in activeUsers: activeUsers.append(userFromCookie)
        return DM.getResponse(userFromCookie, queries['user'])
    elif path == "/direct_messaging.js":
        content = util.readBytes("static/direct_messaging.js")
        return response200("text/javascript", len(content), content)
    elif path == "/home":
        user = db.getUserFromDBByToken(token)
        stored_token = user.token if user else ''
        if not user or stored_token == '': return response302("/")

        content = ""
        idxFile = open('templates/index.html', 'rt').readlines()
        if userFromCookie not in activeUsers: activeUsers.append(userFromCookie)
        for line in idxFile:
            if line.find("<!--ActiveUsers-->") != -1:
                for x in activeUsers:
                    if x != userFromCookie:
                        line = line + '<a class ="dropdown-item" href="/messages?user=' + util.escapeHTML(x) + '">' + util.escapeHTML(x) + '</a>'
            content = content + line
        content = content.replace("{{user}}", util.escapeHTML(db.getNameFromToken(token)))
        if db.getColor(userFromCookie) == "light":
            content = content.replace("{{colorMode}}",'lightMode.css')
            content = util.renderImages(content)
            return response200("text/html", len(content), content.encode())
        else:
            content = content.replace("{{colorMode}}",'darkMode.css')
            content = util.renderImages(content)
            return response200("text/html", len(content), content.encode())
    elif path == "/lightMode.css":
        content = util.readBytes("static/lightMode.css")
        return response200("text/css", len(content), content)
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
    elif path == "/websocket":
        socketKey = header["Sec-WebSocket-Key"] + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        base64_string = base64.b64encode(hashlib.sha1(socketKey.encode()).digest()).decode()
        response = "HTTP/1.1 101 Switching Protocols\r\nConnection:Upgrade\r\nUpgrade:websocket\r\nSec-WebSocket-Accept:" + base64_string + "\r\n\r\n"
        #WebSocketHandler.webSocketClients[userFromCookie] = server
        #WebSocketHandler.webSocketClientsList.append(server)
        if userFromCookie not in WebSocketHandler.webSocketClientsDictList.keys():
            WebSocketHandler.webSocketClientsDictList[userFromCookie] = []
            WebSocketHandler.webSocketClientsDictList[userFromCookie].append(server)
        else:
            WebSocketHandler.webSocketClientsDictList[userFromCookie].append(server)
        #print(WebSocketHandler.webSocketClients)
        print(WebSocketHandler.webSocketClientsDictList)
        return response.encode()
    else:
        return response404()


def postResponse(server, path, received_data):
    # Body of image must not be decoded, data is decoded below
    if path == "/image-upload":
        util.imageUpload(server, received_data)
        return response302("/home")

    print("POST " + path)
    path, queries = util.querying(path)
    header, form = util.buffering(server, received_data)
    print(form)
    if "token" in util.parseCookies(header).keys():
        token = util.parseCookies(header)["token"]
        userFromCookie = db.getEmailFromToken(token)
        if userFromCookie != False:
            print(userFromCookie + " requested the data above")
    else: token, userFromCookie = "", ""

    if path == "/login":
        return login_signup.login(email=form['email'], password=form['password'])
    elif path == '/signUp':
        return login_signup.signup(name=form['name'], email=form['email'], password=form['password'], confirm_password=form['confirm_password'])
    elif path == "/image-upload":
        return response302("/")
    elif path == "/mode":
        # print(userFromCookie + " has made a request for ")
        db.updateColor(userFromCookie, form["Mode"])
        return response302("/home")
    #elif path == "/upvote":
        #imageID = int(str(form["uploadID"]).strip("image"))
        #db.addLike(imageID)
        #return response302("/home")
    #elif path == "/logout":
        #activeUsers.pop(server)
        #return response302("/")
    elif path == "/logout":
        activeUsers.pop(server) if server in activeUsers else True
        db.logoutUser(token)
        userFromCookie = db.getEmailFromToken(token)
        #Ensures that logged out user is removed from websocketclients
        if WebSocketHandler.webSocketClientsDictList.get(userFromCookie) is not None:
            if server in WebSocketHandler.webSocketClientsDictList.get(userFromCookie):
                WebSocketHandler.webSocketClientsDictList.get(userFromCookie).remove(server)
                print(WebSocketHandler.webSocketClientsDictList)
        return response302('/', "token=; Max-Age=0; HttpOnly")
    else:
        return response404()
