from flask_testing import TestCase
from flask import Flask
import pytest
from src.models import User, LocationAirQuality
from .. import create_app, db
from src.collect_data import get_today_aq


def mock_aq_forecast():
    mock_data = {
        "aqi": 27,
        "idx": 3900,
        "city": {
            "geo": [
                42,
                -42
            ],
            "name": "Mock City",
        },
        "dominentpol": "o3",
        "iaqi": {
            "o3": {
                "v": 27
            },

            "pm25": {
                "v": 13
            },

        },
        "time": {
            "iso": "2023-12-03T23:00:00-08:00"
        },
        "forecast": {
            "daily": {
                "o3": [
                    {
                        "avg": 2,
                        "day": "2023-11-28",
                        "max": 13,
                        "min": 1
                    },
                    {
                        "avg": 4,
                        "day": "2023-11-29",
                        "max": 14,
                        "min": 1
                    },
                    {
                        "avg": 15,
                        "day": "2023-11-30",
                        "max": 19,
                        "min": 7
                    },
                ],
                "pm10": [
                    {
                        "avg": 47,
                        "day": "2023-11-28",
                        "max": 55,
                        "min": 16
                    },
                    {
                        "avg": 31,
                        "day": "2023-11-29",
                        "max": 44,
                        "min": 10
                    },
                    {
                        "avg": 7,
                        "day": "2023-11-30",
                        "max": 16,
                        "min": 2
                    },
                ],
                "pm25": [
                    {
                        "avg": 100,
                        "day": "2023-11-28",
                        "max": 119,
                        "min": 45
                    },
                    {
                        "avg": 10,
                        "day": "2023-11-29",
                        "max": 98,
                        "min": 36
                    },
                    {
                        "avg": 12,
                        "day": "2023-11-30",
                        "max": 49,
                        "min": 3
                    },
                ]
            }
        },
    }
    return mock_data


def mock_aq_forecast_two():
    mock_data = {
        "aqi": 27,
        "idx": 12851,
        "city": {
            "geo": [
                42.331427,
                -83.0457538
            ],
            "name": "Mock City",
        },
        "dominentpol": "pm25",
        "iaqi": {
            "pm25": {
                "v": 27
            },
        },
        "time": {
            "iso": "2023-12-03T23:00:00-06:00"
        },
        "forecast": {
            "daily": {
                "o3": [
                    {
                        "avg": 2,
                        "day": "2023-11-28",
                        "max": 13,
                        "min": 1
                    },
                    {
                        "avg": 4,
                        "day": "2023-11-29",
                        "max": 14,
                        "min": 1
                    },
                    {
                        "avg": 15,
                        "day": "2023-11-30",
                        "max": 19,
                        "min": 7
                    },
                ],
                "pm10": [
                    {
                        "avg": 47,
                        "day": "2023-11-28",
                        "max": 55,
                        "min": 16
                    },
                    {
                        "avg": 31,
                        "day": "2023-11-29",
                        "max": 44,
                        "min": 10
                    },
                    {
                        "avg": 7,
                        "day": "2023-11-30",
                        "max": 16,
                        "min": 2
                    },
                ],
                "pm25": [
                    {
                        "avg": 100,
                        "day": "2023-11-28",
                        "max": 119,
                        "min": 45
                    },
                    {
                        "avg": 10,
                        "day": "2023-11-29",
                        "max": 98,
                        "min": 36
                    },
                    {
                        "avg": 12,
                        "day": "2023-11-30",
                        "max": 49,
                        "min": 3
                    },
                ]
            }
        },
    }
    return mock_data


class MyTest(TestCase):
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class ATest(MyTest):

    def test_data_collection_and_analysis(self):

        test_loc1 = LocationAirQuality(location_id=3900,
                                       particulate_matter_level_current=30, particulate_matter_level_average=50,
                                       times_averaged=10, last_time_collected="2023-12-03T21:00:00-08:00")
        test_loc2 = LocationAirQuality(location_id=59,
                                       particulate_matter_level_current=18, particulate_matter_level_average=30,
                                       times_averaged=5, last_time_collected="2023-12-04T00:00:00-05:00")

        db.session.add(test_loc1)
        db.session.add(test_loc2)
        db.session.commit()

        get_today_aq(mock_aq_forecast())
        get_today_aq(mock_aq_forecast_two())
        loc_one = LocationAirQuality.query.get(3900)
        loc_two = LocationAirQuality.query.get(59)
        loc_three = LocationAirQuality.query.get(12851)

        assert loc_one.times_averaged == 11, f"Expected times averaged of 11, but got {loc_one.times_averaged}"
        assert loc_one.particulate_matter_level_average == 48, \
            f"Expected current average of 48, but got {loc_one.particulate_matter_level_average}"
        assert loc_one.particulate_matter_level_current == 27, \
            f"Expected current particle level of 27, but got {loc_one.particulate_matter_level_current}"
        assert loc_one.last_time_collected.__eq__("2023-12-03T23:00:00-08:00"), \
            f"Expected time of 2023-12-03T23:00:00-08:00, but got {loc_one.last_time_collected}"

        assert loc_two.times_averaged == 5, f"Expected times averaged of 5, but got {loc_two.times_averaged}"
        assert loc_two.particulate_matter_level_average == 30, \
            f"Expected current average of 30, but got {loc_two.particulate_matter_level_average}"
        assert loc_two.particulate_matter_level_current == 18, \
            f"Expected current particle level of 18, but got {loc_two.particulate_matter_level_current}"
        assert loc_two.last_time_collected.__eq__("2023-12-04T00:00:00-05:00"), \
            f"Expected time of 2023-12-04T00:00:00-05:00, but got {loc_two.last_time_collected}"

        assert loc_three.times_averaged == 1, f"Expected times averaged of 1, but got {loc_three.times_averaged}"
        assert loc_three.particulate_matter_level_average == 27, \
            f"Expected current average of 48, but got {loc_three.particulate_matter_level_average}"
        assert loc_three.particulate_matter_level_current == 27, \
            f"Expected current particle level of 27, but got {loc_three.particulate_matter_level_current}"
        assert loc_three.last_time_collected.__eq__("2023-12-03T23:00:00-06:00"), \
            f"Expected time of 2023-12-03T23:00:00-06:00, but got {loc_three.last_time_collected}"


