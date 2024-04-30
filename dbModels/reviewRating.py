from dbModels.Models import db

class ReviewRating(db.Model):
    __tablename__ = 'reviewRatings'

    user = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    review = db.Column(db.Integer, db.ForeignKey('reviews.id'), primary_key=True, nullable=False)
    rating = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Review %d %d %s>' % (self.user, self.review, self.date)