from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from .. import db
from dotenv import load_dotenv
from flask_mail import Mail, Message
from src.collect_data import get_today_aq
from src.models import User

load_dotenv()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    uri = os.getenv('DATABASE_URL')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    db.init_app(app)

    from ..models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    mail = Mail(app)

    @app.route("/")
    def index():
        users = User.query.all()
        for user in users:
            aq = get_today_aq(user.latitude, user.longitude)[0]
            thresh = user.air_quality_threshold
            if aq < thresh:
                message = f"Today's air quality is {aq}. This is under your threshold of {thresh}."
            else:
                message = f"Today's air quality is {aq}. This is over your threshold of {thresh}."
            msg = Message(subject="Today's forecast", sender=('Adrian', os.getenv('MAIL_USERNAME')),
                          recipients=[user.email])
            msg.body = message
            print("Message sent1")
            mail.send(msg)
            print("Message sent2")
        return "Message(s) sent!"

    return app
