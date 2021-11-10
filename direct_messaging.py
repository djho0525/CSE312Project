import database as db
import util
import responses as r

active_chatrooms = {}           # only sender to receiver

def getResponse(sender, receiver):
    receiver = receiver.replace("%40", "@")
    if receiver in r.activeUsers:
        messages = ''
        for message in db.getMessages(sender, receiver):
            messages += "<b>" + message['user'] + "</b>" + message['content'] + '<br/>'
        content = util.readBytes("templates/direct_messaging.html")
        content = content.decode().replace('{{messages}}', messages).replace('{{receiver}}', receiver).encode()
        active_chatrooms[sender] = receiver
        return r.response200("text/html", len(content), content)
    else:
        return r.response404("User " + receiver + " does not exist or is inactive")

def newMessage(sender, message):
    receiver = active_chatrooms[sender]
    db.addMessage(sender, receiver, message)
    return sender, receiver
