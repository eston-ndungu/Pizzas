#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


class Home(Resource):

    def get(self):
        response_dict = {
            "message": "Code challenge"
        }
        response = make_response(
            response_dict,
            200
        )
        return response
api.add_resource(Home, '/')

class Restaurants(Resource):

    def get(self):
        # Create a new list of dictionaries containing id, name , and address excluding the information of restaurant_pizzas from response
        
        response_dict_list = [
            {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address

            }
            for restaurant in Restaurant.query.all()
        ]

        response = make_response(
            response_dict_list,
            200,
        )
        return response
    
api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):

    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant is None:
            response_dict ={
                "error": "Restaurant not found" 
            }
            response = make_response(
                response_dict,
                404,
            )
            return response
        
        
api.add_resource(RestaurantByID, '/restaurants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
