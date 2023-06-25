#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        return plants

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help="Name is required")
        parser.add_argument("image", type=str, required=True, help="Image URL is required")
        parser.add_argument("price", type=float, required=True, help="Price is required")
        args = parser.parse_args()

        new_plant = {
            "id": len(plants) + 1,
            "name": args["name"],
            "image": args["image"],
            "price": args["price"]
        }

        plants.append(new_plant)
        return new_plant, 201

class PlantByID(Resource):
    def get(self, plant_id):
        plant = next((p for p in plants if p["id"] == plant_id), None)
        if plant:
            return plant
        else:
            return {"message": "Plant not found"}, 404

api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:plant_id>")
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
