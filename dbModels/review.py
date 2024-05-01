from sqlalchemy import func

from dbModels.Models import db

class Review(db.Model):
    __tablename__ = 'reviews'
    # Název tabulky
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    # id dané recenze, musí být unikátní, databáze si ho spravuje sama
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # id uživatele, který recenzi napsal, bereme si z databáze "users"
    film = db.Column(db.Integer, db.ForeignKey('films.imdbId'), nullable=False)
    # id filmu, ke kterému uživatel přidal recenzi, bereme si z databáze "films"
    content = db.Column(db.String(600), nullable=False)
    # Obsah recenze, max. počet znaků 600
    date = db.Column(db.DateTime, nullable=False, default=func.sysdate())
    # Čas/datum, kdy byla recenze uživatelem napsána

    def __repr__(self):
        return '<Review %r %d %s>' % (self.user, self.film, self.date)
        # Při zavolání si zjistíme daná data, neovlivňuje nijak funčnost