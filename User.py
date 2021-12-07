class User:

    def __init__(self, email, password, name, token):
        self.email = email
        self.password = password
        self.name = name
        self.token = token
        self.messages = {}      # email: [message1, message2, .......]
