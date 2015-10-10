from flask import Flask
from flask.ext.mongoengine import MongoEngine

from config import config

db = MongoEngine()

def create_app(config_name):
    app = Flask(__name__, 
        template_folder=config[config_name].TEMPLATE_PATH, static_folder=config[config_name].STATIC_PATH)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    db.init_app(app)

    from main.urls import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app