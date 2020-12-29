import flask_login
from flask_login import login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

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
        abort_json(403, errors={"email": "User not found"})

    if user.verify_password(pass1):
        login_user(user, remember=True)
        return jsonify({'redirect': "/map"})

    abort_json(403, errors={"email": "User not found"})


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
    errors = {}

    if is_blank(imei):
        errors['imei'] = "Field is required"

    if is_blank(name):
        errors['name'] = "Field is required"

    if len(errors) > 0:
        return abort_json(400, errors=errors)

    device = model.Device()
    device.imei = imei
    device.user_id = flask_login.current_user.id
    device.name = name

    try:
        db.session().add(device)
        db.session.commit()
    except IntegrityError:
        return abort_json(400, errors={"imei": "Imei already registered"})

    return jsonify({})


@app.route('/signup', methods=['POST'])
def signup():
    args = request.get_json()

    if args is None:
        return abort_json(400, message="No payload")

    imei = args.get("imei")
    email = args.get("email")
    pass1 = args.get("password")
    pass2 = args.get("password_confirm")

    errors = {}

    if is_blank(imei):
        errors["imei"] = "Imei must be filled in"

    if is_blank(email):
        errors["email"] = "Email must be filled in"

    if is_blank(pass1) or is_blank(pass2):
        errors["password"] = "Password must be filled in"

    if pass1 != pass2:
        errors["password_confirm"] = "Passwords must be the same"

    if not is_blank(email) and '@' not in parseaddr(email)[1]:
        errors["email"] = "Invalid email"

    if not is_blank(imei):
        device = model.Device.query.filter_by(imei=imei).first()

        if device is not None:
            errors["imei"] = "Imei already registered"

    if len(errors) > 0:
        return abort_json(400, errors=errors)

    user = model.User()
    user.password = pass1
    user.login = email
    user.name = ""

    try:
        db.session().add(user)
        db.session.commit()
    except IntegrityError:
        return abort_json(400, errors={"email": "Already registered"})

    # TODO add device
    login_user(user, remember=True)
    return jsonify({'redirect': "/map"})


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


@app.route('/devices/remove/<imei>')
@login_required
def remove_device(imei):
    devices = model.Device.query.filter_by(user_id=flask_login.current_user.id, imei=imei).delete()
    db.session.commit()
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
