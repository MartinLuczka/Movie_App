from flask import request
from sqlalchemy import text
from Encoder import sha256


def login(username, password):
    query = text("SELECT * FROM users WHERE username = :username AND password = :password")
    parametres = {"username": request.form['username'], "password": sha256(request.form(password))}
    # práce s databází