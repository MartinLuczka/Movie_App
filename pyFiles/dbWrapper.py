from sqlalchemy import text
from dbModels.Models import db


class Dbwrapper:

    @staticmethod
    def getFilmbyPartOfTitle(partOfTitle):
        query = text(
            'SELECT * FROM films WHERE title LIKE \'%\' || :title || \'%\''
            'ORDER BY rating DESC'
        )
        parametres = {"title": partOfTitle}
        return db.session.execute(query, parametres).fetchall()
        # fetchall - protože chceme všechny filmy, které vyhovují naším podmínkám

    @staticmethod
    def rowsToDict(rows):
        if rows is None:
            return []
        return [row._asdict() for row in rows]
