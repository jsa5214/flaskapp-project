from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
from datetime import date

app = Flask(__name__)

def calculAnyEdat100(edatAvui):
    any100=None
    if edatAvui < 100:
        any100 = date.today().year + (100 - edatAvui)
    return any100

@app.route("/")
def inici():
    return redirect(url_for('formEdat100'))

@app.route("/edat100/<nom>/<int:edat>")
def edat100(nom, edat):
    any100=calculAnyEdat100(edat)
    return render_template("edat100.html",name=escape(nom),any100=any100)

@app.route("/edat100/", methods = ['POST', 'GET'])
def formEdat100():
    if request.method == 'GET':
        # mostra el formulari per introduir nom i edat
        return render_template("formEdat.html") 
    else:
        # (mètode POST) recull les dades el formulari i fa el càlcul de l'any que farà 100 anys
        nom = request.form['nom']  # recull nom del formulari
        try:
            edat = int(request.form['edat']) # recull edat del formulari i intenta convertir a int
            any100=calculAnyEdat100(edat) # calcula any que farà 100 anys
            return render_template("edat100.html",name=escape(nom),any100=any100) # mostra resultat
        except: 
            # si no es pot convertir a int, torna a mostrar el formulari
            return render_template("formEdat.html")
