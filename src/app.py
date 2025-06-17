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
from models import db, User, FavoriteCharacters, FavoritePlanets, FavoriteVehicles, Character, Vehicle, Planet
#from models import Person

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

@app.route('/character', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    characters_list = []
    for character in characters:
        characters_list.append(
            character.serialize()
        )
    return jsonify(characters_list), 200 
# def get_characters():
#     people = Character.query.all()
#     people_list = []
#     for person in people: 
#         people_list.append(
#             person.serialize()
#         )
#     return jsonify(people_list), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error":"Person not found"}), 404
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets_list = []
    for planet in planets:
        planets_list.append(
            planet.serialize()
        )
    return jsonify(planets_list), 200 

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error":"Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    vehicles_list = []
    for vehicle in vehicles:
        vehicles_list.append(
            vehicle.serialize()
        )
    return jsonify(vehicles_list), 200 

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"error":"Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
  users = User.query.all()
  users_list = []
  for user in users:
      users_list.append(
          user.serialize()
      )
  return jsonify(users_list), 200 

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "No user found"})
    return jsonify(user.serialize_favorites()), 200

@app.route('/favorite/character/<int:character_id>', methods =['POST'])
def add_favorite_character(character_id):
    user_id = request.json.get('user_id')
    character = Character.query.get(character_id)
    favorite = FavoriteCharacters(user_id = user_id, character_id = character_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods =['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    planet = Planet.query.get(planet_id)
    favorite = FavoritePlanets(user_id = user_id, planet_id = planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/vehicle/<int:vehicle_id>', methods =['POST'])
def add_favorite_vehicle(vehicle_id):
    user_id = request.json.get('user_id')
    vehicle = Vehicle.query.get(vehicle_id)
    favorite = FavoriteVehicles(user_id = user_id, vehicle_id = vehicle_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    user_id = request.json.get('user_id')
    character = Character.query.get(character_id)
    favorite = FavoriteCharacters.query.filter_by(user_id = user_id, character_id = character_id).first()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"MSG": "Favorite deleted"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    planet = Planet.query.get(planet_id)
    favorite = FavoritePlanets.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"MSG": "Favorite deleted"}), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    user_id = request.json.get('user_id')
    vehicle = Vehicle.query.get(vehicle_id)
    favorite = FavoriteVehicles.query.filter_by(user_id = user_id, vehicle_id = vehicle_id).first()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"MSG": "Favorite deleted"}), 200
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
