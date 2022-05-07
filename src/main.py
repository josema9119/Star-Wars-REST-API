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
from models import db, User
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
    body_name = request.json.post("name")
    body_username = request.json.post("username")
    body_email = request.json.post("email")
    body_password = request.json.post("password") 
    user = User(name = body_name, username = body_username, email = body_email, password = body_password)
    db.session.add(user) 
    db.session.commit()
    return jsonify({"name": user.name, "msg": "Creado el usuario con id:" + str(user.id)}), 200

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_serialized = list(map(lambda x: x.serialize(), users))
    return jsonify({"response": users_serialized}), 200

@app.route('/character', methods=['POST'])
def create_character():
    body_name= request.json.post("name")
    body_gender= request.json.post("gender")
    body_age= request.json.post("age")
    db.session.add(character)
    db.session.commit()
    character= Character({"name": character.name, "msg": "Creado el nuevo planet con id" + str(character.id)}), 200

@app.route('/character', methods=['GET'])
def get_all_characters():
    characters = character.query.all()
    characters_serialized = list(map(lambda x: x.serialize(), characters))
    return jsonify({"response": characters_serialized}), 200
    
@app.route('/planet', methods=['POST'])
def create_planet():
    body_name = request.json.post("name")
    body_population = request.json.post("population")
    body_terrain = request.json.post("terrain")
    body_diameter = request.json.post("diameter")
    planet = Planet(name= body_name, population= body_population, terrain= body_terrain, diameter= body_diameter)
    db.session.add(planet)
    db.sessin.commit()
    return jsonify({"name": planet.name, "msg": "Creado el nuevo planet con id" + str(planet.id)}), 200

@app.route('/planet', methods=['GET'])
def get_all_planets():
    planets = planet.query.all()
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify({"response": planets_serialized}), 200

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    body_model= request.json.post("model")
    body_cost_credits= request.json("cost_credits")
    body_cargo_capacity= request.json("cargo_capacity")
    body_passengers= request.json("passengers")
    vehicle= Vehicle(model=body_model, cost_credits= body_cost_credits, cargo_capacity= body_cargo_capacity, passengers= body_passengers)
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({"model": vehicle.model, "msg": "Creado el nuevo vehicle con id" + str(vehicle.id)}), 200

@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    vehicles = vehicle.query.all()
    vehicles_serialized = list(map(lambda x: x.serialize(), vehicles))
    return jsonify({"response": vehicles_serialized}), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
