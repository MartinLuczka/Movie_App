from sqlalchemy import func

from dbModels.Models import db

class Review(db.Model):
    __tablename__ = 'reviews'
    # Název tabulky
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    film = db.Column(db.Integer, db.ForeignKey('films.imdbId'), unique=True, nullable=False)
    content = db.Column(db.String(600), nullable=False)
    # Obsah recenze, max. počet znaků 600
    date = db.Column(db.DateTime, nullable=False, default=func.sysdate())

    def __repr__(self):
        return '<Review %r %d %s>' % (self.user, self.film, self.date)
        # Při zavolání si zjistíme daná data, neovlivňuje nijak funčnost