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
    # print(header)
    request_line = header.split('\r\n')
    content_len = int(request_line[3].split(' ')[1])        # Content-Length: num
    while content_len-len(body) > 0:
        body += server.request.recv(1024)
    return header, body.strip()

def parsing(data):
    form = dict()
    for f_input in data.split('&'):
        name, value = f_input.split('=')
        form[name] = value
    return form

def querying(path):
    if len(path.split('?')) <= 1: return path, {}
    path, queries = path.split("?")
    result = {}
    for x in queries.split('&'):
        key, val = x.split('=')
        result[key] = val
    return path, result
