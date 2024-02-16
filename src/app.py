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

# USERS ENDPOINTS
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]

    if users is None:
        return jsonify({'error':'No users found'}), 404
    else:
        return jsonify(serialized_users), 200


# FAVORITES ENDPOINTS
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error':'User not found'}), 404
    
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    serialized_favorites = [favorite.serialize() for favorite in favorites]

    if favorites is None:
        return jsonify({'error':'Favorites not found for this user'}), 404
    else:
        return jsonify(serialized_favorites), 200

@app.route('/favorites/user/<int:user_id>', methods=['POST'])
def add_favorite(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error':'User not found'}), 404
    
    body = request.get_json()
    favorites = Favorites()
    favorites.user_id = user_id
    if 'character_id' in body:
        favorites.character_id = body['character_id']
    if 'planet_id' in body:    
        favorites.planet_id = body['planet_id']
    if 'vehicle_id' in body:
        favorites.vehicle_id = body['vehicle_id']

    db.session.add(favorites)
    db.session.commit()

    return jsonify({'msg':'Favorites have been updated successfully'}), 200

@app.route('/favorites/users/<int:user_id>/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error':'User not found'}), 404

    favorite_entry = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    
    if favorite_entry:
        db.session.delete(favorite_entry)
        db.session.commit()
        return jsonify({'msg':'Favorite planet deleted successfully'}), 200
    else:
        return jsonify({'error':'Favorite planet not found'}), 404
    
@app.route('/favorites/users/<int:user_id>/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error':'User not found'}), 404
    
    favorite_entry = Favorites.query.filter_by(user_id=user_id, character_id=character_id).first()
    
    if favorite_entry:
        db.session.delete(favorite_entry)
        db.session.commit()
        return jsonify({'msg':'Favorite character deleted successfully'}), 200
    else:
        return jsonify({'error':'Favorite character not found'}), 404

@app.route('/favorites/users/<int:user_id>/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(user_id, vehicle_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error':'User not found'}), 404
    
    favorite_entry = Favorites.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
    
    if favorite_entry:
        db.session.delete(favorite_entry)
        db.session.commit()
        return jsonify({'msg':'Favorite vehicle deleted successfully'}), 200
    else:
        return jsonify({'error':'Favorite vehicle not found'}), 404


# CHARACTERS ENDPOINTS
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]

    if characters is None:
        return jsonify({'error':'No characters found'}), 404
    else:
        return jsonify(serialized_characters), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)

    if character is None:
        return jsonify({'error': 'Character not found'}), 404
    else:
        return jsonify(character.serialize()), 200

@app.route('/characters', methods=['POST'])
def add_character():
    body = request.get_json()
    character = Character()
    character.id = body['id']
    character.name = body['name']
    character.gender = body['gender']
    character.birth_year = body['birth_year']
    character.height = body['height']
    character.hair_color = body['hair_color']
    character.eye_color = body['eye_color']
    character.planet_id = body['planet_id']

    if 'image_url' in body:
        character.image_url = body['image_url']

    db.session.add(character)
    db.session.commit()

    return jsonify("Character created successfully", character.serialize()), 200

@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    body = request.get_json()
    character = Character.query.filter_by(id=character_id).first()

    if character:
       character.name = body['name']
       character.gender = body['gender']
       character.birth_year = body['birth_year']
       character.height = body['height']
       character.hair_color = body['hair_color']
       character.eye_color = body['eye_color']
       character.planet_id = body['planet_id']

    if 'image_url' in body:
        character.image_url = body['image_url']

    db.session.commit()

    return jsonify("Character has been updated successfully", character.serialize()), 200

@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.filter_by(id=character_id).first()
    
    if character:
        db.session.delete(character)
        db.session.commit()
        return jsonify("Character deleted successfully"), 200
    else:
        return jsonify("Character not found"), 404


# PLANETS ENDPOINTS
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]

    if planets is None:
        return jsonify({'error':'No planets found'}), 404
    else:
        return jsonify(serialized_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    
    if planet is None:
        return jsonify({'error':'Planet not found'}), 404
    else:
        return jsonify(planet.serialize()), 200
    
@app.route('/planets', methods=['POST'])
def add_planet():
    body = request.get_json()
    planet = Planet()
    planet.id = body['id']
    planet.name = body['name']
    planet.terrain = body['terrain']
    planet.climate = body['climate']
    planet.population = body['population']
    planet.orbital_period = body['orbital_period']
    planet.rotation_period = body['rotation_period']
    planet.diameter = body['diameter']

    if 'image_url' in body:
        planet.image_url = body['image_url']

    db.session.add(planet)
    db.session.commit()

    return jsonify("Planet created successfully", planet.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    body = request.get_json()
    planet = Planet.query.filter_by(id=planet_id).first()

    if planet:
       planet.name = body['name']
       planet.terrain = body['terrain']
       planet.climate = body['climate']
       planet.population = body['population']
       planet.orbital_period = body['orbital_period']
       planet.rotation_period = body['rotation_period']
       planet.diameter = body['diameter']

    if 'image_url' in body:
        planet.image_url = body['image_url']

    db.session.commit()

    return jsonify("Planet has been updated successfully", planet.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify("Planet deleted successfully"), 200
    else:
        return jsonify("Planet not found"), 404


# VEHICLES ENDPOINTS
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    serialized_vehicles = [vehicle.serialize() for vehicle in vehicles]

    if vehicles is None:
        return jsonify({'error':'No vehicles found'}), 404
    else:
        return jsonify(serialized_vehicles), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    
    if vehicle is None:
        return jsonify({'error':'Vehicle not found'}), 404
    else:
        return jsonify(vehicle.serialize()), 200

@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    body = request.get_json()
    vehicle = Vehicle()
    vehicle.id = body['id']
    vehicle.name = body['name']
    vehicle.model = body['model']
    vehicle.model = body['model']
    vehicle.vehicle_class = body['vehicle_class']
    vehicle.manufacturer = body['manufacturer']
    vehicle.length = body['length']
    vehicle.passengers = body['passengers']

    if 'image_url' in body:
        vehicle.image_url = body['image_url']
    if 'pilot_id' in body:
        vehicle.pilot_id = body['pilot_id']

    db.session.add(vehicle)
    db.session.commit()

    return jsonify("Vehicle created successfully", vehicle.serialize()), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    body = request.get_json()
    vehicle = Vehicle.query.filter_by(id=vehicle_id).first()

    if vehicle:
       vehicle.id = body['id']
       vehicle.name = body['name']
       vehicle.model = body['model']
       vehicle.model = body['model']
       vehicle.vehicle_class = body['vehicle_class']
       vehicle.manufacturer = body['manufacturer']
       vehicle.length = body['length']
       vehicle.passengers = body['passengers']

    if 'image_url' in body:
        vehicle.image_url = body['image_url']
    if 'pilot_id' in body:
        vehicle.pilot_id = body['pilot_id']

    db.session.commit()

    return jsonify("Vehicle has been updated successfully", vehicle.serialize()), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
    
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify("Vehicle deleted successfully"), 200
    else:
        return jsonify("Vehicle not found"), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
