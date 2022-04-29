import pathlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='templates')

    from app.users.users_blueprint import user_blueprints

    app.register_blueprint(user_blueprints)

    app.config['SECRET_KEY'] = 'thisisnoorproject'


    # sqlalchemy .db location (for sqlite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    # sqlalchemy track modifications in sqlalchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # enable debugging mode
    app.config["DEBUG"] = True
    PARENT_PATH = str(pathlib.Path(__file__).parent.resolve())
    UPLOAD_FOLDER = PARENT_PATH + '\static'

    # Upload folder
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)

    return app
