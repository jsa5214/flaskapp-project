from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key_here'

# Dummy user database
users = {}

# Home page with login status and links to login/register or logout
@app.route('/')
def home():
    if 'username' in session:
        return f"Hello, {session['username']}! <a href='/logout'>Logout</a>"
    return "<a href='/login'>Login</a> | <a href='/register'>Register</a>"

# Private page that requires login
@app.route('/page1')
def page1():   # page1 is a private page
    if 'username' in session:
        return f"Hello, {session['username']}! <a href='/logout'>Logout</a> <br><h1>you are in Page1</h1>"
    return redirect(url_for('login'))

# Registration page to create new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'Username already exists!'
        users[username] = generate_password_hash(password)
        return redirect(url_for('login'))
    return render_template('register.html')

# Login page to authenticate users
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid credentials!'
    return render_template('login.html')

# Logout route to clear the session and redirect to home
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))



# to execute flask app run in code
if __name__ == '__main__':
    app.run(debug=True)
