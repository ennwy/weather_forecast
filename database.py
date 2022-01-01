"""Dockstring might be here."""

import sqlite3
from secondary_functions import 


class DataBase:
    """Class for managing database tables."""
    def __init__(self, db_name="weather_db.db"):
        self.db_name = db_name

    def execute(
            self,
            sql,
            data: tuple=tuple(),
            commit: bool=False,
            fetchall=False,
            fetchmany=0,
            fetchone=False
            ):
        """Useful execute."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(sql, data)
        parameters = self.get_fetched_data(cursor,
                                     fetchall,
                                     fetchmany,
                                     fetchone
                                     )
        if commit:
            conn.commit()

        return parameters


    def get_fetched_data(
            self,
            cursor,
            fetchall,
            fetchmany,
            fetchone
            ):
        """Checks execute function for fetch argument."""
        data = ()

        if fetchall:
            data = cursor.fetchall()
        elif fetchmany >= 1:
            data = cursor.fetchmany(fetchmany)
        elif fetchone:
            data = cursor.fetchone()

        return data


    def clear_db(self):
        """Delete all data from the database."""
        sql = """
        DELETE FROM 
        weather_forecast;
        """
        self.execute(sql, commit=True)


    def create_db(self):
        "Announces the table."""
        sql = """
        CREATE TABLE weather_forecast (
                    city text,
                    date integer,
                    temp real,
                    pcp real,
                    clouds integer,
                    pressure integer,
                    humidity integer,
                    wind_speed real
                    );
        """
        self.execute(sql, commit=True)


    def insert(self, parameters):
        """Insert data in table."""
        sql = """
        INSERT INTO
            weather_forecast
        VALUES
            (?,?,?,?,?,?,?,?);
        """
        self.execute(sql, parameters, commit=True)


    def init_db(self):
        """Checks if database already exist."""
        try:
            self.create_db()
        except sqlite3.OperationalError:
            self.clear_db()


    def get_unic_cities(self):
        """Returns list with unic cities."""
        sql = """
        SELECT DISTINCT
            city
        FROM
            weather_forecast;
        """
        cities = self.execute(sql, fetchall=True)
        cities = unpack_list_with_lists(cities)
        return cities

    def get_all_data(self):
        """Returns all table data."""
        sql = """
        SELECT * FROM
        weather_forecast;
        """
        data = self.execute(sql, fetchall=True)
        data = parse_data_from_list(data)
        return data


    def get_mean(self, args):
        """
        Returns the average of the
        selected value for the selected city.
        """
        city, value_type = args["city"], args["value_type"]
        validiti = is_data_valid(value_type)

        if not validity:
            return "Invalid parameter 'value_type'"

        sql = f"""
        SELECT
            {value_type}  
        FROM
            weather_forecast
        WHERE
            city=?;
        """

        data = self.execute(sql, [city], fetchall=True)

        values = unpack_list_with_lists(data)
        args["value_type"] = sum(values) / len(values)
        return args


    def slice_data(self, args):
        """Returns a piece of data truncated by date."""
        sql = """
        SELECT * FROM
            weather_forecast
        WHERE
            ? < date
        AND
            date < ?
        AND
            city = ?;
        """
        city = args["city"].lower()
        start, end = args["start_dt"].lower(), args["end_dt"].lower()
        start, end = parse_date_to_timestamp((start, end))

        data = self.execute(sql, [start, end, city], fetchall=True)
        data = parse_data_from_list(data)
        return data


    def get_moving_mean(self, args):
        """
        Returns the moving average of the
        selected value for the selected city.
        """
        city, value_type = args["city"], args["value_type"]

        sql = f"""
        SELECT
            {value_type}
        FROM
            weather_forecast
        WHERE
            city=?;
        """
        data = self.execute(sql, [city], fetchall=True)
        values = unpack_list_with_lists(data)
        return sum(values) / len(values)
