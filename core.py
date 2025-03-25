from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from config import *
import hashlib
import datetime

# Initialize Flask app, SQLAlchemy, and JWT manager
app = Flask(__name__)

# Configure SQLAlchemy to use SQLite (this will create a local SQLite file)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI  # Change to SQLite URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Secret key to encode the JWT

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# User Model (SQLAlchemy ORM)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Workout Model (SQLAlchemy ORM)
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('workouts', lazy=True))

    def __repr__(self):
        return f"<Workout {self.name}>"

# Utility function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()