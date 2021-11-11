import database as db
import util
import responses as r

active_chatrooms = {}           # only sender to receiver

def getResponse(sender, receiver):
    receiver = receiver.replace("%40", "@")
    if receiver in r.activeUsers:
        messages = ''
        for message in db.getMessages(sender, receiver):
            messages += "<b>" + message['user'] + ": </b>" + message['content'] + "<br/>"

        users_dropdown = ''
        for user in r.activeUsers:
            users_dropdown += '<a class ="dropdown-item" href="/messages?user=' + user + '">' + user + '</a>'

        content = util.readBytes("templates/direct_messaging.html")
        content = content.decode().replace('{{messages}}', messages).replace('{{receiver}}', receiver).replace("<!--ActiveUsers-->", users_dropdown)

        content = content.replace("{{user}}", sender)
        if db.getColor(sender) == "light": content = content.replace("{{colorMode}}",'lightMode.css')
        else: content = content.replace("{{colorMode}}",'darkMode.css')

        content = content.encode()
        return r.response200("text/html", len(content), content)
    else:
        return r.response404("User " + receiver + " does not exist or is inactive")

def newMessage(sender, message):
    receiver = active_chatrooms[sender]
    db.addMessage(sender, receiver, message)
    return sender, receiver
