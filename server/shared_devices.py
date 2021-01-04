import flask_login
from flask import jsonify, request, Blueprint
from flask_login import login_required
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

import model
from model import db
from web import abort_json

shared_devices_page = Blueprint('shared_page', __name__, template_folder='templates')


@shared_devices_page.route('/shared/list', methods=['GET'])
@login_required
def friends_list():
    devices = model.Device.query \
        .options(joinedload(model.Device.share, innerjoin=True), joinedload(model.Device.user, innerjoin=True)) \
        .filter(or_(model.Device.user_id == flask_login.current_user.id,
                    model.SharedDevices.shared_with == flask_login.current_user.id)).all()

    def converter(x):
        return {
            'id': x.share.id,
            'owner': x.user.name,
            'device_id': x.id,
            'state': x.share.state.value
        }

    return jsonify(list(map(converter, devices)))


@shared_devices_page.route('/shared/accept/<int:id>', methods=['GET'])
@login_required
def friends_accept(id):
    rows = model.SharedDevices.query.filter_by(shared_with=flask_login.current_user.id, id=id,
                                               state=model.SharingState.requested).update(
        {'state': model.SharingState.accepted})
    db.session.commit()

    return jsonify({'result': rows})


@shared_devices_page.route('/shared/revoke/<int:id>', methods=['GET'])
@login_required
def friends_reject(id):
    rows = model.SharedDevices.query.filter_by(shared_with=flask_login.current_user.id, id=id).update(
        {'state': model.SharingState.declined})
    db.session.commit()
    return jsonify({'result': rows})


@shared_devices_page.route('/shared/request', methods=['POST'])
@login_required
def friends_add():
    args = request.get_json()

    if args is None:
        return abort_json(400, message="No payload")

    friend_login = args.get("friend_login")
    friend = model.User.query.filter_by(login=friend_login).first()

    if friend is None or friend.id == flask_login.current_user.id:
        return abort_json(400, errors={'friend_login': 'Not found'})

    device_id = args.get("device_id")
    device = model.Device.query.filter_by(id=device_id).first()

    if device is None:
        return abort_json(400, errors={'device_id': 'Not found'})

    new_record = model.SharedDevices()
    new_record.shared_with = friend.id
    new_record.device_id = device_id

    try:
        db.session().add(new_record)
        db.session.commit()
    except IntegrityError:
        pass

    return jsonify({})
