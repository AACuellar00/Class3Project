from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv
from prometheus_client import Counter

db = SQLAlchemy()
DB_NAME = "database.db"
load_dotenv()
REQUESTS = Counter("total_application_requests", "Total HTTP requests to the application.")


def create_app():
    app = Flask(__name__)

    uri = os.getenv('DATABASE_URL')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    if os.getenv('ENV').__eq__('test'):
        app.config['TESTING'] = True
        uri = f'sqlite:///{DB_NAME}'

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    db.init_app(app)

    from src.views import views
    from src.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from src.models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
