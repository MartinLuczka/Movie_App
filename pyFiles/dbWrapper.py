from sqlalchemy import text
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
