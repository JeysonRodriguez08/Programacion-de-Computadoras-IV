import requests

# Definimos las URLs base de la API
BASE_URL = "https://swapi.dev/api/"
PLANETS_URL = BASE_URL + "planets/"
PEOPLE_URL = BASE_URL + "people/"
STARSHIPS_URL = BASE_URL + "starships/"

# Definimos la función para hacer solicitudes GET a la API
def make_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# a) ¿En cuántas películas aparecen planetas cuyo clima sea árido?
def count_arid_planets_films():
    planets_response = make_request(PLANETS_URL)
    if planets_response is not None:
        arid_planets = [planet for planet in planets_response["results"] if "arid" in planet["climate"]]
        # Imprimimos el número de películas en las que aparecen estos planetas
        films = set()
        for planet in arid_planets:
            for film_url in planet["films"]:
                film = make_request(film_url)
                if film is not None:
                    films.add(film["title"])
        print(f"Hay {len(films)} películas en las que aparecen planetas con clima árido.")

# b) ¿Cuántos Wookies aparecen en toda la saga?
def count_wookies():
    people_response = make_request(PEOPLE_URL)
    if people_response is not None:
        wookies = [person for person in people_response["results"] if "wookiee" in person["species"]]
        print(f"Hay {len(wookies)} Wookies en toda la saga.")

# c) ¿Cuál es el nombre de la aeronave más pequeña en la primera película?
def smallest_starship_first_movie():
    starships_response = make_request(STARSHIPS_URL)
    if starships_response is not None:
        # Filtramos las naves espaciales por aquellas que aparecen en la primera película
        starships_first_movie = [starship for starship in starships_response["results"] if "1" in starship["films"][0]]
        # Encontramos la nave espacial más pequeña
        smallest_starship = min(starships_first_movie, key=lambda x: float(x["length"].replace(",", "")))
        print(f"La aeronave más pequeña en la primera película se llama {smallest_starship['name']} y mide {smallest_starship['length']} metros de largo.")

# Llamamos a las funciones para obtener las respuestas
count_arid_planets_films()
count_wookies()
smallest_starship_first_movie()
