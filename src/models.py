from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(220), nullable=False, unique=True)
    password = db.Column(db.String(250))  
    def __repr__(self):
        return "user: " + self.username
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    
    def serialize(self):
        return {
            "id ": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        } 

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "name":self.name,
            "population": self.population,
            "terrain": self.terrain,
            "diameter": self.diameter
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(250), nullable=False)
    cost_credits = db.Column(db.String(250), nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "model":self.model,
            "cost_credits": self.cost_credits,
            "cargo_capacity": self.cargo_capacity,
            "passengers": self.passengers
        }
    
