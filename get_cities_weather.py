"""
Creates a database of weather forecast for the next 7 days for the names of cities.
"""


from json import loads
import sqlite3
from requests import get
from cities_coordinates import get_city_coordinates
from database import DataBase


def main():
    """Activates the entire program."""
    db = DataBase("weather_forecast.db")
    cities = ["kyiv", "lviv", "kharkiv", "CityThatNotExist", "new-york", "saratov"]
    cities_coordinates = get_city_coordinates(cities)
    db.announce_db()
    fill_db(db, cities_coordinates)


def fill_db(db, cities_coordinates):
    """Fills the entire table with data."""
    for city, lat, lon in cities_coordinates:
        url = build_url_for_weather(lat, lon)
        response = get(url)

        if response:
            print(f"({city = }) request is successful!")
        else:
            print(f"({city = }) request returned an error!")
            continue

        data = loads(response.text)

        for day in range(7):
            parameters = [city] + announce_parameters(data, day)
            db.insert_data(parameters)


def announce_parameters(all_data, current_day):
    """Init parameters that will be in table."""
    data = all_data["daily"][current_day]
    date = data["dt"]
    temp = data["temp"]["day"]
    pcp = data["pop"]
    clouds = data["clouds"]
    pressure = data["pressure"]
    humidity = data["humidity"]
    wind_speed = data["wind_speed"]

    parameters = [
            date, temp, pcp,
            clouds, pressure,humidity, wind_speed
            ]
    return parameters


def build_url_for_weather(lat, lon):
    """Build a url."""
    api = "8f6fe32c8781671c86b0e9941a7f061f"
    url = f"https://api.openweathermap.org/data/2.5/onecall?{lat=}&{lon=}"
    url += "&units=metric"
    url += "&exclude=current,minutely,hourly"
    url += f"&appid={api}"

    return url


if __name__ == "__main__":
    main()
