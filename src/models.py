from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    terrain = db.Column(db.Enum('desert', 'grasslands, mountains', 'jungle, rainforests', 'tundra, ice caves, mountain ranges', 'swamp, jungles', name="terrain_types"), nullable=False)
    climate = db.Column(db.Enum('arid', 'temperate', 'tropical', 'frozen', 'murky', name='climate_types'), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500))

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate,
            "population": self.population,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.Enum('female', 'male', 'other', 'n/a', name="gender_types"), nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.Enum('brown', 'blond', 'red', 'black', 'n/a', name="hair_color_types"), nullable=False)
    eye_color = db.Column(db.Enum('brown', 'green', 'blue', 'gold', 'n/a', name="eye_color_types"), nullable=False)
    image_url = db.Column(db.String(500))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    model = db.Column(db.String(100), nullable=False)
    vehicle_class = db.Column(db.Enum('repulsorcraft', 'wheeled', 'starfighter', name="vehicle_class_types"), nullable=False)
    manufacturer = db.Column(db.Enum('Incom Corporation', 'Corellia Mining Corporation', name="manufacturer_types"), nullable=False)
    length = db.Column(db.String(10), nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500))
    pilot_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship(Character)

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "passengers": self.passengers
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    user = db.relationship(User)
    character = db.relationship(Character)
    planet = db.relationship(Planet)
    vehicle = db.relationship(Vehicle)

    def __repr__(self):
        return '<Favorites %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }
