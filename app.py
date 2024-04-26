from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from dbModels.Models import db

app = Flask(__name__)

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

@app.route("/prihlaseni", methods = ["GET", "POST"])
def prihlaseni():
    infoMessage = ''
    if request.method == 'POST':

        if login( request.form['username'] , request.form['password'] ):
            return render_template( 'HomePage.html', webTitle='Domovská stránka' )
        else:
            infoMessage = 'Wrong username or password'

    return render_template( 'Login.html', webTitle='Přihlášení' , infoMessage=infoMessage)

