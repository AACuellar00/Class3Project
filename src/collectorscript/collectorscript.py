from flask import Flask
import os
from src.collect_data import update_all
from src import db
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

load_dotenv()
DB_NAME = "database.db"

app = Flask(__name__)
uri = os.getenv('DATABASE_URL')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db.init_app(app)

with app.app_context():
    db.create_all()


def scheduled_task():
    with app.app_context():
        update_all()


@app.route("/")
def home():
    return "This updates the data", 200


scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_task, trigger="interval", minutes=60)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


