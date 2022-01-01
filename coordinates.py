"""Functions to get coordinates by name of the city."""


from pprint import pprint
from json import loads
from requests import get
from pprint import pprint


def convert_city_to_coordinates(city):
    """Return coordinates of the city by name."""
    url = generate_url(city)
    response = get(url)
    data = loads(response.text)

    try:
        info = data["hits"][0]
    except IndexError:
        print(f"Coordinates were not recieved! [{city}]")
        return False
    
    city = info["name"].lower()
    lat = info["point"]["lat"]
    lon = info["point"]["lng"]

    result = (city, lat, lon)
    print(f"Coordinates: {lat:.2f}  {lon:.2f} [{city}]")

    return result


def generate_url(city):
    """Builds the url."""
    api = "93428d03-daf7-4650-b591-d7da2ecaf1e9"
    url = "https://graphhopper.com/api/1/geocode?"
    url += "&locale=" + "en"
    url += "&q=" + city
    url += "&debug=" + "true"
    url += "&key=" + api
    
    
    return url
