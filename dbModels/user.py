from dbModels.Models import db

# vytvoření třídy pro uživatele
class User(db.Model): # user - v pythonu chceme pracovat s jedním uživatelem
    __tablename__ = "users" 
    # nastavujeme jméno tabulky, jinak by si databáze vzala jméno třídy

    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    # primary_key - hlavní identifikátor záznamu v tabulce (musí být unikátní); autoincrement - databáze si sama doplní unikátní identifikační číslo
    username = db.Column(db.String(45), unique = True, nullable = False) 
    # unique - uživ. jméno musí být unikátní, max počet znaků: 45, nullable - Může být nulová hodnota ? - v našem případě nemůže
    password = db.Column(db.String(64), nullable = False)
    # heslo nemusí být unikátní, nesmí být nulové, jeho délka bude 64 znaků - použijeme SHA256
    image_file_name = db.Column(db.String(100), nullable = False)
    # Název profilového obrázku, je to string, nesmí být nulový (každý profil má defaultní obrázek)
    description = db.Column(db.String(1000), nullable = True)
    # Popisek O MNĚ, je to string - povolen velký počet znaků, může být nulový, uživatel nemusí mít popisek v profilu

    def __repr__(self):
        return "User " + self.username
    # funkce, která vrací string - string reprezentuje/popíše objekt
