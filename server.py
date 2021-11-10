import socketserver
import responses as r
import WebSocketHandler

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        received_data = self.request.recv(1024)
        client_id = self.client_address[0] + ":" + str(self.client_address[1])

        request_line = received_data.strip().decode().split('\r\n')[0].split(' ')  # ie. ["GET", "/", "HTTP/1.1"]
        request_type, path = request_line[0], request_line[1]

        if r.storedUser in r.userToServer:
            s = r.userToServer.pop(r.storedUser)
            r.userToServer[r.storedUser] = s
            r.serverToUser[self] = r.storedUser
            # print(r.storedUser + " made a request:")

        if request_type == "GET": response = r.getResponse(self, path, received_data)
        else: response = r.postResponse(self, path, received_data)

        self.request.sendall(response)
        if path == "/websocket":  # establish a websocket connection after serving the home page
            WebSocketHandler.webSocketConnection(self)

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8001

    print('Running on ' + str(port))
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()
