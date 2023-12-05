from flask import Flask
import os
from flask_login import LoginManager
from .. import db
from dotenv import load_dotenv
from flask_mail import Mail, Message
from src.collect_data import get_data
from datetime import datetime
from src.analyze_data import threshold_less_than_aq_of_day
from zoneinfo import ZoneInfo

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

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail = Mail(app)

    with app.app_context():
        users = User.query.all()
        for user in users:
            user_time = datetime.now(tz=ZoneInfo(user.time_zone))
            user_hour = user_time.strftime("%H")
            if user.allow_emails:
                if user_hour.__eq__("7"):
                    data = get_data(user.latitude, user.longitude, "today_aq")
                    if not data["last_time_gen"].__eq__(user.last_time_sent):
                        print(f"Sending emai to {user.username}")
                        aq = data["aqi"]
                        thresh = user.air_quality_threshold
                        if threshold_less_than_aq_of_day(thresh, aq) == 1:
                            message = f"Today's air quality near you is {aq}. This is under your threshold of {thresh}."
                        else:
                            message = f"Today's air quality near you is {aq}. This is over your threshold of {thresh}."
                        msg = Message(subject="Today's forecast", sender=('Adrian', os.getenv('MAIL_USERNAME')),
                                      recipients=[user.email])
                        msg.body = message
                        mail.send(msg)
                        user.last_time_sent = data["last_time_gen"]
                        db.session.commit()
        print("Message(s) sent!")

    return app
