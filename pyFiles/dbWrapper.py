from sqlite3 import IntegrityError

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from dbModels.Models import db


class Dbwrapper:
# Definice třídy Dbwrapper pro práci s databází

    @staticmethod
    def getFilmbyPartOfTitle(partOfTitle):
    # Statická metoda pro získání filmů podle části jejich názvu
        query = text(
            'SELECT * FROM films WHERE title LIKE \'%\' || :title || \'%\''
            'ORDER BY rating DESC'
        )
        # Sestavení SQL dotazu pomocí SQLAlchemy objektu text
        parametres = {"title": partOfTitle}
        # Parametry pro dotaz - část názvu filmu
        return db.session.execute(query, parametres).fetchall()
        # fetchall - protože chceme všechny filmy, které vyhovují naším podmínkám

    @staticmethod
    def rowsToDict(rows):
    # Statická metoda pro převod řádků na seznam slovníků
        if rows is None:
            return []
        # Pokud je vstupní seznam prázdný nebo None, vrátí se prázdný seznam
        return [row._asdict() for row in rows]
        # Jinak provede převod každého řádku na slovník a vrátí seznam slovníků

    @staticmethod
    def getFilmById(id):
    # Statická metoda pro získání filmu podle IMDb ID
        query = text('SELECT * FROM films WHERE imdbId = :imdbId')
        # Sestavení SQL dotazu pro vyhledání filmu podle IMDb ID
        params = {"imdbId": id}
        # Parametry pro dotaz - IMDb ID
        return db.session.execute( query, params ).fetchone()
        # Použití fetchone() pro získání jednoho řádku odpovídajícího dotazu

    @staticmethod
    def getRating( userId, filmId ):
        query = text(
            'SELECT rating FROM ratings'
            ' WHERE userId = :userId AND filmId = :filmId'
        )
        params = {"userId": userId, "filmId": filmId}
        try:
            try:
                return db.session.execute( query, params ).fetchone()[0]
            except TypeError as te:
                return 0
        except SQLAlchemyError as e:
            return 0

    @staticmethod
    def addRating(userId, filmId, rating):
        query = text("INSERT INTO ratings (userId, filmId, rating) VALUES (:userId, :filmId, :rating)")
        parametres = {"userId": userId, "filmId": filmId, "rating": rating}
        try:
            db.session.execute(query, parametres)
            db.session.commit()
            print("rating added")
        except SQLAlchemyError as e:
            print(e.orig)
            db.session.rollback()
            if isinstance(e.orig, IntegrityError):
                if Dbwrapper.changeRating(userId, filmId, rating):
                    return True
            print(e)
            return False
        return True

    @staticmethod
    def changeRating(userId, filmId, rating):
        query = text(
            'UPDATE ratings SET rating = :rating WHERE userId = :userId AND filmId = :filmId')
        params = {"userId": userId, "filmId": filmId, "rating": rating}
        try:
            db.session.execute(query, params)
            db.session.commit()
            print("rating changed")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return False
        return True
