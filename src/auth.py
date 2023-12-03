from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, REQUESTS
from flask_login import login_user, login_required, logout_user, current_user
import os
import requests
from dotenv import load_dotenv

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

        email = request.form.get('email')
        username = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
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
            print('Invalid email entered.')
        elif len(username) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Your passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("register.html", user=current_user), 200
