from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from . import db
from flask_login import login_required, current_user
import requests
from dotenv import load_dotenv
import os
from .collect_data import get_today_aq, get_forecast

load_dotenv()

views = Blueprint('views', __name__)

AV_KEY = os.getenv("AV_KEY")


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return_value = get_today_aq(current_user.latitude, current_user.longitude)
    data = {'aq': return_value[0], 'station': return_value[1], 'cityN': return_value[2]}
    forecast = get_forecast()
    return render_template("home.html", user=current_user, data=data, forecast=forecast)


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        form_data = request.form
        try:
            lat = float(form_data.get('latitude'))
            current_user.latitude = lat
        except ValueError:
            flash('Invalid input for latitude.', category='error')
            return redirect(url_for(settings.html))
        try:
            lon = float(form_data.get('longitude'))
            current_user.longitude = lon
        except ValueError:
            flash('Invalid input for longitude.', category='error')
            return redirect(url_for(settings.html))
        try:
            aqt = float(form_data.get('air_quality_threshold'))
            if aqt >= 0:
                current_user.current_user.air_quality_threshold = aqt
            else:
                flash('Negative numbers are not accepted for air quality threshold.', category='error')
                return redirect(url_for(settings.html))
        except ValueError:
            flash('Invalid input for air quality threshold.', category='error')
            return redirect(url_for(settings.html))

        current_user.allow_emails = (form_data.get('email_allowed') == 'Yes')
        db.session.commit()

        return redirect(url_for('views.home'))
    return render_template('settings.html',
                           lat=current_user.latitude, lon=current_user.longitude,
                           aqt=current_user.air_quality_threshold)
