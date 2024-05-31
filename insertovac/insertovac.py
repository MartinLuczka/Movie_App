import json
import time

import sqlalchemy
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from scraper import ScraperFilmy

def addFilms(films):
    start_time = time.time()

    query = text( \
        'insert into films (imdbId, title, year, rating, description, director, actors, posterImgSrc, trailerUrl) \
          values (:imdbId, :title, :year, :rating, :description, :director, :actors, :posterImgSrc, :trailerUrl);' )

    for film in films:
        try:
            conn.execute( query,
                {
                'imdbId': film['imdbId'],
                 'title': film['title'],
                 'year': film['year'],
                 'rating': film['rating'],
                 'genres': film["genres"],
                 'director': json.dumps(film["director"]),
                 'actors': json.dumps(film["actors"]),
                 'description': film['description'],
                 'posterImgSrc': film['posterUrl'],
                 'trailerUrl': film['trailerUrl'],
                 } )

            elapsed_time = time.time() - start_time
            print( f"cas filmInfo: {elapsed_time:.2f} seconds" )
        except SQLAlchemyError as e:
            print( "Error: {}".format( e ) )
            conn.rollback()
    conn.commit()

def filmIdExists(id):
    query = text( 'SELECT * FROM films WHERE imdbId = :imdbId' )
    params = {"imdbId": id}
    return conn.execute( query, params ).fetchone()

def addFilm(film):
    print( film )
    query = text( \
        'insert into films (imdbId, title, year, rating, description, director, actors, posterImgSrc, trailerUrl) \
          values (:imdbId, :title, :year, :rating, :description, :director, :actors, :posterImgSrc, :trailerUrl);' )
    try:
        for par in film:
            print( f'{par}: {film[par]} {type(film[par])}' )

        conn.execute( query,
            {
            'imdbId': film['imdbId'],
             'title': film['title'],
             'year': film['year'],
             'rating': film['rating'],
             'genres': film["genres"],
             'director': json.dumps(film["director"]),
             'actors': json.dumps(film["actors"]),
             'description': film['description'],
             'posterImgSrc': film['posterUrl'],
             'trailerUrl': film['trailerUrl'],
             } )
        conn.commit()
    except SQLAlchemyError as e:
        print( "Error: {}".format( e ) )
        conn.rollback()
        return False
    return True

if __name__ == '__main__':
    db = sqlalchemy.create_engine( 'sqlite:///../instance/database.db' )

    conn = db.connect()

    scraper = ScraperFilmy()

    filmy = []

    start_time = time.time()

    for id in scraper.getTop250Ids(250):
        if filmIdExists(id) is None:
            print( "NOVYYYYYYYYYYYY" )
            film = scraper.getFilmInfo( id )
            if film:
                filmy.append( film )

    #print(json.dumps(filmy, indent=4))
    addFilms(filmy)

    conn.close()

    elapsed_time = time.time() - start_time
    print( f"cas HOTOVO: {elapsed_time:.2f} seconds" )


    def addFilms(films):
     start_time = time.time()

     query = text( \
         'insert into films (imdbId, title, year, rating, description, director, actors, posterImgSrc, trailerUrl) \
           values (:imdbId, :title, :year, :rating, :description, :director, :actors, :posterImgSrc, :trailerUrl);' )
     try:
         [conn.execute( query,
             {
             'imdbId': film['imdbId'],
              'title': film['title'],
              'year': film['year'],
              'rating': film['rating'],
              'genres': film["genres"],
              'director': json.dumps(film["director"]),
              'actors': json.dumps(film["actors"]),
              'description': film['description'],
              'posterImgSrc': film['posterUrl'],
              'trailerUrl': film['trailerUrl'],
              } ) for film in films]
         conn.commit()

         elapsed_time = time.time() - start_time
         print( f"cas filmInfo: {elapsed_time:.2f} seconds" )
     except SQLAlchemyError as e:
         print( "Error: {}".format( e ) )
         conn.rollback()
         return False
     return True