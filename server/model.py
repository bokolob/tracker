from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ..app import app.db
import os

app = Flask(__name__)
# mysql://username:password@server/db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI');
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# an example mapping using the base
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    devices = db.relationship('Device', backref='devices', lazy=True)


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    imei = db.Column(db.String(16), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user = db.relationship("User", back_populates="devices", lazy=True)
    coordinates = db.relationship("Coordinates", back_populates="device", lazy=True)


class Coordinates(db.Model):
    __tablename__ = 'coordinates'
    id = db.Column(db.BigInteger, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    device = db.relationship("Device", back_populates="coordinates")
    lat = db.Column(db.Numeric)
    lng = db.Column(db.Numeric)
