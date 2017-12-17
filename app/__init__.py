from flask import Flask
from flask_bootstrap import Bootstrap, bootstrap_find_resource
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    config[config_name].init_app(app)
    app.config['SECRET_KEY'] = config[config_name].SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config[config_name].SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = config[config_name].SQLALCHEMY_COMMIT_ON_TEARDOWN
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config[config_name].SQLALCHEMY_TRACK_MODIFICATIONS
    moment.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


