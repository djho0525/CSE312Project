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
        if user.password == password: return 'Logged in successfully'
        else: return 'Login failed'

    else: return 'Email is not registered'


@app.route('/signUp', methods=['POST'])
def signUp():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if db.userExists(email): return 'Email was already registered'
    else:
        if password == confirm_password:
            db.addUser(email, password, name)
            return 'Created account successfully'
        else: return 'Passwords do not match'


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)
