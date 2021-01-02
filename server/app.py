import os

from flask import Flask
from flask_login import LoginManager

import model

login_manager = LoginManager()


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
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    from model import db
    db.init_app(app)

    with app.app_context():
        model.db.create_all()

    # db.init_app(app)
    login_manager.init_app(app)

    from friends import friends_page
    from web import main_page
    app.register_blueprint(friends_page)
    app.register_blueprint(main_page)

    return app
