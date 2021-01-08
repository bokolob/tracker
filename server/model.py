from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
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


class SharedDevices(db.Model):
    __tablename__ = 'shared_devices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    shared_with = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    device = db.relationship("Device", lazy="joined", uselist=False, back_populates="share")
    user = db.relationship("User", uselist=False, lazy=True)

    __table_args__ = (Index('User_device', 'shared_with', 'device_id', unique=True),)


class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plans'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)


class SubscriptionOptions(db.Model):
    __tablename__ = 'subscription_option'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    imei = db.Column(db.String(16), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_shareable = db.Column(db.Boolean, nullable=False, default=False)
    settings = db.relationship("DeviceSettings", lazy="joined")
    user = db.relationship("User", back_populates="devices", uselist=False, lazy="joined")
    share = db.relationship("SharedDevices", back_populates="device", lazy="joined")
    # coordinates = db.relationship("Coordinates", back_populates="device", lazy=True)


class Coordinates(db.Model):
    __tablename__ = 'coordinates'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    device = db.relationship("Device")
    lat = db.Column(db.Numeric)
    lng = db.Column(db.Numeric)


class DeviceSettings(db.Model):
    __tablename__ = 'device_settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    __table_args__ = (Index('settings_unique', 'device_id', 'key', unique=True),)


class LBSQueue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coord_rec_id = db.Column(db.BigInteger, db.ForeignKey('coordinates.id'), nullable=False)
    country_code = db.Column(db.Integer)
    operator_id = db.Column(db.Integer)
    lac = db.Column(db.Integer)
    cell_id = db.Column(db.Integer)
    signal_strength = db.Column(db.Numeric)
