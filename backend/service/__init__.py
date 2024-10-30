import json
from exceptions import CityInternalServerError


def load_local_city_data():
    cityinfo = None

    def parse_data(path: str):
        try:
            nonlocal cityinfo
            if cityinfo is None:
                with open(path, 'r') as file:
                    cityinfo = json.load(file)
                    return cityinfo
        except Exception:
            raise CityInternalServerError()

    return parse_data


load_local_data = load_local_city_data()
cities = load_local_data('./cities.json')
from .city import CityService
from .weather import WeatherService

_all__ = (
    'CityService',
    'WeatherService',
)
