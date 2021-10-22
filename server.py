from flask import Flask, render_template, request
import database as db

app = Flask(__name__)

@app.route('/')
def startupPage():
    return render_template('login.html')    # render_template looks at 'templates' as root folder


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if db.userExists(email):
        user = db.getUser(email)
        if user.password == password: print('Logged in successfully')
        else: print('Login failed')

    else: print('Username does not exist')
    return


@app.route('/signUp', methods=['POST'])
def signUp():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    conf_password = request.form['confirm_password']

    if db.userExists(email): print('Email was already registered')
    else:
        if password == conf_password:
            db.addUser(email, password, name)
            print('Created account successfully')
        else: print('Passwords do not match')
    return


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)
