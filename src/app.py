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
from models import db, User, Planet, Character, Vehicle, Favorites


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]

    return jsonify(serialized_characters), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)

    if character is None:
        return jsonify(), 404
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]

    return jsonify(serialized_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    
    if planet is None:
        return jsonify(), 404
    return jsonify(planet.serialize()), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    serialized_vehicles = [vehicle.serialize() for vehicle in vehicles]

    return jsonify(serialized_vehicles), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    
    if vehicle is None:
        return jsonify(), 404
    return jsonify(vehicle.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
