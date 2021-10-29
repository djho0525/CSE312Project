def readBytes(filename):
    with open(filename, "rb") as file: b = file.read()
    file.close()
    return b

def writeBytes(filename, data):
    with open(filename, "wb") as file: file.write(data)
    file.close()

def buffering(server, received_data):
    data = received_data
    while b'\r\n\r\n' not in data:
        data += server.request.recv(1024)
    data = received_data.split(b"\r\n\r\n", 1)
    header, body = data[0].strip().decode(), data[1]
    header = header.split('\r\n')
    content_len = int(header[3].split(' ')[1])        # Content-Length: num
    while content_len-len(body) > 0:
        body += server.request.recv(1024)
    print(header[1:])
    return header[1:], body.strip()

def parsing(data):
    form = dict()
    for f_input in data.split('&'):
        name, value = f_input.split('=')
        form[name] = value
    return form

# Parses HTTP Headers into a Dictionary
def parseHeaders(headers):
    headersDict = {}
    for header in headers:
        keyAndValue = header.split(":")
        key = keyAndValue[0]
        value = keyAndValue[1].strip()
        # Extra check to check for "=" so that each ";" has a "=" to separate the name and value (used to exclude instances where the value may have "; " but isn't for additional options)
        if value.find("; ") != -1 and (value.count("; ") == value.count("=")):
            headersDict[key] = {}
            headersDict[key]["value"] = value[:value.find("; ")].strip()
            if value.count("; ") == 1:
                headersDict[key]["extras"] = {}
                extra = value[value.find("; ")+2:]
                print(extra)
                extraKeyAndValue = extra.split("=")
                extraKey = extraKeyAndValue[0]
                extraValue = extraKeyAndValue[1]
                headersDict[key]["extras"][extraKey] = extraValue
            else:
                extraHeaders = value[value.find("; ")+2:].split("; ")
                print(extraHeaders)
                headersDict[key]["extras"] = {}
                for extra in extraHeaders:
                    extraKeyAndValue = extra.split("=")
                    extraKey = extraKeyAndValue[0]
                    extraValue = extraKeyAndValue[1]
                    headersDict[key]["extras"][extraKey] = extraValue
        else:
            headersDict[key] = value
    #print(headersDict)
    return headersDict



def querying(path):
    if len(path.split('?')) <= 1: return path, {}
    path, queries = path.split("?")
    result = {}
    for x in queries.split('&'):
        key, val = x.split('=')
        result[key] = val
    return path, result
