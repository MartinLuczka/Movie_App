from dbModels.Models import db

class ReviewRating(db.Model):
    __tablename__ = 'reviewRatings'
    # Název tabulky databáze
    user = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    # Jaký uživatel recenzi ohodnotil, bereme z tabulky "users"
    review = db.Column(db.Integer, db.ForeignKey('reviews.id'), primary_key=True, nullable=False)
    # Jakou recenzi uživatel ohodnotil, bereme z tabulky "reviews" (v ní je poté dáno i jaký je to film...)
    rating = db.Column(db.Boolean, nullable=False)
    # Hodnocení, které uživatel přidal, False - palec dolů, True - palec nahoru

    def __repr__(self):
        return '<Review %d %d %s>' % (self.user, self.review, self.date)