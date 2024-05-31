import time

import sqlalchemy
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

import requests # http requesty
from bs4 import BeautifulSoup # knihovna pro parsovani

headers = {  # hlavicka, kde je nejake info navic, aby nas IMDb pustilo
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "cs-CZ,cs;q=0.8"
    }

def getSoup(url):
    start_time = time.time()

    # Send a GET request to the URL with headers
    response = requests.get( url, headers=headers )

    elapsed_time = time.time() - start_time

    soup = BeautifulSoup( response.content, 'html.parser' )

    print( f"cas getSoup: {elapsed_time:.2f} seconds" )

    return soup


def getcsfd_description(movie_name):
    try:
        soup = getSoup( 'https://www.csfd.cz/hledat/?q=' + movie_name )
        section = soup.find( "section", class_="box main-movies" )
        urlFilmu = 'https://www.csfd.cz/' + section.find( 'a', class_="film-title-name" ).get_attribute_list( "href" )[0]
    except Exception as e:
        print(e)
        return None

    try:
        soup = getSoup(urlFilmu)
        description = soup.find( "div", class_="plot-full" ).findChild( "p" ).text
        print(description.split('\n')[1].strip())
        return description.split('\n')[1].strip()
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    # getcsfd_description("terminator")
    # exit()
    db = sqlalchemy.create_engine( 'sqlite:///../instance/database.db' )

    conn = db.connect()

    filmy = conn.execute(text("SELECT * FROM films")).fetchall()


    for film in filmy:
        film = film._asdict()
        filmDescription = getcsfd_description(film['title'])
        if filmDescription is None:
            filmDescription = "Chyba"
        try:
            conn.execute(
                text(
                    "UPDATE films SET description = :filmDescription WHERE imdbId = :filmId"
                ),
                {"filmDescription": filmDescription, "filmId": film['imdbId']},
            )
            conn.commit()
            print(f"{film['title']} description updated")
        except SQLAlchemyError as e:
            print(e)
            conn.rollback()
            print(f"{film['title']} description not updated")

    conn.close()
    print("konec")