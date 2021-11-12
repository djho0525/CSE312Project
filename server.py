import socketserver
import responses as r
import WebSocketHandler

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        received_data = self.request.recv(1024)
        client_id = self.client_address[0] + ":" + str(self.client_address[1])

        request_line = received_data.strip().split('\r\n'.encode())[0].split(' '.encode())  # ie. ["GET", "/", "HTTP/1.1"]
        request_type, path = request_line[0].decode(), request_line[1].decode()

        if request_type == "GET": response = r.getResponse(self, path, received_data)
        else: response = r.postResponse(self, path, received_data)

        self.request.sendall(response)
        if path == "/websocket":  # establish a websocket connection after serving the home page
            data = received_data.decode()
            userFromCookie = data[data.index("user="):].split("\r\n")[0].split("; ")[0].split("=")[1]
            WebSocketHandler.webSocketConnection(self, userFromCookie)

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8001

    print('Running on ' + str(port))
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()
