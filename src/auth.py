from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, REQUESTS
from flask_login import login_user, login_required, logout_user, current_user
import os
import requests
from dotenv import load_dotenv
from timezonefinder import TimezoneFinder

auth = Blueprint('auth', __name__)
load_dotenv()
@auth.route('/login', methods=['GET', 'POST'])
def login():
    REQUESTS.inc()
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('views.home'))

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user), 200


@auth.route('/logout')
@login_required
def logout():
    REQUESTS.inc()
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/registration', methods=['GET', 'POST'])
def register():
    REQUESTS.inc()
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('views.home'))
        form_data = request.form
        email = form_data.get('email')
        username = form_data.get('userName')

        try:
            lati = float(form_data.get('latitude'))
            lon = float(form_data.get('longitude'))
            obj = TimezoneFinder()
            time_zone = obj.timezone_at(lng=lon, lat=lati)
        except ValueError:
            flash('Invalid input for latitude or longitude.', category='error')
            return render_template("register.html", user=current_user), 200

        aqt = float(form_data.get('air_quality_threshold'))
        allow_emails = (form_data.get('email_allowed') == 'Yes')
        password1 = form_data.get('password1')
        password2 = form_data.get('password2')
        email_verifier = os.getenv("EMAIL_VER_KEY")
        url = (f"https://api.emailvalidation.io/v1/info?apikey={email_verifier}&email={email}")
        payload = {}
        headers = {}
        email_response = requests.request("GET", url, headers=headers, data=payload).json()

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already in use.', category='error')
        elif email_response['state'] == 'undeliverable':
            flash('Invalid email entered.', category='error')
        elif len(username) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif aqt<0:
            flash('Negative numbers are not accepted for air quality threshold.', category='error')
        elif password1 != password2:
            flash('Your passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            new_user = User(email=email, username=username, latitude=lati, longitude=lon,
                            time_zone=time_zone, air_quality_threshold=aqt,
                            allow_emails=allow_emails, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("register.html", user=current_user), 200
