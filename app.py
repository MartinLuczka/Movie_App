from flask import Flask, render_template, request, session, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

from dbModels.Models import db
from pyFiles.UserController import login, signup
from pyFiles.dbWrapper import Dbwrapper

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
    # Z requestu uděláme json formát a vezmeme si z něj hodnotu val (text v searchBaru)
    films = Dbwrapper.getFilmbyPartOfTitle(val)
    # Volání metody Dbwrapper.getFilmbyPartOfTitle pro vyhledání filmů podle části názvu
    films = Dbwrapper.rowsToDict(films)
    # Převedení výsledků (seznamu řádků) na seznam slovníků pomocí metody rowsToDict
    return jsonify({"data": films})
    # Vrácení výsledků ve formátu JSON s klíčem "data", obsahující seznam filmů

@app.route('/film/<filmId>')
# cesta daná <filmId>, pro každý film unikátní
def filmPage(filmId):
    film = Dbwrapper.getFilmById(filmId)
    # Získání informací o konkrétním filmu podle jeho IMDb ID
    rating = 0
    # Převedení výsledku na slovník, získání jednoho jediného prvku na indexu 0
    if "user" in session:
        rating = Dbwrapper.getRating(session["user"]["id"], filmId)
    if film:
        return render_template( 'film.html', film=film, usersRating=rating)
        # Vygenerování HTML stránky s informacemi o filmu a zobrazením hodnocení uživatelů
    return render_template("film.html", errorMessage = "Film not found")

@app.route('/hodnoceniFilmu', methods=['POST', 'GET'])
def hodnoceniFilmu():
    val = request.json
    print(val)

    if 'user' not in session:
        return "notlogedin"

    print(session['user']['id'], val['filmId'], val['rating'])
    result = Dbwrapper.addRating( session['user']['id'], val['filmId'], val['rating'] )
    print(result)
    if result:
        return "success"

    return "fail"


