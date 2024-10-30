from datetime import datetime

import pytest
import requests

from exceptions import *
from . import *


def test_local_adcode():
    adcode = weather_service.get_local_adcode("广州市")
    assert adcode == "440100"
    adcode = weather_service.get_local_adcode("不存在")
    assert adcode == ""


def test_remote_adcode():
    adcode = weather_service.get_remote_adcode("盖州市")
    assert adcode == "210881"
    adcode = weather_service.get_local_adcode("不存在")
    assert adcode == ""


def test_forecasts():
    forecasts = weather_service.get_forecasts("广州市")
    assert type(forecasts) == dict
    assert len(forecasts["casts"]) == 4
    assert forecasts["casts"][0]["date"] == datetime.now().date().strftime("%Y-%m-%d")
    with pytest.raises(WeatherNotFoundError) as e:
        weather_service.get_forecasts("不存在的城市")
    assert e.value.status == 404


