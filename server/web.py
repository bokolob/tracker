import flask_login
from flask_login import login_user, login_required, logout_user

import model
from flask import abort, jsonify, render_template, request, make_response, redirect, send_from_directory
from sqlalchemy import and_, desc
from app import app, db, login_manager
from email.utils import parseaddr


@login_manager.user_loader
def load_user(user_id):
    return model.User.query.filter_by(id=int(user_id)).first()


@app.route('/', methods=['POST', 'GET'])
def root():
    return render_template('login.html')


@app.route('/auth', methods=['POST', 'GET'])
def login():
    args = request.get_json()

    if args is None:
        abort_json(400, message="No payload")

    email = args.get("email")
    pass1 = args.get("password")

    user = model.User.query.filter_by(login=email).first()

    if user is None:
        abort_json(403, message="User not found")

    if user.verify_password(pass1):
        login_user(user, remember=True)
        return jsonify({'redirect': "/map"})

    abort_json(403, message="User not found")


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/devices/add', methods=['POST'])
def add_device():
    args = request.get_json()

    if args is None:
        abort_json(400, message="No payload")

    imei = args.get("imei")
    name = args.get("name")

    if is_blank(imei) or is_blank(name):
        abort(make_response(jsonify(message="Required fields are empty", fields="*"), 400))

    device = model.Device.query.filter_by(imei=imei).first()

    if device is not None:
        abort_json(400, message="Imei already registered", fields="imei")

    device = model.Device
    device.imei = imei
    device.user_id = flask_login.current_user.id
    device.name = name

    db.session().add(device)
    db.session.commit()

    return jsonify({})


@app.route('/signup', methods=['POST'])
def signup():
    args = request.get_json()

    if args is None:
        abort_json(400, message="No payload")

    imei = args.get("imei")
    email = args.get("email")
    pass1 = args.get("password")
    pass2 = args.get("password_confirm")

    if is_blank(imei) or is_blank(email) or is_blank(pass1) or is_blank(pass2):
        abort(make_response(jsonify(message="Required fields are empty", fields="*"), 400))

    if pass1 != pass2:
        abort(make_response(jsonify(message="Passwords are different", fields="password"), 400))

    if '@' not in parseaddr(email)[1]:
        abort(make_response(jsonify(message="invalid email", fields="email"), 400))

    device = model.Device.query.filter_by(imei=imei).first()

    if device is not None:
        abort_json(400, message="Imei registered", fields="imei")

    user = model.User()
    user.password = pass1
    user.login = email
    user.name = ""

    db.session().add(user)
    db.session.commit()
    # TODO add device

    return jsonify({})


def abort_json(code, **kwargs):
    return abort(make_response(jsonify(kwargs), code))


def is_blank(s):
    return bool(not s or s.isspace())


@app.route('/map')
@login_required
def index():
    return render_template('leaflet.html', imei="deadbeef")


@app.route('/devices')
@login_required
def get_devices():
    devices = model.Device.query.filter_by(user_id=flask_login.current_user.id).all()
    return jsonify(list(map(lambda x: {'name': x.name, 'id': x.id, 'imei': x.imei}, devices)))


@app.route('/<imei>/coordinates')
@login_required
def get_coordinates(imei=None):
    # TODO auth and imei check
    device = model.Device.query.filter_by(imei=imei, user_id=flask_login.current_user.id).first()

    if device is None:
        abort(404, description="Device not found")

    shifted = device.id << 32
    shifted_high = (device.id + 1) << 32

    rs = model.Coordinates.query.with_entities(model.Coordinates.lat, model.Coordinates.lng) \
        .filter(and_(model.Coordinates.id > shifted, model.Coordinates.id < shifted_high)) \
        .order_by(desc(model.Coordinates.id)).limit(60).all()

    return jsonify(list(map(lambda x: [str(x.lat), str(x.lng)], rs)))
