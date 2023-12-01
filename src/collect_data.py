from . import db
from flask_login import login_required, current_user
import requests
from dotenv import load_dotenv
import os
from .models import LocationAirQuality, User
from .analyze_data import average_location_data

load_dotenv()

AQI_KEY = os.getenv("AQI_KEY")

@login_required
def get_forecast():
    url = (f"https://api.waqi.info/feed/geo:{current_user.latitude};{current_user.longitude}/?token={AQI_KEY}")
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    forecast = response['data']['forecast']['daily']
    max1 = max(forecast['o3'][0]['avg'], forecast['pm10'][0]['avg'], forecast['pm25'][0]['avg'])
    max2 = max(forecast['o3'][1]['avg'], forecast['pm10'][1]['avg'], forecast['pm25'][1]['avg'])
    max3 = max(forecast['o3'][2]['avg'], forecast['pm10'][2]['avg'], forecast['pm25'][2]['avg'])
    return_value = {"one_day": max1,
                    "two_day": max2,
                    "three_day": max3}
    return return_value


def get_today_aq(latitude, longitude):
    url = (f"https://api.waqi.info/feed/geo:{latitude};{longitude}/?token={AQI_KEY}")
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    aq = response['data']['aqi']
    idx = response['data']['idx']
    city = response['data']['city']['name']
    last_time_collected = response['data']['time']['iso']
    aq_entry = LocationAirQuality.query.get(idx)
    return_value = [aq, idx, city]
    if aq_entry:
        if aq_entry.last_time_collected.__eq__(last_time_collected):
            return return_value
        else:
            average_location_data(aq, aq_entry, last_time_collected)
    else:
        new_location = LocationAirQuality(location_id=idx, particulate_matter_level_average=aq,
                                          particulate_matter_level_current=aq, last_time_collected=last_time_collected)
        db.session.add(new_location)
        db.session.commit()

    return return_value


def update_all():
    users = User.query.all()
    print(users)
    for user in users:
        lat = user.latitude
        long = user.longitude
        get_today_aq(lat, long)
        print(user.username)
    print("Updated all locations linked to a user!")
