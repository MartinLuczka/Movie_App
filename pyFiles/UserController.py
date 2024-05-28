import os
import shutil

from flask import request, session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from pyFiles.Encoder import sha256
from dbModels.Models import db

def login(username, password):
    # ověření záznamu při přihlášení, vracíme True/False
    query = text("SELECT * FROM users WHERE username = :username AND password = :password")
    # SQL command v textu
    parametres = {"username": username, "password": sha256(password)}
    # práce s databází
    user = db.session.execute(query, parametres).fetchone()
    # execute - parametry zadá to query (metoda sqlalchemy), fetchone() - získání jednoho řádku v databázi z výsledku metody (vrátí řádek nebo None)
    if user:
        session["user"] = {"username": user.username, "id": user.id}
        # na serveru se do session zapíše daný uživatel, tyto hodnoty se po nějaké době vymažou, session je slovník
        if f"{session["user"]["id"]}.png" not in os.listdir(f"{os.getcwd()}/static/imgs/profile_pictures"):
        # Pokud uživatel pro svoje ID ještě nemá profilovou fotografii ve složce profile_pictures
        # listdir() - metoda pro ověření přítomnosti souboru, getcwd - vrací cestu aktuálního pracovního adresáře
            shutil.copy(f"{os.getcwd()}/static/imgs/profile_pictures/default.png", f"{os.getcwd()}/static/imgs/profile_pictures/{session["user"]["id"]}.png")
            # Tak zkopíruj soubor defaultního profilového obrázku a ulož ho jako png obrázek daného uživatele podle jeho id, které máme uložené v sessionu
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
    except IntegrityError:
        db.session.rollback()
        # Vrátí se zpět dosud provedené změny
        return "Uživatelské jméno je již zabrané"
        # Pokud nám databáze řekne, že zadané uživatelské jméno již existuje, tak vrátíme hlášku uživatelovi
    except SQLAlchemyError as error:
        db.session.rollback()
        # Vrátí se zpět dosud provedené změny
        return error
    # pokud nastane chyba při zapsání do databáze, tak se vykoná blok kódu except, vrácený error se zapíše do infoMessage
    return True