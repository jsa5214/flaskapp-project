"""
From https://www.learnpython.dev/03-intermediate-python/80-web-frameworks/basic-flask/

Els exemples de <<A Basic Flask App >>
"""

from flask import Flask
from flask import render_template

app = Flask(__name__)

# exemples inicials
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/my/secret/page")
def secret():
    return "Shh!"

@app.route("/user/<username>")
def user_page(username):
    return f"Welcome, {username}!"

@app.route("/blog/post/<int:post_id>")
def show_post(post_id):
    return f"This is the page for post # {post_id}"

# l'exercici parell senar fet com a webapp
# el numero arriba a la URL
@app.route("/parellsenar/<int:num>")
def parellsenar(num):
    if num % 2 == 0:
        return f"El numero {num} es parell"
    else:
        return f"El numero {num} es senar"

# Reposta amb fitxer HTML
# Ha d'estar a la carpeta templates
# El fitxer HTML es una plantilla Jinja que admet variables
@app.route('/hello/')
@app.route('/hello/<nom>')
def hello2(nom=None):
    return render_template('index.html', name=nom)


@app.route("/projects/")  #admet /projects i /projects/ (per /projects fa un redirect a /projects/)
def projects():
    return f"Estic a projects"

@app.route("/about")    #nomes admet /about, si posem la / al final dona error 404
def about():
    return f"Estic a about"

