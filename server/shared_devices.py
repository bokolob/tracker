import time

import flask_login
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from flask import jsonify, request, Blueprint, url_for
from flask_login import login_required
from sqlalchemy import or_, asc, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

import model
from app import csrf, socketio
from model import db
from web import abort_json, is_blank

shared_devices_page = Blueprint('shared_page', __name__, template_folder='templates')
key = bytearray.fromhex('754409aece52cc7c71c5ebd3e684e23ae2b288c25f70a1c91d86479920ebea76')
iv = bytearray.fromhex('afd607ff3c9a34261a76129b1767efb3')
cipher = Cipher(algorithms.AES(key), modes.CFB(iv))


@shared_devices_page.route('/shared/list', methods=['GET'])
@login_required
def shared_list():
    devices = model.SharedDevices.query \
        .options(joinedload(model.SharedDevices.device, innerjoin=True).joinedload(model.Device.user, innerjoin=True)) \
        .filter(or_(model.Device.user_id == flask_login.current_user.id,
                    model.SharedDevices.shared_with == flask_login.current_user.id)) \
        .order_by(asc(model.Device.id)) \
        .all()

    def converter(x):
        return {
            'id': x.id,
            'is_mine': x.device.user.id == flask_login.current_user.id,
            'owner': x.device.user.name,
            'device_id': x.device.id,
            'device_name': x.device.name,
        }

    return jsonify(list(map(converter, devices)))


@shared_devices_page.route('/shared/link/<token>', methods=['GET'])
@csrf.exempt
@login_required
def shared_accept(token):
    if is_blank(token):
        return abort_json(400, message="No token")

    decryptor = cipher.decryptor()
    content = (decryptor.update(bytearray.fromhex(token)) + decryptor.finalize()).decode("latin1")

    if not content.startswith("deadbeef"):
        return abort_json(400, message="Invalid link")

    (prefix, ts, device_id) = content.split(":")

    if time.time() > int(ts) + 24 * 3600:
        return abort_json(400, message="Stale link")

    device = model.Device.query.filter(
        and_(model.Device.id == device_id, model.Device.user_id != flask_login.current_user.id)).first()

    if device is None:
        return abort_json(400, errors={'device_id': 'Not found'})

    new_record = model.SharedDevices()
    new_record.shared_with = flask_login.current_user.id
    new_record.device_id = device.id

    try:
        db.session().add(new_record)
        db.session.commit()
    except IntegrityError:
        pass

    socketio.emit('new_device', {'data': {}}, room='__user_' + str(flask_login.current_user.id))
    socketio.emit('device_shared_with', {'data': {}}, room='__user_' + str(device.user_id))

    return jsonify({})


@shared_devices_page.route('/shared/<int:id>', methods=['DELETE'])
@login_required
def shared_reject(id):
    rows = model.SharedDevices.query.filter_by(shared_with=flask_login.current_user.id, id=id).delete()
    db.session.commit()
    return jsonify({'result': rows})


@shared_devices_page.route('/shared/link', methods=['POST'])
@login_required
def gen_link_for_device():
    args = request.get_json()

    if args is None:
        return abort_json(400, message="No payload")

    device_id = args.get("device_id")
    device = model.Device.query.filter_by(id=device_id, user_id=flask_login.current_user.id, is_shareable=True).first()

    if device is None:
        return abort_json(400, errors={'device_id': 'Not found'})

    data = ":".join(("deadbeef", str(int(time.time())), str(device.id)))
    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(data, "latin1")) + encryptor.finalize()

    return jsonify({'link': url_for('shared_page.shared_accept', _external=True, token=ct.hex())})
