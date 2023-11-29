from flask import Flask
from os import path
from flask_login import LoginManager
from src.collect_data import update_all
from .. import db

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sdaiufhasldfjhasd'
    app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql://cdiciireuzgfrd'
                                             ':a29648edfc241975347522ecdc215496642e61203915bd34431dc4af79971658@ec2'
                                             '-52-21-61-131.compute-1.amazonaws.com:5432/d46iufn0n1hobk')
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