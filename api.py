"""API requests."""


from flask import Flask
from flask_restful import Resource, Api, reqparse
from database import DataBase

app = Flask(__name__)
api = Api(app)

db = DataBase()


class AllData(Resource):
    """Show all database data."""
    def get(self):
        return db.get_all_data()


class Cities(Resource):
    """Show all cities in database."""
    def get(self):
        return db.get_unic_cities()


class Mean(Resource):
    """Show weekly mean of chosen value in  chosen city."""
    def get(self):
        args = parse_args(("city", "value_type"), is_required=True)
        return db.get_mean(args)


class Records(Resource):
    """Show city's data in chosen period of time."""
    def get(self):
        args = parse_args(("city", "start_dt", "end_dt"), is_required=True)
        return db.slice_data(args)


class MovingMean(Resource):
    """Show weekly moving mean of chosen value in chosen city."""
    def get(self):
        args = parse_args(("city", "value_type"), is_required=True)
        return db.get_moving_mean(args)


def parse_args(
        args: tuple=tuple(),
        is_required: bool=False
        ):
    """Parse arguments."""
    parser = reqparse.RequestParser()
    for argument in args:
        parser.add_argument(argument, required=is_required)

    data = parser.parse_args()
    return data


api.add_resource(AllData, "/")
api.add_resource(Cities, "/cities")
api.add_resource(Mean, "/mean")
api.add_resource(Records, "/records")
api.add_resource(MovingMean, "/moving_mean")

if __name__ == "__main__":
    app.run(debug=True)
