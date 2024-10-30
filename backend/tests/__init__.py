import os


current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
os.chdir(parent_directory)
from service import CityService,WeatherService

city_service = CityService()
weather_service = WeatherService()