from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# an example mapping using the base
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    devices = db.relationship('Device', backref='devices', lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


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
