from dbModels.film import Film

def findDirector(filmId):
    # Funkce na získání režiséra určitého filmu z databáze
    film = Film.query.filter_by(imdbId=filmId).first()
    # Film najdeme podle jeho Id, které si posíláme do této funkce jako parametr, bereme hned první výsledek, v našem případě i jediný
    director_data = film.director
    # Data o režisérovi (slovník) si uložíme do proměnné
    return director_data["name"]
    # Jméno si vrátíme pomocí klíče "name"

def findActors(filmId):
    # Funkce na získání seznamů herců daného filmu
    film = Film.query.filter_by(imdbId=filmId).first()
    # Film najdeme podle jeho Id, které si zde posíláme
    actors_data = film.actors
    # Data o hercích si uložíme do proměnné, je to seznam slovníků
    list_of_actors = []
    # Vytvoření listu, do kterého budeme ukládat herce
    for actor in actors_data:
        list_of_actors.append(actor["name"])
    # Pomocí for cyklu projedeme všechny slovníky seznamu a do seznamu herců si uložíme poouze jejich jména pomocí klíče "name"
    return list_of_actors
    # Vracíme seznam herců (jen jejich jmen)