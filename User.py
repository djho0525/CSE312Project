class User:

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
        self.messages = {}      # email: [message1, message2, .......]
