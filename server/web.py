import model
from flask import abort, jsonify, render_template
from sqlalchemy import and_, desc
from app import app


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/map')
def index():
    return render_template('leaflet.html')


@app.route('/<imei>/coordinates')
def get_coordinates(imei=None):
    # TODO auth and imei check
    device = model.Device.query.filter_by(imei=imei).first()

    if device is None:
        abort(404, description="Device not found")

    shifted = device.id << 32
    shifted_high = (device.id + 1) << 32

    rs = model.Coordinates.query.with_entities(model.Coordinates.lat, model.Coordinates.lng) \
        .filter(and_(model.Coordinates.id > shifted, model.Coordinates.id < shifted_high)) \
        .order_by(desc(model.Coordinates.id)).limit(20).all()

    return jsonify(list(map(lambda x: [str(x.lat), str(x.lng)], rs)))


@app.route('/hello')
def hello():
    return 'Hello, World!'
