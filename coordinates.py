"""Functions to get coordinates by name of the city."""


from json import loads
from requests import get


def get_city_coordinates(cities):
    """Returns coordinates of the city."""
    cities_coordinates = []

    for city in cities:
        result = convert_city_to_coordinates(city)

        if not result:
            continue

        cities_coordinates.append(result)

    return cities_coordinates


def convert_city_to_coordinates(city):
    url = generate_url(city)
    response = get(url)
    data = loads(response.text)

    try:
        point = data["hits"][0]["point"]
    except IndexError:
        print(f"({city = }) Coordinates were not recieved!")
        return False

    lat = point["lat"]
    lon = point["lng"]

    result = (city, lat, lon)
    print(f"({city = }) Coordinates: {lat:.2f}  {lon:.2f}")

    return result



def generate_url(city):
    """Builds the url."""
    api = "93428d03-daf7-4650-b591-d7da2ecaf1e9"
    url = "https://graphhopper.com/api/1/geocode?"
    url += "q=" + city
    url += "&debug=" + "true"
    url += "&key=" + api

    return url
