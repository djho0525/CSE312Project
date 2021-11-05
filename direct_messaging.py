import database as db
import util
import responses as r

def postResponse(receiver, sender, message):
    db.addMessage(receiver, sender, message)
    messages = ''
    for i in db.users[receiver].messages[sender]: messages += i + '<br/>'
    content = util.readBytes("templates/messages.html")
    content = content.decode().replace('{{message}}', messages).replace('{{receiver}}', receiver).replace("{{sender}}", sender).encode()
    return r.response200("text/html", len(content), content)

