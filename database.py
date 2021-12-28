"""A."""


import sqlite3
import datetime


class DataBase:
    """Class for managing database tables."""
    def __init__(self, db_name):
        self.db_name = db_name


    def clear_db(self):
        """Delete all data from the database."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute("DELETE FROM weather_forecast;")
        self.conn.commit()
        self.conn.close()


    def make_db(self):
        "Announces the table."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE weather_forecast
        (city text,
        date integer,
        temp real,
        pcp real,
        clouds integer,
        pressure integer,
        humidity integer,
        wind_speed real)
        ;""")
        self.conn.commit()
        self.conn.close()


    def insert_data(self, parameters):
        """Insert data in table."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        sql = "INSERT INTO weather_forecast VALUES (?,?,?,?,?,?,?,?);"
        self.cursor.executemany(sql, [parameters])

        self.conn.commit()
        self.conn.close()


    def announce_db(self):
        """Checks if database already exist."""
        try:
            self.make_db()
        except sqlite3.OperationalError:
            self.clear_db()


    def connection(self, function):
        """Stupid attemp to create decorator."""
        def wrapper():
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.function()
            self.conn.close()
        return wrapper()


    def get_unic_cities(self):
        """Returns list with unic cities."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        cities_list = []
        cities = self.cursor.execute("SELECT DISTINCT city FROM weather_forecast;")
        for city in cities:
            cities_list += city
        self.conn.close()
        return cities_list


    def get_all(self):
        """Returns all table data."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM weather_forecast;")
        result = self.cursor.fetchall()
        self.conn.close()
        return result


    def get_mean(self, args):
        """
        Returns the average of the
        selected value for the selected city.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        avg = 0

        sql = f"SELECT city, {args['value_type']} FROM weather_forecast;"
        for city, value in self.cursor.execute(sql):
            if city == args['city']:
                try:
                    avg += float(value)
                except TypeError:
                    return {"ERROR": "Enter another value_type!"}

        args["value_type"] = avg / 7
        self.conn.close()
        return args


    def slice_data(self, args):
        """Returns a piece of data truncated by date."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        sliced = {}
        slice_started = False
        for data in self.cursor.execute("SELECT * FROM weather_forecast;"):
            date = datetime.datetime.fromtimestamp(int(data[1])).strftime("%d.%m.%Y")
            if args["start_dt"] == date:
                slice_started = True

            if args["city"] == data[0] and slice_started:
                sliced[args["city"] + " " + date] = data[2:]

            if date == args["end_dt"]:
                self.conn.close()
                return sliced


    def get_moving_mean(self, args):
        """
        Returns the moving average of the
        selected value for the selected city.
        """
        self.conn =  sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        moving_mean = 0

        sql = f"SELECT city, {args['value_type']} FROM weather_forecast;"
        for city, value in self.cursor.execute(sql):
            if city == args['city']:
                try:
                    moving_mean += float(value)
                except:
                    return {"ERROR": "Enter another value_type!"}
        self.conn.close()
        return {args['value_type']: moving_mean / 7}
