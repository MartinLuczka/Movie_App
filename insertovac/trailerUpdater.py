import sqlalchemy
from pytube import Search
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def getTrailerUrl(movieName):
    ytVideoID = Search( movieName + " trailer" ).results[0].video_id
    return f"https://www.youtube.com/embed/{ytVideoID}"


if __name__ == "__main__":
    db = sqlalchemy.create_engine( 'sqlite:///../instance/database.db' )

    conn = db.connect()

    filmy = conn.execute(text("SELECT * FROM films")).fetchall()#[:1]


    for film in filmy:
        film = film._asdict()
        trailerUrl = getTrailerUrl( film['title'] )
        try:
            conn.execute(
                text(
                    "UPDATE films SET trailerUrl = :trailerUrl WHERE imdbId = :filmId"
                ),
                {"trailerUrl": trailerUrl, "filmId": film['imdbId']},
            )
            conn.commit()
            print(f"{film['title']} trailer updated")
        except SQLAlchemyError as e:
            print(e)
            conn.rollback()
            print(f"{film['title']} trailer not updated")

    conn.close()
    print("konec")
