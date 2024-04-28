from crypt import methods

from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy

from dbModels.Models import db
from pyFiles.UserController import login, signup

# používané importy

app = Flask(__name__)
# vytvoření instance samotné Flask aplikace, Třída Flask je hlavním prvkem knihovny Flask, reprezentuje samotnou aplikaci

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# hranatými závorkami vytváříme záznam v konfiguračním slovníku flask aplikace, konfigurace webové aplikace, zavádíme jazyk a název databáze

app.secret_key = "tajny_klic"
# nastavení klíče pro session

#print(app.config) - můžeme si zobrazit konfiguraci aplikace

db.init_app(app)
# připojení databáze k aplikaci

with app.app_context():
    db.create_all()
# vytvoření souboru databáze, poskládání tabulek

@app.route("/")
def home():
    print(session)
    return render_template("HomePage.html", webTitle = "Domovská stránka")
# domovská stránka webu

@app.route("/prihlaseni", methods = ["GET", "POST"])
# stránka řešící přihlášení
def prihlaseni():
    infoMessage = ''
    if request.method == 'POST':
    # Uživatel vyplnit formulář pro přihlášení
        if login(request.form['username'], request.form['password']):
            return redirect("/")
        # Přihlášení se podařilo, uživatel se dostane na domovskou stránku
        else:
            infoMessage = 'Chybné heslo nebo přihlašovací jméno'
        # Přihlášení se nezdaří, informuje me ho o špatně zadaných údajích

    return render_template('Login.html', webTitle='Přihlášení' , infoMessage=infoMessage)
    # uživatel zůstane na stránce přihlášení, proměnnou infoMessage předáváme stránce Login.html

@app.route("/odhlaseni")
# stránka pro odlášení
def odhlaseni():
    session.pop("user", None)
    # ukončení sessionu uživatele
    return redirect("/")
    # po odhlášení přesměrování na domovskou stránku, uživatel již není v session

@app.route("/registrace", methods = ["GET", "POST"])
# stránka pro registraci
def registrace():
    infoMessage = ""
    if request.method == "POST":
        signup_result = signup(request.form["username"], request.form["password"], request.form["password_confirm"])
        # funkce vrací True nebo Error podle toho, jestli se uživatele podařilo zaregistrovat
        if isinstance(signup_result, bool) and signup_result == True:
            # vrátí True, pokud signup_result bude True (boolean hodnota)
            return redirect("/prihlaseni")
        else:
            # pokud signup_result bude error, tak se přepíše do infoMessage
            infoMessage = signup_result
    return render_template("SignUp.html", webTitle = "Registrace", infoMessage = infoMessage)

@app.route("/searchBarProcess", methods = ["POST"])
def searchBarProcess():
    val = request.json["val"]
    # z requestu uděláme json formát a vezmeme si z něj hodnotu val (text v searchBaru)

