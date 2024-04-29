from dbModels.Models import db

class Rating(db.Model):
    __tablename__ = 'ratings'
    filmId = db.Column(db.Integer, db.ForeignKey('films.imdbId'), primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    film = db.relationship('Film', backref=db.backref('ratings'))
    user = db.relationship('User', backref=db.backref('ratings'))