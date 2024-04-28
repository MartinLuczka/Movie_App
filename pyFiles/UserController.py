from flask import request, session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from pyFiles.Encoder import sha256
from dbModels.Models import db

def login(username, password):
    # ověření záznamu při přihlášení, vracíme True/False
    query = text("SELECT * FROM users WHERE username = :username AND password = :password")
    # SQL command v textu
    parametres = {"username": request.form['username'], "password": sha256(request.form["password"])}
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

def signup(username, password, password_confirm):
    if password != password_confirm:
        return "Zadaná hesla se neshodují"
    query = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    # SQL command - vložení záznamu do tabulky
    parametres = {"username": username, "password": sha256(password)} # heslo zakódujeme pomocí funkce
    # parametry pro SQL command (VALUES)
    try:
        db.session.execute(query, parametres)
        db.session.commit()
        # vložení hodnot do databáze
    except SQLAlchemyError as error:
        return error
    # pokud nastane chyba při zapsání do databáze, tak se vykoná blok kódu except, vrácený error se zapíše do infoMessage
    return True