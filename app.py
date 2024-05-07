import datetime

from flask import Flask, render_template, request, session, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

from dbModels.Models import db
from pyFiles.UserController import login, signup
from pyFiles.dbWrapper import Dbwrapper
from pyFiles.GetData import findDirector, findActors

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

@app.route('/user/<int:id>')
# Cesta pro zobrazení profilu uživatele, id uživatele zde máme jako parametr
def userPage(id):
# Funkce, zajišťující načtení stránky profilu uživatele
    user = Dbwrapper.getUserById(id)
    # informace o uživateli získáme zavoláním metody, tyto informace si uložíme do proměnné user
    if user:
    # Pokud jsme o něm nějaké informace zjistili
        usersRatings = None
        usersReviews = None
        # Nastavení proměnných do počátečních hodnot
        try:
            usersRatings = Dbwrapper.getRatingsByUserId(id)
            # Uživatelovi hodnocení si zkusíme uložit do proměnné
        except Exception as e:
            print(e)
            # Pokud se vyskytne vyjímka, tak si ji budeme chtít zobrazit v konzoli
        try:
            usersReviews = Dbwrapper.getReviewsByUserId(id)
            # Uživatelovi recenze si zkusíme uložit do proměnné
        except Exception as e:
            print(e)
            # Pokud se vyskytne vyjímka, tak si ji budeme chtít zobrazit v konzoli
        return render_template('User.html', user=user, usersRatings = usersRatings, usersReviews = usersReviews)
        # Vracíme načtení stránky HTML dokumentu, do kterého si posíláme získaná data pro vhodné zobrazení
    return render_template('User.html', errorMessage='User not found')
    # Pokud jsme nenašli uživatele, tak načteme stránku vyjadřující, že se vyskytla chyba

@app.route('/film/<filmId>', methods = ["GET", "POST"])
# cesta daná <filmId>, pro každý film unikátní
def filmPage(filmId):
    director_name = findDirector(filmId)
    # Získáme jméno režiséra daného filmu
    actors = findActors(filmId)
    # Získáme seznam (hlavních) herců, kteří hrají v daném filmu
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
    allReviewsWithoutLoggedinUser = []
    # Nastavení základní hodnoty pro náš seznam všech recenzí (mimo přihlášeného uživatele)
    try:
        allReviews = Dbwrapper.rowsToDict(allReviews)
        # Recenze daného filmu si zkusíme převést metodou na seznam
    except Exception as e:
        print(e)
        # Chyba, pokud nejsou žádné recenze
    if "user" in session:
        rating = Dbwrapper.getRating(session["user"]["id"], filmId)
        # Pokud je uživatel v sessionu, tak pomocí metody getRating získáme hodnocení konkrétního uživatele pro konkrétní film
        usersReview = Dbwrapper.getReview(session["user"]["id"], filmId)
        # Získáme informaci o tom, jestli má uživatel již recenzi k danému filmu, podle toho budeme přizpůsobovat elementy v HTML
        try:
        # Logika pro odstranění naší recenze ze všech recenzí (naši si budeme zobrazovat vždy samostatně nahoře)
            for review in allReviews:
            # projíždíme si jednotlivě recenze v allReviews
                if review.id == usersReview.id:
                # Pokud je některé id recenze totožné s id naší recenze
                    allReviews.remove(review)
                    # Tak tuto recenzi chceme ze všech recenzí vymazat
        except:
        # Pokud se při cyklu něco pokazí
            pass
            # Tak nás to nezajímá a tuto část přeskočíme
        # (popis celého try/except bloku): Pokud přihlášený uživatel má recenzi, tak ji vymaž ze všech recenzí
        user = True
        # Kontrola, že je uživatel přihlášen je dána podmínkou, rovnou nastavme do True

    if allReviews:
        # Pokud máme nějaké recenze
        print(allReviews)
        # Recenze si vypíšeme do konzole

        for i, review in enumerate(allReviews):
            # Pro každou recenzi v seznamu
            print(review)
            # V každém projetí cyklem si vypíšeme recenzi, se kterou se pracuje
            reviewRatings = Dbwrapper.rowsToDict(Dbwrapper.getReviewRatings(review['id']))
            # Všechny hodnocení k jednotlivým recenzím
            ratings = {"thumbsup": 0, "thumbsdown": 0}
            # Základní hodnoty hodnocení

            if reviewRatings:
            # Pokud existují hodnocení k recenzi
                for reviewRating in reviewRatings:
                    # Pro každé hodnocení k recenzi
                    if reviewRating['rating'] == 1:
                    # Pokud je hodnocení v databázi 1
                        ratings["thumbsup"] += 1
                        # Přičti 1 k palcům nohoru
                    elif reviewRating['rating'] == 0:
                    # Nebo pokud je hodnocení v databázi 0
                        ratings["thumbsdown"] += 1
                        # Přičti jedničku k palcům dolů

                    if 'user' in session:
                    # Pokud je uživatel přihlášen
                        if reviewRating['user'] == session['user']['id']:
                            # Pokud se uživatel daného hodnocení shoduje s přihlášeným uživatelem
                            review['logedinUsersReviewRating'] = reviewRating['rating']
                            # Uloží hodnocení přihlášeného uživatele do recenze
                        else:
                            review['logedinUsersReviewRating'] = -1
                            # Jinak nastaví hodnocení na -1 (uživatel není autorem hodnocení)
            review['reviewRatings'] = ratings
            # Přiřadí počet lajků a dislajků do recenze
            try:
                if review['user'] == session['user']['id']:
                    usersReview = review
                    # Zkusíme zkontrolovat podmínku - Pokud je uživatel autorem recenze, uloží recenzi do proměnné usersReview
                else:
                    allReviewsWithoutLoggedinUser.append(review)
                    # Jinak přidá recenzi do seznamu allReviewsWithoutLoggedinUser
            except Exception as e:
            # Pokud dojde k chybě
                print(e)
                # Chybu si vytiskneme do konzole

    if film:
    # Pokud film existuje (nachází se v databázi)
        return render_template( 'film.html', film=film, userRating=rating, user=user, userReview=usersReview, allReviews = allReviewsWithoutLoggedinUser, director_name = director_name, actors = actors)
        # Vygenerování HTML stránky s informacemi o filmu a zobrazením hodnocení uživatele
    return render_template("film.html", errorMessage = "Film not found")
    # Pokud se stránka s filmem nenajde, tak zahlásíme error

@app.route('/addReview', methods=['POST'])
def addReview():
# Funkce, kterou voláme při vyplnění formuláře v HTML
    if request.method == 'POST' and 'user' in session:
        # Pokud uživatel pošle recenzi na server a také je přihlášen (je v sessionu)
        Dbwrapper.addReview(session['user']['id'], request.form['filmId'], request.form['reviewContent'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # Voláme metodu, která nám přidá recenzi do databáze, posíláme id uživatele, id filmu, obsah recenze a také čas přidání recenze
        return redirect(request.referrer)
        # Přesměrování tam, odkud jsme request poslali, odkud jsme přišli
    return "chyba"
    # Tato situace by neměla nastat, vyřešeno podmínkami v html dokumentu

@app.route('/deleteReview', methods=['POST'])
def deleteReview():
# Tuto funkci voláme, pokud zmáčkneme v html tlačítko pro smazání naší recenze
    if request.method == 'POST' and 'user' in session:
    # Pokud je požadavek "POST" a uživatel je v sessionu (je přihlášen)
        Dbwrapper.deleteReview(session['user']['id'], request.form['reviewId'])
        # Voláme metodu, která z databáže vymaže uživatelovu recenzi, předáváme id uživatele a také id recenze
        return redirect(request.referrer)
        # Přesměrování tam, odkud jsme request poslali, odkud jsme přišli
    return "chyba"
    # Tato situace by neměla nastat, vyřešeno podmínkami v html dokumentu

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

    print(session['user']['id'], val['filmId'], val['rating'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # pro kontrolu si tiskneme id uživatele, id filmu, hodnocení a čas hodnocení
    result = Dbwrapper.addRating(session['user']['id'], val['filmId'], val['rating'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # data posíláme jako parametry funkce, která je pošle na zapsání do databáze
    print(result)
    # Funkce addRating vrací False/True, tento výsledek jsme si uložili a budeme s ním pracovat
    if result:
        return "success"
        # Data se přidala úspěšně a funkce vrátila True, my tím pádem pošleme do JavaScriptu hlášku "success" - úspěch
    return "fail"
    # Pokud se přidání do databáze nezdaří, tak se předchozí podmínka nesplní a do JS pošleme hlášku "fail" - selhání

@app.route('/setReviewRating', methods=["POST"])
# URL na kterou se posílají data o recenzi a jejího hodnocení z JavaScript souboru
def setReviewRating():
# Funkce, pro nastavení hodnocení recenze
    if request.method == "POST":
    # Pokud se něco poslalo
        print(request)
        print(request.json)
        # Data si pracovně vypíšeme do konzole
        Dbwrapper.setReviewRating(session['user']['id'], int(request.json['reviewId']), int(request.json['rating']))
        # JSON data z JavaScriptu si jednotlivě posíláme jako parametry pro metodu na změnu stavu recenze
        return "success"
        # Vše se provedlo v pořádku, hodnocení recenze se upravilo
    return "fail"
    # Něco se pokazilo, metoda se nezaznamenala jako POST
