import json

import requests # http requesty
from bs4 import BeautifulSoup # knihovna pro parsovani
import time

from sqlalchemy import text


class ScraperFilmy:
    urlTop = "https://www.imdb.com/chart/top"  # url odkud si vytahneme html
    urlFilm = "https://www.imdb.com/title/"  # url odkud si vytahneme html

    headers = {  # hlavicka, kde je nejake info navic, aby nas IMDb pustilo
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5",  # Set the Accept-Language header to English (United States)
        #"Accept-Language": "cs-CZ,cs;q=0.8"
    }

    def getFilmInfoL(self, id):
        soup = self.getSoup( self.urlFilm + id)
        start_time = time.time()
        info = {}

        main = soup.find( "main" )

        info["title"] = main.find( "span", class_="hero__primary-text").text

        vrchniSekce = main.find( "div", class_="sc-4e4cc5f9-3 dDRspk")

        levaPodNazvem = vrchniSekce.find_all("li", attrs={"role": "presentation"})
        info["year"] = levaPodNazvem[0].text
        info["length"] = levaPodNazvem[2].text

        info["rating"] = vrchniSekce.find( "span", class_="sc-bde20123-1 cMEQkK" ).text


        genres = main.find_all( "span", class_="ipc-chip__text" )

        info["genre"] = [genre.text for genre in genres]

        info["description"] = main.find( "p", class_="sc-a31b0662-3 flXAL" ).text

        info["posterImgSrc"] = main.find( "div", class_="sc-4e4cc5f9-7 joCxEc" ).find("a")["href"]

        print(soup.find( "script", id="__NEXT_DATA__").prettify())

        elapsed_time = time.time() - start_time
        print( f"cas ids: {elapsed_time:.2f} seconds" )
        return info

    def getFilmInfo(self, id):
        soup = self.getSoup( self.urlFilm + id )
        start_time = time.time()
        info = {}

        print(id)

        vsechnoInfo = json.loads( soup.find( "script", id="__NEXT_DATA__").text )["props"]["pageProps"]["aboveTheFoldData"]

        try:
            info["imdbId"] = vsechnoInfo.get( "id" )
        except (KeyError, IndexError):
            info["imdbId"] = None

        try:
            info["title"] = vsechnoInfo["titleText"]["text"]
        except (KeyError, IndexError):
            info["title"] = None

        try:
            info["year"] = vsechnoInfo["releaseYear"]["year"]
        except (KeyError, IndexError):
            info["year"] = None

        try:
            info["runtime"] = vsechnoInfo["runtime"]["displayableProperty"]["value"]["plainText"]
        except (KeyError, IndexError):
            info["runtime"] = None

        try:
            info["rating"] = vsechnoInfo["ratingsSummary"]["aggregateRating"]
        except (KeyError, IndexError):
            info["rating"] = None

        try:
            info["genres"] = [genre["text"] for genre in vsechnoInfo["genres"]["genres"]]
        except (KeyError, IndexError):
            info["genres"] = None

        try:
            info["description"] = vsechnoInfo["primaryVideos"]["edges"][0]["node"]["description"]["value"]
        except (KeyError, IndexError):
            info["description"] = None

        try:
            info["plot"] = vsechnoInfo["plot"]["plotText"]["plainText"]
        except (KeyError, IndexError):
            info["plot"] = None

        try:
            info["trailerUrl"] = vsechnoInfo["primaryVideos"]["edges"][0]["node"]["playbackURLs"][0]["url"]
        except (KeyError, IndexError):
            info["trailerUrl"] = None

        try:
            director = vsechnoInfo["principalCredits"][0]["credits"][0]["name"]
            info["director"] = {'name': director['nameText']['text'], 'id': director['id']}
        except (KeyError, IndexError):
            info["director"] = None

        try:
            actors = vsechnoInfo["principalCredits"][2]["credits"]
            info["actors"] = [{'name': actor['name']['nameText']['text'], 'id': actor['name']['id']} for actor in
                              actors]
        except (KeyError, IndexError):
            info["actors"] = None

        try:
            info["posterUrl"] = vsechnoInfo["primaryImage"]["url"]
        except (KeyError, IndexError):
            info["posterUrl"] = None

        elapsed_time = time.time() - start_time
        print( f"cas filmInfo: {elapsed_time:.2f} seconds" )
        return info



    def getTop250Ids(self, limit):
        soup = self.getSoup(self.urlTop)

        start_time = time.time()

        main = soup.find( "main" )

        uls = main.find_all( "ul", attrs={"role": "presentation"} )

        IDs = []

        for ul in uls:
            lis = ul.find_all( "li" , limit=limit )
            for li in lis:
                ass = li.find_all( "a" )
                href = ass[0]["href"]
                IDs.append( href.split( "/" )[2] )

        elapsed_time = time.time() - start_time
        print( f"get ids: {elapsed_time:.2f} seconds" )

        return IDs

    def getSoup( self , url):
        start_time = time.time()

        # Send a GET request to the URL with headers
        response = requests.get( url, headers=self.headers )

        elapsed_time = time.time() - start_time

        soup = BeautifulSoup( response.content, 'html.parser' )

        print( f"cas getSoup: {elapsed_time:.2f} seconds" )

        return soup
