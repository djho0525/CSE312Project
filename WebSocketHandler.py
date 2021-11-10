import responses as r
import json
import direct_messaging

def webSocketConnection(server):
    # print(r.storedUser + " has connected")
    if r.storedUser not in r.activeUsers:
        r.activeUsers.append(r.storedUser)
    # r.storedUser = ''
    while True:
        recData = server.request.recv(2048)
        if len(recData) > 0:
            frame = webSocketFrameParser(recData)
            if frame["opcode"] == 8:
                r.storedUser = r.serverToUser[server]
                print(r.storedUser + " has disconnected")
                if r.storedUser in r.activeUsers:
                    r.activeUsers.remove(r.storedUser)
                    print("removed " + r.storedUser + " from active users list")

            elif frame["opcode"] == 1:
                content = json.loads(bytes(frame["data"]).decode())

                if content["listener"] == "direct_message":
                    sender, receiver = direct_messaging.newMessage(r.serverToUser[server], content["message"])
                    clients = [r.userToServer[sender], r.userToServer[receiver]]
                    sendFrame = createWebSocketFrame(content["message"])
                    r.userToServer[sender].request.sendall(sendFrame)
                    print("is it stopping here?")


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

