from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    favorite_characters: Mapped[list["FavoriteCharacters"]] = relationship(
        "FavoriteCharacters", back_populates="user")
    favorite_planets: Mapped[list["FavoritePlanets"]] = relationship(
        "FavoritePlanets", back_populates="user")
    favorite_vehicles: Mapped[list["FavoriteVehicles"]] = relationship(
        "FavoriteVehicles", back_populates="user")

    def serialize(self):
        characters = [character.serialize()
                      for character in self.favorite_characters]
        planets = [planet.serialize() for planet in self.favorite_planets]
        vehicles = [vehicle.serialize() for vehicle in self.favorite_vehicles]
        return {
            "id": self.id,
            "email": self.email,
            "favorites": {"characters": characters,
                          "planets": planets,
                          "vehicles": vehicles}
            # do not serialize the password, its a security breach
        }
    def serialize_favorites(self):
        characters = [character.serialize()
                      for character in self.favorite_characters]
        planets = [planet.serialize() for planet in self.favorite_planets]
        vehicles = [vehicle.serialize() for vehicle in self.favorite_vehicles]
        return {
            "favorites": {"characters": characters,
                          "planets": planets,
                          "vehicles": vehicles}
        }


class FavoriteCharacters(db.Model):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    user: Mapped["User"] = relationship(
        "User", back_populates="favorite_characters")
    character: Mapped["Character"] = relationship(backref="character")
    __table_args__ = (db.UniqueConstraint(
        "user_id", "character_id", name="no_duplicate_for_user_and_character"),)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id
        }


class FavoritePlanets(db.Model):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    user: Mapped["User"] = relationship(
        "User", back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship(backref="planet")
    __table_args__ = (db.UniqueConstraint(
        "user_id", "planet_id", name="no_duplicate_for_user_and_planet"),)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }


class FavoriteVehicles(db.Model):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"))
    user: Mapped["User"] = relationship(
        "User", back_populates="favorite_vehicles")
    vehicle: Mapped["Vehicle"] = relationship(backref="vehicle")
    __table_args__ = (db.UniqueConstraint(
        "user_id", "vehicle_id", name="no_duplicate_for_user_and_vehicle"),)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120))
    image_url: Mapped[str] = mapped_column(String(120))
    biography: Mapped[str] = mapped_column(String(300))
    birthday: Mapped[int] = mapped_column()
    gender: Mapped[str] = mapped_column(String(7))
    favorite_character: Mapped[list["FavoriteCharacters"]] = relationship(
        backref="favorite_character")

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "image_url": self.image_url,
            "biography": self.biography,
            "birthday": self.birthday,
            "gender": self.gender,
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    image_url: Mapped[str] = mapped_column(String(120))
    history: Mapped[str] = mapped_column(String(300))
    population: Mapped[int] = mapped_column()
    terrain: Mapped[str] = mapped_column(String(50))
    inhabitants: Mapped[str] = mapped_column(String(80))
    language: Mapped[str] = mapped_column(String(50))
    favorite_planet: Mapped[list["FavoritePlanets"]
                            ] = relationship(backref="favorite_planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
            "history": self.history,
            "terrain": self.terrain,
            "inhabitants": self.inhabitants,
            "language": self.language
        }


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50))
    passengers: Mapped[int] = mapped_column()
    favorite_vehicle: Mapped[list["FavoriteVehicles"]
                             ] = relationship(backref="favorite_vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "passengers": self.passengers,
        }
