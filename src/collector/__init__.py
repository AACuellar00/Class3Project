import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from src.collect_data import update_all
from .. import db

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sdaiufhasldfjhasd'
    uri = os.getenv("DATABASE_URL")
    if uri and uri.startswith("postgres:://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = (uri)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        update_all()

    return app

def create_database(app):
    if not path.exists('' + DB_NAME):
        db.create_all(app=app)