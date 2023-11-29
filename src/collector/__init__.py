from flask import Flask
import os
from flask_login import LoginManager
from src.collect_data import update_all
from .. import db

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    uri = os.getenv('DATABASE_URL')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        update_all()

    return app
