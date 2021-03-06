from urllib.parse import urlparse

import flask_login
from flask import abort, jsonify, render_template, request, make_response, redirect, send_from_directory, Blueprint
from flask_login import login_user, login_required, logout_user
from flask_wtf.csrf import generate_csrf
from sqlalchemy import and_, asc, or_, desc
from sqlalchemy.exc import IntegrityError

import model
from app import csrf
from model import db
from validators import validated

main_page = Blueprint('main_page', __name__, template_folder='templates')


@main_page.route('/', methods=['POST', 'GET'])
def root():
    return render_template('login.html', target=request.args.get('next', '', type=str))


def process_target_url(target):
    if not is_blank(target):
        o = None
        try:
            o = urlparse(target)
        except ValueError:
            pass

        if o is not None:
            return o[2] + '?' + o[3]

    return None


@main_page.route('/auth', methods=['POST', 'GET'])
@csrf.exempt
@validated
def login():
    args = request.get_json()

    email = args.get("email")
    pass1 = args.get("password")

    user = model.User.query.filter_by(login=email).first()

    if user is None:
        abort_json(403, errors={"email": "User not found"})

    if user.verify_password(pass1):
        login_user(user, remember=True)
        possible_redirect = process_target_url(args.get('target')) or '/map'
        return jsonify({'redirect': possible_redirect})

    abort_json(403, errors={"email": "User not found"})


@main_page.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@main_page.route('/app/<path:path>')
def send_app(path):
    return send_from_directory('js/tracker-frontend/dist', path)


@main_page.route("/logout")
@login_required
def logout():
    logout_user()

    if request.accept_mimetypes['application/json']:
        return jsonify({})

    return redirect("/")


@main_page.route("/csrf")
@login_required
def get_csrf():
    return jsonify({"csrf": generate_csrf()});


@main_page.route('/signup', methods=['POST'])
@csrf.exempt
@validated
def signup():
    args = request.get_json()

    imei = args.get("imei")
    email = args.get("email")
    pass1 = args.get("password")
    pass2 = args.get("password_confirm")

    errors = {}

    if pass1 != pass2:
        errors["password_confirm"] = "Passwords must be the same"

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
    possible_redirect = process_target_url(args.get('target')) or '/map'
    return jsonify({'redirect': possible_redirect})


def abort_json(code, **kwargs):
    return abort(make_response(jsonify(kwargs), code))


def is_blank(s):
    return bool(not s or s.isspace())


@main_page.route('/map')
@login_required
def index():
    return render_template('leaflet.html')


@main_page.route('/<imei>/coordinates')
@login_required
def get_coordinates(imei=None):
    since = request.args.get('since', None, type=int)
    until = request.args.get('until', None, type=int)
    direction = request.args.get('direction', 'asc', type=str)

    if since is not None:
        if since > 2 ** 31 or since < 0:
            abort(400, description="Bad 'since' param")

    subquery = model.SharedDevices.query. \
        with_entities(model.SharedDevices.device_id).filter_by(shared_with=flask_login.current_user.id).subquery()

    device = model.Device.query.with_entities(model.Device.id) \
        .filter(model.Device.imei == imei,
                or_(model.Device.id.in_(subquery), model.Device.user_id == flask_login.current_user.id)
                ).first()

    if device is None:
        abort(404, description="Device not found")

    shifted = device.id << 32
    shifted_high = (device.id + 1) << 32
    timestamp_mask = 0xffffffff

    where = [model.Coordinates.id > shifted, model.Coordinates.id < shifted_high]

    if since is not None:
        since = shifted | since
        where.append(model.Coordinates.id > since)

    if until is not None:
        until = shifted | until
        where.append(model.Coordinates.id <= until)

    if direction == 'asc':
        order_stm = asc(model.Coordinates.id)
    else:
        order_stm = desc(model.Coordinates.id)

    rs = model.Coordinates.query.with_entities(model.Coordinates.lat, model.Coordinates.lng, model.Coordinates.id) \
        .filter(and_(*where)).order_by(order_stm).limit(100).all()

    return jsonify(list(map(lambda x: {'lat': str(x.lat), 'lng': str(x.lng), 'ts': int(x.id & timestamp_mask)}, rs)))
