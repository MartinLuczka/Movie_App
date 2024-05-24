from dbModels.Models import db

class Film(db.Model):
    __tablename__ = 'films'
    # nastavujeme jméno tabulky, jinak by si databáze vzala jméno třídy

    imdbId = db.Column(db.String(9), primary_key=True)
    # 2 písmena 7 čísel
    title = db.Column(db.String(80), unique=True, nullable=False)
    # název filmu, musí být unikátní, nesmí být nenulový
    year = db.Column(db.Integer,  nullable=False)
    # rok vydání filmu, nesmí být nenulový
    imdbRating = db.Column(db.Float,  nullable=False)
    # hodnocení z IMBD, nesmí být nenulové

    director = db.Column(db.JSON)
    # režisér, zapisujeme JSON dictionary
    actors = db.Column(db.JSON)
    # herci, zapisujeme JSON dictionary

    description = db.Column(db.String(600))
    # popis filmu - max. 600 znaků
    posterImgSrc = db.Column(db.String(120))
    # URL adresa plagátu filmu, max 120. znaků
    trailerUrl = db.Column(db.String(200))
    # URL adresa traileru, max. 200 znaků

    def __repr__(self):
        return '<Film %r %d>' % (self.title, self.year)
    # metoda, která vrací námi zformátovaný popis třídy, je to string