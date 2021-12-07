import database as db

def readBytes(filename):
    with open(filename, "rb") as file: b = file.read()
    file.close()
    return b

def writeBytes(filename, data):
    with open(filename, "wb") as file: file.write(data)
    file.close()

def parsingToDict(con_array, split_char):
    result = {}
    for x in con_array:
        if split_char in x:
            key, val = x.split(split_char, 1)
            result[key] = val
        else: return con_array
    return result

def buffering(server, received_data):
    while b'\r\n\r\n' not in received_data:
        received_data += server.request.recv(1024)
    data = received_data.split(b"\r\n\r\n", 1)
    header, body = data[0].strip().decode().split('\r\n'), data[1]

    content_len = int(header["Content-Length"]) if "Content-Length" in header else 0
    content_type = header["Content-Type"] if "Content-Type" in header else ''
    while content_len-len(body) > 0:
        body += server.request.recv(1024)
    body = parseBody(body, content_type)
    return header[1:], body

# def parsing(data):
#     form = dict()
#     for f_input in data.split('&'):
#         name, value = f_input.split('=')
#         form[name] = value
#     return form

# Parses HTTP Headers into a Dictionary
def parseHeaders(headers):
    headersDict = {}
    for header in headers:
        keyAndValue = header.split(":")
        key = keyAndValue[0]
        value = keyAndValue[1].strip()
        #print("KEY: " + key + " VALUE: " + value)
        # Extra check to check for "=" so that each ";" has a "=" to separate the name and value (used to exclude instances where the value may have "; " but isn't for additional options)
        if value.find("; ") != -1 and (value.count("; ") == value.count("=")):
            headersDict[key] = {}
            headersDict[key]["value"] = value[:value.find("; ")].strip()
            if value.count("; ") == 1:
                headersDict[key]["extras"] = {}
                extra = value[value.find("; ")+2:]
                # print(extra)
                extraKeyAndValue = extra.split("=")
                extraKey = extraKeyAndValue[0]
                extraValue = extraKeyAndValue[1]
                headersDict[key]["extras"][extraKey] = extraValue
            else:
                extraHeaders = value[value.find("; ")+2:].split("; ")
                # print(extraHeaders)
                headersDict[key]["extras"] = {}
                for extra in extraHeaders:
                    extraKeyAndValue = extra.split("=")
                    extraKey = extraKeyAndValue[0]
                    extraValue = extraKeyAndValue[1]
                    headersDict[key]["extras"][extraKey] = extraValue
        else:
            headersDict[key] = value
    # print(headersDict)
    return headersDict

def parseBody(body, content_type):
    content = {}
    print(body)
    if body == b'': return {}
    if 'multipart/form-data' in content_type:
        boundary = ('--' + content_type.split("; ")[1].split("=")[1]).encode()
        body_list = list(filter(lambda x: x != b'\r\n' and x != b'' and x != b'--', body.strip().split(boundary)))
        for y in body_list:
            header, body = y.strip().split(b"\r\n\r\n", 1)
            header = header.decode().replace("\r\n", "; ").replace(": ", "=")
            temp = parsingToDict(header.split('; '), '=')
            name = temp.pop('name')[1:-1]            # remove quotations "" around name value
            content[name] = body
            for key, val in temp.items(): content[key] = val
    else: content = parsingToDict(body.decode().split('&'), '=')
    return content

imageUploads = []
validFiles = []

def imageUpload(server, receive):
    imageNameCount = db.getLastIDNum()
    newLineAfterHeadersInBytes = receive.find("\r\n\r\n".encode())
    # print(newLineAfterHeadersInBytes)
    requestInBytes = receive[0:newLineAfterHeadersInBytes]
    # print(str(requestInBytes))
    endOfHeaders = receive.find("\r\n\r\n".encode())
    endOfRequestLineInBytes = requestInBytes.find("\r\n".encode())
    headersInBytes = requestInBytes[endOfRequestLineInBytes + 2:endOfHeaders]
    decodedHeaders = headersInBytes.decode("utf-8")
    # print("DECODED HEADERS: " + decodedHeaders)
    splitDecodedHeaders = filter(None, decodedHeaders.split("\r\n"))  # split makes each line of header a element in an array and remove empty elements from ending \r\n
    decodedRequestHeaders = parseHeaders(splitDecodedHeaders)
    print(decodedRequestHeaders)

    encodedBoundary = decodedRequestHeaders.get("Content-Type").get("extras").get("boundary").encode()
    fullEncodedBoundary = b"--" + encodedBoundary
    print(fullEncodedBoundary)

    contentLength = int(decodedRequestHeaders.get("Content-Length"))
    startOfBody = endOfHeaders + 4
    body = receive[startOfBody:startOfBody + contentLength]  # +4 to get through all \r\n\r\n
    # print(body.encode())  # prints the body in bytes
    # print("Content Length: " + str(contentLength) + " Body Length: " + str(len(body)))
    bytesRead = b""
    bytesRead += body
    # print("BYTES READ: " + bytesRead)

    while len(bytesRead) != contentLength:
        receive = server.request.recv(1024)
        # print(receive)
        bytesRead += receive
        # print("Bytes Read: " + str(len(bytesRead)) + "Content Length: " + str(contentLength))
        # print(bytesRead)
    # print(bytesRead)

    # bytesRead STORES THE FULL BODY READ IN BYTES

    print("Bytes Read: " + str(len(bytesRead)) + "Content Length: " + str(contentLength))

    contentParts = list(filter(None, bytesRead.split(fullEncodedBoundary)))  # Removes empty elements
    contentParts = contentParts[:len(contentParts) - 1]  # Removes -- from last boundary
    # print(contentParts)
    currentUploaderComment = ""
    fileExtension = ".jpg"
    for part in contentParts:
        headersandbodyOfPart = part.split("\r\n\r\n".encode())
        decodedUnsplittedHeadersOfPart = headersandbodyOfPart[0].strip().decode("utf-8")
        decodedHeadersOfPart = filter(None, decodedUnsplittedHeadersOfPart.split("\r\n"))
        bodyOfPart = headersandbodyOfPart[1].strip()
        decodedHeadersDictOfPart = parseHeaders(decodedHeadersOfPart)
        # print(bodyOfPart)
        print(decodedHeadersDictOfPart)
        #if decodedHeadersDictOfPart.get("Content-Disposition").get("extras").get("name").strip('"') == "xsrf_token":
        #    if bodyOfPart.decode() not in tokenList:  # have to decode the body of xsrf_token since the token is a string
        #        print("INVALID TOKEN: " + bodyOfPart.decode())
        #        response = buildHTTPForbiddenResponse()
        #        self.request.sendall(response.encode("utf-8"))
        #        return
        if decodedHeadersDictOfPart.get("Content-Type") is None:
            if decodedHeadersDictOfPart.get("Content-Disposition").get("extras").get("name").strip('"') == "caption":
                print("CAPTION DETECTED")
                currentUploaderComment += bodyOfPart.decode("utf-8")
                print(currentUploaderComment)
        elif decodedHeadersDictOfPart.get("Content-Type") is not None and decodedHeadersDictOfPart.get("Content-Type").find("text/") == -1:
            if decodedHeadersDictOfPart.get("Content-Disposition").get("extras").get("filename") is not None:
                print("CHECKING IMAGE FILE TYPE THRU FILENAME")
                filename = decodedHeadersDictOfPart.get("Content-Disposition").get("extras").get("filename").strip('"')
                fileExtension = filename[len(filename)-len(".___"):]
                print("FILE EXTENSION: " + fileExtension)
            if decodedHeadersDictOfPart.get("Content-Disposition").get("extras").get("name").strip('"') == "upload":
                print("IMAGEUPLOAD PART")
                print(currentUploaderComment)
                imageNameCount += 1
                f = open("imageUploads/" + "image" + str(imageNameCount) + fileExtension, "wb")
                f.write(bodyOfPart)
                f.close()
                currentUploaderComment = ""
    #currentUploaderComment = cleanMessage(currentUploaderComment)
    imageUploads.append(currentUploaderComment + ":" + "image" + str(imageNameCount) + fileExtension)
    validFiles.append("image" + str(imageNameCount) + fileExtension)
    db.uploadImage("imageUploads/" + "image" + str(imageNameCount) + fileExtension, currentUploaderComment)
    print("VALID FILES")
    print(validFiles)
    print(imageUploads)

def renderImages(html):
    imageNameCount = db.getLastIDNum()
    # Uses HTML Templates to render images
    #file = open("templates/index.html", "r")
    readFile = html #file.read()  # .read() reads bytes into a string
    loopStartIndex = readFile.find("{{image_loop}}")
    loopEndIndex = readFile.find("{{image_end_loop}}")
    contentPlaceholder = readFile[loopStartIndex + 14:loopEndIndex]

    allImageTagsCaptionLikes = ""
    for image in db.getLatest10Uploads():
        imageID = image[0]
        imageName = image[1].split('/')[1]
        caption = image[2]
        likes = image[3]
        currentImageTag = contentPlaceholder.replace("{{image_filename}}", "/uploadedimage/" + imageName)  # when browser receives our images.html it will make request(s) for the image(s) thru a request url of /image/<image_name> "/image/" is the path we told the browser to request in the html
        #print(currentImageTag)
        allImageTagsCaptionLikes += "<div id=" + "upload" + str(imageID) + ">" + currentImageTag
        allImageTagsCaptionLikes += "<p class="+"image-caption" + " id=" + "image" + str(imageID) + ">" + "Likes ♥: " + str(likes) + "</p>"
        #allImageTagsCaptionLikes += "<br>"
        allImageTagsCaptionLikes += "<p class="+"image-caption"+">" + caption + "</p>" +"</div>"
        allImageTagsCaptionLikes = allImageTagsCaptionLikes.replace("{{uploadID}}", "image"+str(imageID))
        allImageTagsCaptionLikes = allImageTagsCaptionLikes.replace("{{imageToLikeID}}", "'" + "image" + str(imageID) + "'")

    readFile = readFile[:loopStartIndex] + allImageTagsCaptionLikes + readFile[loopEndIndex:]
    readFile = readFile.replace("{{image_loop}}", '')
    readFile = readFile.replace("{{image_end_loop}}", '')
    return readFile

def hostImage(path):
    # Image Hosting
    firstSlash = path.find("/")
    slashBeforeImageName = path.find("/", firstSlash + 1)
    imageName = path[slashBeforeImageName + 1:]
    # imageName = cleanFileName(imageName)
    '''if imageName not in validFiles:
        print("INVALID FILE REQUEST")
        print("CURRENT VALID FILES")
        print(validFiles)
        print("CURRENT FILE NAME REQUESTED: " + imageName)
        return None
    print(f"Path is image path, image name is {imageName}")'''
    try:
        file = open(f"imageUploads/{imageName}", "rb")
        readFile = file.read()  # .read() reads bytes into byte array using "rb"
        #contentLength = len(readFile)
        return readFile
    except FileNotFoundError:
        return None

def querying(path):
    if len(path.split('?')) <= 1: return path, {}
    path, queries = path.split("?")
    result = {}
    for x in queries.split('&'):
        key, val = x.split('=')
        result[key] = val
    return path, result

def escapeHTML(string):
    return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def userFromCookies(header):
    if "Cookie" in header and "token" in header["Cookie"]:
        cookie = header["Cookie"]
        cookie = cookie[cookie.index("token"):]
        return cookie.split("; ")[0].split("=")[1]
    else: return ''
