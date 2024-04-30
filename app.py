import datetime

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

@app.route('/film/<filmId>', methods = ["GET", "POST"])
# cesta daná <filmId>, pro každý film unikátní
def filmPage(filmId):
    allReviews = Dbwrapper.getAllReviewsByFilm(filmId)
    # Získáme všechny recenze daného filmu
    film = Dbwrapper.getFilmById(filmId)
    # Získání informací o konkrétním filmu podle jeho IMDb ID
    rating = 0
    # Základní hodnota hodnocení je 0
    user = False
    # Defaultní hodnota pro nepřihlášeného uživatele
    usersReview = None
    # Defaultní hodnota pro to, jestli má uživatel recenzi
    if "user" in session:
        rating = Dbwrapper.getRating(session["user"]["id"], filmId)
        # Pokud je uživatel v sessionu, tak pomocí metody getRating získáme hodnocení konkrétního uživatele pro konkrétní film
        usersReview = Dbwrapper.getReview(session["user"]["id"], filmId)
        # Získáme informaci o tom, jestli má uživatel již recenzi k danému filmu, podle toho budeme přizpůsobovat elementy v HTML
        try:
            for review in allReviews:
                if review.id == usersReview.id:
                    allReviews.remove(review)
        except:
            pass
        # Pokud přihlášený uživatel má recenzi, tak ji vymaž ze všech recenzí
        user = True
        # Kontrola, že je uživatel přihlášen je dána podmínkou, rovnou nastavme do True

    if film:
    # pokud film existuje (nachází se v databázi)
        return render_template( 'film.html', film=film, userRating=rating, user=user, userReview=usersReview, allReviews = allReviews)
        # Vygenerování HTML stránky s informacemi o filmu a zobrazením hodnocení uživatele
    return render_template("film.html", errorMessage = "Film not found")
    # Pokud se stránka s filmem nenajde, tak zahlásíme error

@app.route('/addReview', methods=['POST'])
def addReview():
    if request.method == 'POST' and 'user' in session:
        Dbwrapper.addReview(session['user']['id'], request.form['filmId'], request.form['reviewContent'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return redirect(request.referrer)
        # Odkud jsme request poslali, odkud jsme přišli
    return "chyba"

@app.route('/deleteReview', methods=['POST'])
def deleteReview():
    if request.method == 'POST' and 'user' in session:
        print(request.form)
        Dbwrapper.deleteReview(session['user']['id'] ,request.form['reviewId'] )
        return redirect(request.referrer)
    return "chyba"

@app.route('/hodnoceniFilmu', methods=['POST', 'GET'])
# "stránka" na kterou se zavolá při zhodnocení filmu, volání v JavaScriptu Rating.js
def hodnoceniFilmu():
    # funkce, která zhodnocení filmu zpracovává
    val = request.json
    # získá data z HTTP požadavku jako json objekt a přiřadí ho proměnné val
    print(val)
    # val je zde slovník s daty o hodnocení a filmu, tisk do konzole pro kontrolu

    if 'user' not in session:
        return "notlogedin"
    # Pokud příchozí na stránku film ohodnotí, ale není přihlášen, tak se mu vyhodí hláška pro přihlášení

    print(session['user']['id'], val['filmId'], val['rating'])
    # pro kontrolu si tiskneme id uživatele, id filmu a hodnocení
    result = Dbwrapper.addRating(session['user']['id'], val['filmId'], val['rating'])
    # data posíláme jako parametry funkce, která je pošle na zapsání do databáze
    print(result)
    # Funkce addRating vrací False/True, tento výsledek jsme si uložili a budeme s ním pracovat
    if result:
        return "success"
        # Data se přidala úspěšně a funkce vrátila True, my tím pádem pošleme do JavaScriptu hlášku "success" - úspěch

    return "fail"
    # Pokud se přidání do databáze nezdaří, tak se předchozí podmínka nesplní a do JS pošleme hlášku "fail" - selhání


