from flask import request, session
from sqlalchemy import text
from Encoder import sha256
from dbModels.Models import db

def login(username, password):
    # ověření záznamu při přihlášení, vracíme True/False
    query = text("SELECT * FROM users WHERE username = :username AND password = :password")
    # SQL command v textu
    parametres = {"username": request.form['username'], "password": sha256(request.form(password))}
    # práce s databází
    user = db.session.execute(query, parametres).fetchone()
    # execute - parametry zadá to query (metoda sqlalchemy), fetchone() - získání jednoho řádku v databázi z výsledku metody (vrátí řádek nebo None)
    if user:
        session["user"] = {"username": user.username, "id": user.id}
        # na serveru se do session zapíše daný uživatel, tyto hodnoty se po nějaké době vymažou, session je slovník
        return True
        # přihlášení se podařilo
    return False
    # přihlášení se nezdařilo