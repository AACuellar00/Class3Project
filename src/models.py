from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Float(12), default=37.773972)
    longitude = db.Column(db.Float(12), default=-122.431297)
    time_zone = db.Column(db.String(50), default="America/Los_Angeles")
    air_quality_threshold = db.Column(db.Integer, default=50)
    allow_emails = db.Column(db.Boolean, default=False)
    last_time_sent=db.Column(db.String(30), default="")


class LocationAirQuality(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    particulate_matter_level_current = db.Column(db.Integer)
    particulate_matter_level_average = db.Column(db.Integer)
    times_averaged = db.Column(db.Integer, default=1)
    last_time_collected = db.Column(db.String(30), default="")
