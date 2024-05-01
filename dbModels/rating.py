from sqlalchemy import func

from dbModels.Models import db

class Rating(db.Model):
    __tablename__ = 'ratings'
    # Příkaz pro název databáze
    filmId = db.Column(db.Integer, db.ForeignKey('films.imdbId'), primary_key=True)
    # Id filmu si bereme z databáze filmů, musí být unikátní
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # Id uživatele si bereme z databáze uživatelů, musí být unikátní
    rating = db.Column(db.Integer, nullable=False)
    # Hodnocení je číslelná hodnota od 1 do 10, nesmí být nenulová
    dateTime = db.Column(db.DateTime, nullable = False, default = func.sysdate())
    # Zjištění času, kdy uživatel provedl hodnocení filmu
    film = db.relationship('Film', backref=db.backref('ratings'))
    # vztah mezi tabulkou ratings a Film (objekt Film bude mít přístup k hodnocením ratings)
    user = db.relationship('User', backref=db.backref('ratings'))
    # vztah mezi tabulkou ratings a User (objekt User bude mít přístup k hodnocením ratings)