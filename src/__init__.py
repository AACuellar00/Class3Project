from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


def create_app():
    app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
    app.config['SECRET_KEY'] = 'fhakjlssdfhaeunfa'

    from src.frontend.views import views

    app.register_blueprint(views, url_prefix='/')
    return app
