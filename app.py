from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from dbModels.Models import db
from pyFiles.UserController import login

# používané importy

app = Flask(__name__)
# vytvoření instance samotné Flask aplikace, Třída Flask je hlavním prvkem knihovny Flask, reprezentuje samotnou aplikaci

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# hranatými závorkami vytváříme záznam v konfiguračním slovníku flask aplikace, konfigurace webové aplikace, zavádíme jazyk a název databáze

#print(app.config) - můžeme si zobrazit konfiguraci aplikace

db.init_app(app)
# připojení databáze k aplikaci

with app.app_context():
    db.create_all()
# vytvoření souboru databáze, poskládání tabulek

@app.route("/")
def home():
    return "Hello, Flask!"
# domovská stránka webu

@app.route("/prihlaseni", methods = ["GET", "POST"])
# stránka řešící přihlášení
def prihlaseni():
    infoMessage = ''
    if request.method == 'POST':
    # Uživatel vyplnit formulář pro přihlášení
        if login(request.form['username'], request.form['password']):
            return render_template('HomePage.html', webTitle='Domovská stránka')
        # Přihlášení se podařilo, uživatel se dostane na domovskou stránku
        else:
            infoMessage = 'Wrong username or password'
        # Přihlášení se nezdaří, informuje me ho o špatně zadaných údajích

    return render_template('Login.html', webTitle='Přihlášení' , infoMessage=infoMessage)
    # uživatel zůstane na stránce přihlášení, proměnnou infoMessage předáváme stránce Login.html

