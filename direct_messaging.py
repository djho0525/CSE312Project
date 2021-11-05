import database as db
import util
import responses as r

def getResponse(sender, receiver):
    receiver = receiver.replace("%40", "@")
    if receiver in r.activeUsers:
        messages = ''
        for message in db.getMessages(sender, receiver):
            messages += "<b>" + message['user'] + "</b>" + message['content'] + '<br/>'
        content = util.readBytes("templates/direct_messaging.html")
        content = content.decode().replace('{{messages}}', messages).replace('{{receiver}}', receiver).encode()
        return r.response200("text/html", len(content), content)
    else:
        return r.response404("User " + receiver + " does not exist or is inactive")

def postResponse(sender, receiver, message):
    receiver = receiver.replace("%40", "@")
    if receiver in r.activeUsers:
        db.addMessage(sender, receiver, message)
        return r.response301("/messages?user=" + receiver)
    else:
        r.response404("User " + receiver + " does not exist or is inactive")
