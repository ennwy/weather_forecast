"""
Creates a database of weather forecast for the next 7 days for the names of cities.
"""

from json import loads
import sqlite3
from requests import get
from coordinates import *
from database import DataBase


cities = ["surgut", "tula", "znamyanka", "Ukraine, pokrov, Dnipropetrovsk Oblast"]
api = "8f6fe32c8781671c86b0e9941a7f061f"


def main(cities):
    """Fills the entire table with data."""
    db = DataBase()
    db.init_db()

    cities_coordinates = get_cities_coordinates(cities)

    for name, lat, lon in cities_coordinates:
        
        url = build_city_url(lat, lon)
        response = get_response(url, name)

        if not response:
            continue

        data = loads(response.text)
        insert_data(db, data, name)


def insert_data(db, data, name):
    
    for day in data["daily"]:
        day["name"] = name
        parameters = parse_parameters(day)
        db.insert(parameters)


def get_response(url, name):
    response = get(url)

    if response:
        print(f"Request is successful! [{name}]")
    else:
        print(f"Request is not successful! [{name}]")
        response = False

    return response

    
def parse_parameters(day):
    """Init parameters that will be in table."""
    city_name = day["name"]
    date = day["dt"]
    temp = day["temp"]["day"]
    pcp = get_pcp(day)
    clouds = day["clouds"]
    pressure = day["pressure"]
    humidity = day["humidity"]
    wind_speed = day["wind_speed"]

    parameters = (
                city_name,
                date,
                temp,
                pcp,
                clouds,
                pressure,
                humidity,
                wind_speed
                )
    return parameters


def get_pcp(day):
    pcp = 0
    if "rain" in day:
        pcp += day["rain"]
    if "snow" in day:
        pcp += day["snow"]

    return pcp
    


def get_cities_coordinates(cities):
    """Returns coordinates of the cities."""
    cities_coordinates = []

    for city in cities:
        url = generate_url(city)
        result = convert_city_to_coordinates(city)

        if not result:
            continue

        cities_coordinates.append(result)

    return cities_coordinates


def build_city_url(lat, lon):
    """Build a url."""
    url = f"https://api.openweathermap.org/data/2.5/onecall"
    url += f"?{lat=}&{lon=}"
    url += "&units=metric"
    url += "&exclude=current,minutely,hourly"
    url += f"&appid={api}"

    return url


if __name__ == "__main__":
    main(cities)
