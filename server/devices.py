import flask_login
from flask import Blueprint, request, jsonify
from flask_login import login_required
from sqlalchemy import or_
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

import model
from app import socketio
from device_settings import settings_to_web_format
from web import abort_json, is_blank

devices_page = Blueprint('devices_page', __name__, template_folder='templates')


@devices_page.route('/devices/settings/<imei>', methods=['POST'])
def save_device_settings(imei=None):
    args = request.get_json()  # TODO validation
    device = model.Device.query.filter_by(user_id=flask_login.current_user.id, imei=imei).first()

    if device is None:
        abort_json(404, errors={'imei': 'None found'})

    stmt = insert(model.DeviceSettings).values(device_id=device.id, settings=args).prefix_with('IGNORE')

    model.db.session.execute(stmt)
    model.db.session.commit()

    return jsonify({})


@devices_page.route('/devices/add', methods=['POST'])
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
        model.db.session().add(device)
        model.db.session.commit()
    except IntegrityError:
        return abort_json(400, errors={"imei": "Imei already registered"})

    socketio.emit('new_device', {'data': {}}, room='__user_'+str(flask_login.current_user.id))

    return jsonify({})


@devices_page.route('/devices')
@login_required
def get_devices():
    subquery = model.SharedDevices.query. \
        with_entities(model.SharedDevices.device_id).filter_by(shared_with=flask_login.current_user.id).subquery()

    devices = model.Device.query. \
        options(joinedload(model.Device.user, innerjoin=True), joinedload(model.Device.settings, innerjoin=False)) \
        .filter(or_(model.Device.user_id.in_(subquery), model.Device.user_id == flask_login.current_user.id)).all()

    return jsonify(list(
        map(lambda x: {'name': x.name,
                       'id': x.id,
                       'imei': x.imei,
                       'settings': (settings_to_web_format(x.settings.settings if x.settings else None)),
                       'is_shareable': x.user.id == flask_login.current_user.id and x.is_shareable,
                       'user': {'id': x.user.id, 'name': x.user.login,
                                'shared': x.user.id != flask_login.current_user.id}},
            devices)))


@devices_page.route('/devices/remove/<imei>', methods=['DELETE'])
@login_required
def remove_device(imei):
    devices = model.Device.query.filter_by(user_id=flask_login.current_user.id, imei=imei).delete()
    model.db.session.commit()

    socketio.emit('removed_device', {'data': {}}, room='__user_'+str(flask_login.current_user.id))
    socketio.emit('removed_device', {'data': {}}, room='__device_'+str(imei))

    return jsonify(list(map(lambda x: {'name': x.name, 'id': x.id, 'imei': x.imei}, devices)))
