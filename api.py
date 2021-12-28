from flask import Flask
from flask_restful import Resource, Api, reqparse
from database import DataBase

app = Flask(__name__)
api = Api(app)
db = DataBase("weather_forecast.db")


class AllData(Resource):
    def get(self):
        return db.get_all()


class Cities(Resource):
    def get(self):
        return db.get_unic_cities()


class Params(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("value_type", required=True)
        parser.add_argument("city", required=True)
        args = parser.parse_args()
        return db.get_mean(args)

class Records(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("city", required=True)
        parser.add_argument("start_dt", required=True)
        parser.add_argument("end_dt", required=True)
        args = parser.parse_args()
        return db.slice_data(args)

class MovingMean(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("city", required=True)
        parser.add_argument("value_type", required=True)
        args = parser.parse_args()
        return db.get_moving_mean(args)


api.add_resource(AllData, "/")
api.add_resource(Cities, "/cities")
api.add_resource(Params, "/mean")
api.add_resource(Records, "/records")
api.add_resource(MovingMean, "/moving_mean")

app.run(debug=True)
