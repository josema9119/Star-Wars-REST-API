"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Character, Planet, Vehicle
#from models import Perso

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['POST'])
def create_user():
    body_name = request.json.get("name")
    body_username = request.json.get("username")
    body_email = request.json.get("email")
    body_password = request.json.get("password") 
    user = User(name = body_name, username = body_username, email = body_email, password = body_password)
    db.session.add(user) 
    db.session.commit()
    return jsonify({"name": user.name, "msg": "Creado el usuario con id:" + str(user.id)}), 200

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_serialized = list(map(lambda x: x.serialize(), users))
    return jsonify({"response": users_serialized}), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.get(user_id)
    return jsonify({"response": user.serialize()}), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_one_user(user_id):
    user = User.query.get( user_id)
    db.session.delete(user)
    db.session.commit
    return jsonify ({"deleted":True}), 200


@app.route('/character', methods=['POST'])
def create_character():
    body_name= request.json.get("name")
    body_gender= request.json.get("gender")
    body_age= request.json.get("age")
    db.session.add(character)
    db.session.commit()
    character= Character({"name": character.name, "msg": "Creado el nuevo planet con id" + str(character.id)}), 200

@app.route('/character', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    characters_serialized = list(map(lambda x: x.serialize(), characters))
    return jsonify({"response": characters_serialized}), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    character = Character.query.get(character_id)
    return jsonify({"response": character}), 200

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_one_character(character_id):
    character = Character.query.delete(id = character_id)
    db.session.delete(character)
    db.session.commit()
    return jsonify ({"deleted":True}), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    body_name = request.json.get("name")
    body_population = request.json.get("population")
    body_terrain = request.json.get("terrain")
    body_diameter = request.json.get("diameter")
    planet = Planet(name= body_name, population= body_population, terrain= body_terrain, diameter= body_diameter)
    db.session.add(planet)
    db.session.commit()
    return jsonify({"name": planet.name, "msg": "Creado el nuevo planet con id" + str(planet.id)}), 200

@app.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify({"response": planets_serialized}), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet():
    planet = Planet.query.get(planet_id)
    return jsonify({"response": planet}), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_one_planet(planet_id):
    planet = Planet.query.delete(id = planet_id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify ({"deleted":True}), 200

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    body_model= request.json.get("model")
    body_cost_credits= request.json.get("cost_credits")
    body_cargo_capacity= request.json.get("cargo_capacity")
    body_passengers= request.json.get("passengers")
    vehicle= Vehicle(model=body_model, cost_credits= body_cost_credits, cargo_capacity= body_cargo_capacity, passengers= body_passengers)
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({"model": vehicle.model, "msg": "Creado el nuevo vehicle con id" + str(vehicle.id)}), 200

@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicle.query.all()
    vehicles_serialized = list(map(lambda x: x.serialize(), vehicles))
    return jsonify({"response": vehicles_serialized}), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle():
    vehicle = Vehicle.query.get(vehicle_id)
    return jsonify({"response": vehicle}), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_one_vehicle(vehicle_id):
    vehicle = Vechicle.query.delete(id = vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify ({"deleted":True}), 200

@app.route('/favorites/<int:favorites_id>', methods=['DELETE'])
def delete_one_favorites(favorites_id):
    favorites = Favorites.query.get(favorites_id)
    db.session.delete(favorites)
    db.session.commit()
    return jsonify({"deleted": True}), 200

@app.route('/user/<int:user_id>/favorites', methods= ['GET'])
def get_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id = user_id).first()
    return jsonify({'favorites': favorites.serialize()}), 200

@app.route('/user/<int:user_id>/favorites/character/<int:character_id>', methods=['POST'])
def post_one_favourite_character(user_id, character_id):
    favorites = Favorites(user_id = user_id, character_id = character_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify(({'favorites': favorites.serialize()})), 200

@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>/', methods=['POST'])
def post_one_favourite_planet(user_id, planet_id):
    favorites = Favorites(user_id = user_id, planet_id = planet_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify(({'favorites': favorites.serialize()})), 200

@app.route('/user/<int:user_id>/favorites/vehicle/<int:vehicle_id>/', methods=['POST'])
def post_one_favourite_vehicle(user_id, vehicle_id):
    favorites = Favorites(user_id = user_id, vehicle_id = vehicle_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify(({'favorites': favorites.serialize()})), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
