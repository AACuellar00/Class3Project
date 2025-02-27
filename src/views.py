from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db, REQUESTS
from flask_login import login_required, current_user
from .collect_data import get_data
from .analyze_data import threshold_less_than_aq_of_day
from timezonefinder import TimezoneFinder
from prometheus_client import generate_latest

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    REQUESTS.inc()
    lat = current_user.latitude
    lon = current_user.longitude
    return_value = get_data(lat, lon, 'today_aq')
    data = {'aq': return_value['aqi'], 'station': return_value['idx'], 'cityN': return_value['city'],
            'average': return_value['average_aq']}
    forecast = get_data(lat, lon, 'forecast')
    threshold_under_aq_list = [threshold_less_than_aq_of_day(current_user.air_quality_threshold, return_value['aqi']),
                               threshold_less_than_aq_of_day(current_user.air_quality_threshold, forecast["one_day"]),
                               threshold_less_than_aq_of_day(current_user.air_quality_threshold, forecast["two_day"]),
                               threshold_less_than_aq_of_day(current_user.air_quality_threshold, forecast["three_day"])]
    return render_template("home.html", user=current_user, data=data,
                           forecast=forecast, threshold_under_aq_list=threshold_under_aq_list), 200


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    REQUESTS.inc()
    if request.method == 'POST':
        form_data = request.form
        try:
            lati = float(form_data.get('latitude'))
            current_user.latitude = lati
            lon = float(form_data.get('longitude'))
            current_user.longitude = lon
            obj = TimezoneFinder()
            time_zone = obj.timezone_at(lng=lon, lat=lati)
            current_user.time_zone = time_zone
        except ValueError:
            flash('Invalid input for latitude or longitude.', category='error')
            return redirect(url_for('views.settings'))
        try:
            aqt = float(form_data.get('air_quality_threshold'))
            if aqt >= 0:
                current_user.air_quality_threshold = aqt
            else:
                flash('Negative numbers are not accepted for air quality threshold.', category='error')
                return redirect(url_for('views.settings'))
        except ValueError:
            flash('Invalid input for air quality threshold.', category='error')
            return redirect(url_for('views.settings'))

        current_user.allow_emails = (form_data.get('email_allowed') == 'Yes')
        db.session.commit()

        return redirect(url_for('views.home'))
    return render_template('settings.html',
                           lat=current_user.latitude, lon=current_user.longitude,
                           aqt=current_user.air_quality_threshold), 200



@views.route("/health")
async def health():
    return "Healthy Application Here", 200

@views.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest()


@views.route('/latitude:<latitude>/longitude:<longitude>', methods=['GET', 'POST'])
def location(latitude,longitude):
    REQUESTS.inc()
    try:
        lat = float(latitude)
        long = float(longitude)
        obj = TimezoneFinder()
        time_zone = obj.timezone_at(lng=long, lat=lat)
        current_user.time_zone = time_zone
    except ValueError:
        flash('Invalid input for latitude or longitude. Here is an example of proper coordinates. ', category='error')
        return redirect(url_for('views.location', latitude=37.77,longitude=-122.43))

    return_value = get_data(lat, long, 'today_aq')
    data = {'aq': return_value['aqi'], 'station': return_value['idx'], 'cityN': return_value['city'],
            'average': return_value['average_aq']}
    forecast = get_data(lat, long, 'forecast')
    return render_template("location.html", data=data,
                           forecast=forecast), 200