import functools

import flask_login
from flask import Blueprint
from flask_login import current_user
from flask_socketio import disconnect, emit, join_room

import model
from app import socketio

event_source_page = Blueprint('event_source_page', __name__)


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@socketio.on('connect')
@authenticated_only
def test_connect():
    room = '__user_' + str(current_user.id)
    join_room(room)


@socketio.on('subscribe_on_device')
@authenticated_only
def subscribe_on_device(data):
    print('Received data (subscribe_on_device): ', data)
    device = model.Device.query.filter_by(user_id=flask_login.current_user.id, imei=data['imei']).first()

    if device is None:
        emit('error', {'data': 'Bad imei'})  # TODO callback?

    join_room("__device_" + str(device.id))
