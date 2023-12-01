import pytest
from src.analyze_data import threshold_less_than_aq_of_day
from src.collect_data import get_forecast, get_today_aq


def mock_aq_forecast():
    mock_data = {
        "aqi": 27,
        "idx": 999999,
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
            "iso": "2023-11-30T21:00:00-08:00"
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


def test_forecast_parse():
    fake_response = mock_aq_forecast()
    result = get_forecast(fake_response)
    assert result['one_day'] == 100, f"Expected day one forecast of 100, but got {result['one_day']}"
    assert result['two_day'] == 31, f"Expected day one forecast of 31, but got {result['two_day']}"
    assert result['three_day'] == 15, f"Expected day one forecast of 15, but got {result['three_day']}"


def test_today_aq_parse():
    fake_response = mock_aq_forecast()
    result = get_today_aq(fake_response, True)
    assert result['aqi'] == 27, f"Expected aqi of 27, but got {result['aqi']}"
    assert result['idx'] == 999999, f"Expected idx: 999999, but got {result['idx']}"
    assert result['city'] == 'Mock City', f"Expected location: Mock City, but got {result['city']}"


def test_threshold_comparison():
    fake_response = mock_aq_forecast()
    result = get_today_aq(fake_response, True)
    result_less = threshold_less_than_aq_of_day(24, result["aqi"])
    result_more = threshold_less_than_aq_of_day(30, result["aqi"])
    assert result_less, f"Expected value of 1 for correct, but got {result_less}"
    assert not result_more, f"Expected value of 0 for false, but got {result_more}"
