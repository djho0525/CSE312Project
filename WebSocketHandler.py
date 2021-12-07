import database
import responses as r
import json
import direct_messaging as DM

#webSocketClients = {}
#webSocketClientsList = []
import util

webSocketClientsDictList = {}

def webSocketConnection(server, token):
    userFromCookie = database.getEmailFromToken(token)
    if userFromCookie == "": return

    print(userFromCookie + " has connected")

    if userFromCookie not in r.activeUsers:
        r.activeUsers.append(userFromCookie)

    while True:
        recData = server.request.recv(2048)
        if len(recData) > 0:
            frame = webSocketFrameParser(recData)
            if frame["opcode"] == 8:
                print(userFromCookie + " has disconnected")
                #webSocketClients.pop(userFromCookie)
                #webSocketClientsList.remove(server)
                webSocketClientsDictList[userFromCookie].remove(server)
                print(webSocketClientsDictList)
                if userFromCookie in r.activeUsers and len(webSocketClientsDictList[userFromCookie]) == 0: # if all of that user's open websocket connections are closed
                    r.activeUsers.remove(userFromCookie)
                    print("removed " + userFromCookie + " from active users list")
                break

            elif frame["opcode"] == 1:
                content = json.loads(bytes(frame["data"]).decode())
                if "imageid" in content.keys():
                    #print(b"TESTING LIVE UPVOTES" + frame["data"])
                    imageid = str(content["imageid"]).replace("image","")
                    print("Image ID to upvote: " + imageid)
                    print("Number of Likes: " + content["likes"])
                    newNumLikes = int(content["likes"]) + 1
                    database.addLikeLive(imageid,newNumLikes)
                    tempUpvoteDict = {"imageid":str(content["imageid"]),"likes":str(newNumLikes)}
                    jsonFormattedNewUpvote = json.dumps(tempUpvoteDict)
                    print(jsonFormattedNewUpvote)
                    frameToSend = createWebSocketFrame(jsonFormattedNewUpvote)
                    #print(frameToSend)
                    for user in webSocketClientsDictList.keys():
                        for client in webSocketClientsDictList[user]:
                            #print("Websocket Client: " + str(client))
                            client.request.sendall(frameToSend)
                    print(webSocketClientsDictList)
                if "listener" in content.keys():
                    if content["listener"] == "direct_message":
                        sender, receiver = DM.newMessage(userFromCookie, content["message"])

                        chatroom_frame = createWebSocketFrame(json.dumps({"listener": "direct_message", "type": "chatroom", "message": util.escapeHTML(content["message"]), "sender": sender}))
                        notif_frame = createWebSocketFrame(json.dumps({"listener": "direct_message", "type": "notif", "message": util.escapeHTML(content["message"]), "sender": sender}))
                        # webSocketClients[sender].request.sendall(chatroom_frame)
                        for client in webSocketClientsDictList[sender]:
                            client.request.sendall(chatroom_frame)

                        if receiver in DM.active_chatrooms and DM.active_chatrooms[receiver] == sender:
                            for client in webSocketClientsDictList[receiver]:
                                client.request.sendall(chatroom_frame)
                        else:
                            for client in webSocketClientsDictList[receiver]:
                                client.request.sendall(notif_frame)



def webSocketFrameParser(frame):
    retVal = {}
    retVal["opcode"] = frame[0] & 15
    retVal["fin"] = (frame[0] & 128) >> 7
    maskBit = (frame[1] & 128) >> 7

    payloadLen = int.from_bytes(frame[1:2], 'big') & 127
    currentByte = 2
    if payloadLen == 126:
        payloadLen = int.from_bytes(frame[2:3] + frame[3:4], 'big')
        currentByte = 4
    elif payloadLen == 127:
        payloadLen = b''
        for x in range(2, 10):
            payloadLen += frame[x:x+1]
        payloadLen = int.from_bytes(payloadLen, 'big')
        currentByte = 11

    if maskBit == 1:
        mask = [frame[currentByte:currentByte+1], frame[currentByte+1:currentByte+2], frame[currentByte+2:currentByte+3], frame[currentByte+3:currentByte+4]]
        currentByte += 4

        byteNum = 1
        payload = b''
        for x in range(currentByte, currentByte + payloadLen):
            maskPiece = (byteNum % 4) - 1
            if maskPiece == -1: maskPiece = 3

            payload += (int.from_bytes(frame[x:x+1], 'big') ^ int.from_bytes(mask[maskPiece], 'big')).to_bytes(1, 'big')
            byteNum += 1
        retVal["data"] = payload
        return retVal

def createWebSocketFrame(content):
    payload = bytes(content.encode())
    frame, index, payload_len = [], 0, len(payload)         # index = 0
    frame.append(binToDec('1000 0001'))                     # index = 1

    if payload_len >= 65536:
        frame.append(127)                                   # index = 2
        pay_len_bin = decToBin(payload_len)
        for i in range(0, 64, 8): frame.append(binToDec(pay_len_bin[i:i+8]))            # index = 9
    elif payload_len >= 126:
        frame.append(126)                                   # index = 2
        pay_len_bin = decToBin(payload_len)
        for i in range(0, 16, 8): frame.append(binToDec(pay_len_bin[i:i+8]))            # index = 3
    else: frame.append(payload_len)                             # index = 2

    for i in payload: frame.append(i)
    return bytearray(frame)

def decToBin(decimal):
    binary, x = '', 8
    while pow(2, x) <= decimal: x += 8
    for i in range(x-1, -1, -1):
        binary += str(decimal//pow(2, i))
        decimal = decimal % pow(2, i)
    return binary

def binToDec(binary):
    binary = binary.replace(' ', '')
    decimal = 0
    for i in range(len(binary)):
        if binary[len(binary)-1-i] == '1': decimal += pow(2, i)
    return decimal

