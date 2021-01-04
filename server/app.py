import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

import model

login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    return model.User.query.filter_by(id=int(user_id)).first()


def create_app(config_filename):
    app = Flask(__name__,
                static_url_path='',
                static_folder='/static')

    # app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['DEBUG'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = None
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    from model import db
    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        model.db.create_all()

    login_manager.init_app(app)

    from web import main_page
    from devices import devices_page
    from shared_devices import shared_devices_page

    app.register_blueprint(main_page)
    app.register_blueprint(devices_page)
    app.register_blueprint(shared_devices_page)

    return app
