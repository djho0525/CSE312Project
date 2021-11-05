import socketserver
import responses

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        received_data = self.request.recv(1024)
        client_id = self.client_address[0] + ":" + str(self.client_address[1])

        request_line = received_data.strip().decode().split('\r\n')[0].split(' ')  # ie. ["GET", "/", "HTTP/1.1"]
        request_type, path = request_line[0], request_line[1]

        if request_type == "GET": response = responses.getResponse(self, path, received_data)
        else: response = responses.postResponse(self, path, received_data)

        self.request.sendall(response)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8001

    print('Running on ' + str(port))
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()
