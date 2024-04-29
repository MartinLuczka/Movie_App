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
    def getRating(userId, filmId):
    # Metoda pro získání hodnocení z databáze pro daného uživatele a film
        query = text("SELECT rating FROM ratings WHERE userId = :userId AND filmId = :filmId")
        # Vytvoření SQL dotazu pro získání hodnocení pro konkrétního uživatele a film
        parametres = {"userId": userId, "filmId": filmId}
        # Definice parametrů pro dotaz
        try:
        # Pokus o vykonání SQL dotazu na databázi
            try:
                return db.session.execute(query, parametres).fetchone()[0]
                # Vrácení hodnocení, chceme poslat pouze jeden výsledek na indexu 0
            except TypeError as te:
                return 0
            # Pokud není nalezeno žádné hodnocení, tak se vrátí hodnota 0
        except SQLAlchemyError as e:
            return 0
        # Pokud dojde k chybě při vykonávání dotazu na databázi, vrátí se také hodnota 0

    @staticmethod
    def addRating(userId, filmId, rating):
    # Metoda pro přidání hodnocení do databáze pro daného uživatele a film
        query = text("INSERT INTO ratings (userId, filmId, rating) VALUES (:userId, :filmId, :rating)")
        # Vytvoření SQL dotazu pro vložení nového hodnocení do tabulky ratings
        parametres = {"userId": userId, "filmId": filmId, "rating": rating}
        # Definice parametrů pro dotaz (userId, filmId, rating)
        try:
        # Pokus o provedení SQL dotazu a potvrzení změn v databázi
            db.session.execute(query, parametres)
            db.session.commit()
            print("rating added")
            # Výpis potvrzení, že hodnocení bylo úspěšně přidáno
        except SQLAlchemyError as e:
        # Pokud dojde k chybě při provádění dotazu na databázi
            print(e.orig)
            # Výpis původní chyby
            db.session.rollback()
            # Vrácení změn provedených před chybou
            if isinstance(e.orig, IntegrityError): # Zpracování specifických typů chyb
            # Pokud hodnocení již bylo zadáno, tak se volá pouze funkce pro změnu
                if Dbwrapper.changeRating(userId, filmId, rating):
                    # Volání metody pro změnu hodnocení
                    return True
                    # změna hodnocení se provede a tato funkce vrátí True
            print(e)
            return False
            # Pokud vznikla jiná chyba, chceme si ji vytisknout a vrátit False - hodnocení se neuložilo správně
        return True
        # Pokud nebyla vznesena jakákoliv chyba, tak se vše provedlo správně a můžeme vrátit True

    @staticmethod
    def changeRating(userId, filmId, rating):
    # Metoda pro změnu hodnocení pro daného uživatele a film
        query = text('UPDATE ratings SET rating = :rating WHERE userId = :userId AND filmId = :filmId')
        # Vytvoření SQL dotazu pro aktualizaci hodnocení ve stávajícím záznamu v tabulce ratings
        parametres = {"userId": userId, "filmId": filmId, "rating": rating}
        # Definice parametrů pro dotaz (userId, filmId, rating)
        try:
        # Pokus o provedení SQL dotazu a potvrzení změn v databázi
            db.session.execute(query, parametres)
            db.session.commit()
            print("rating changed")
            # Výpis potvrzení, že hodnocení bylo úspěšně změněno
        except SQLAlchemyError as e:
        # Pokud dojde k chybě při provádění dotazu na databázi
            db.session.rollback()
            # Vrácení změn provedených před chybou
            print(e)
            return False
            # Výpis konkrétní chyby a vrácení hodnoty False
        return True
        # Pokud vše proběhne bez problému, tak funce vrátí True, tím se také splní podmínka v předchozí funkci, která rovněž vrátí True
