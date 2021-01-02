import flask_login
from flask import jsonify, request, Blueprint
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

import model
from model import db
from web import abort_json

friends_page = Blueprint('friends_page', __name__, template_folder='templates')


@friends_page.route('/friends')
@login_required
def friends_list():
    friends = model.Friends.query.filter_by(user_id=flask_login.current_user.id).all()
    return jsonify(list(map(lambda x: x.friend, friends)))


@friends_page.route('/friends/request', methods=['GET'])
@login_required
def friends_requests():
    friends = model.Friends.query.filter_by(friend=flask_login.current_user.id, accepted=False).all()
    return jsonify(list(map(lambda x: {'friend': x.friend, 'id': x.id}, friends)))


@friends_page.route('/friends/accept/<int:id>', methods=['GET'])
@login_required
def friends_accept(id):
    rows = model.Friends.query.filter_by(friend=flask_login.current_user.id, id=id).update({'accepted': True})
    return jsonify({'result': rows})


@friends_page.route('/friends/reject/<int:id>', methods=['GET'])
@login_required
def friends_reject(id):
    rows = model.Friends.query.filter_by(friend=flask_login.current_user.id, id=id).update({'accepted': False})
    return jsonify({'result': rows})


@friends_page.route('/friends/remove/<int:id>', methods=['POST'])
@login_required
def friends_remove(id):
    model.Friends.query.filter_by(user_id=flask_login.current_user.id, id=id).delete()
    return jsonify({})


@friends_page.route('/friends/add', methods=['POST'])
@login_required
def friends_add():
    args = request.get_json()

    if args is None:
        return abort_json(400, message="No payload")

    friend_login = args.get("friend_login")
    friend = model.User.query.filter_by(login=friend_login).first()

    if friend is None or friend.id == flask_login.current_user.id:
        return abort_json(400, errors={'friend_login': 'Not found'})

    friend = model.Friends()
    friend.user_id = flask_login.current_user.id
    friend.friend = friend.id

    try:
        db.session().add(friend)
        db.session.commit()
    except IntegrityError:
        pass

    return jsonify({})
