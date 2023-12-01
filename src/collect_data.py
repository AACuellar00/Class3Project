from . import db
import requests
from dotenv import load_dotenv
import os
from .models import LocationAirQuality, User
from .analyze_data import average_location_data

load_dotenv()

AQI_KEY = os.getenv("AQI_KEY")


def get_data(latitude, longitude, get_which):
    url = (f"https://api.waqi.info/feed/geo:{latitude};{longitude}/?token={AQI_KEY}")
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    if get_which == 'forecast':
        return get_forecast(response['data'])
    else:
        return get_today_aq(response['data'], False)


def get_forecast(response):
    forecast = response['forecast']['daily']
    max1 = max(forecast['o3'][0]['avg'], forecast['pm10'][0]['avg'], forecast['pm25'][0]['avg'])
    max2 = max(forecast['o3'][1]['avg'], forecast['pm10'][1]['avg'], forecast['pm25'][1]['avg'])
    max3 = max(forecast['o3'][2]['avg'], forecast['pm10'][2]['avg'], forecast['pm25'][2]['avg'])
    return_value = {"one_day": max1,
                    "two_day": max2,
                    "three_day": max3}
    return return_value


def get_today_aq(response, test):
    aq = response['aqi']
    idx = response['idx']
    city = response['city']['name']
    last_time_generated = response['time']['iso']
    return_value = {"aqi": aq, "idx": idx, "city": city}
    if not test:
        aq_entry = LocationAirQuality.query.get(idx)
        if aq_entry:
            if aq_entry.last_time_collected.__eq__(last_time_generated):
                return return_value
            else:
                average_location_data(aq, aq_entry, last_time_generated)
        else:
            new_location = LocationAirQuality(location_id=idx, particulate_matter_level_average=aq,
                                              particulate_matter_level_current=aq,
                                              last_time_collected=last_time_generated)
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
