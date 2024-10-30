from typing import Dict, Any

import requests
import os
from dotenv import load_dotenv
from . import cities
from exceptions import WeatherInternalServerError, WeatherNotFoundError, WeatherServiceUnavailable
from utils import CacheDict
from datetime import timedelta
from exceptions.exception import WeatherServiceException

load_dotenv(".env.secret")
load_dotenv(".env.share")



class WeatherService:
    adcode_cache = CacheDict(timedelta(days=30))
    forecasts_cache = CacheDict(timedelta(minutes=30))

    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.adcode_api = os.environ.get('ADCODE_API')
        self.weather_api = os.environ.get('WEATHER_API')
        self.adcode_index = {}
        for city_info in cities:
            if city_info[2].find("区") == -1:
                self.adcode_index[city_info[2]] = city_info[-1]

    def get_remote_adcode(self, city: str) -> str:
        adcode = WeatherService.adcode_cache.get(city)
        if adcode:
            return adcode
        try:
            response = requests.get(self.adcode_api, params={
                "keywords": city,
                "subdistrict": 0,
                "key": self.api_key,
            })
            response.raise_for_status()
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                raise ValueError("Invalid JSON response")
            if "districts" not in data:
                raise KeyError("Invalid response structure")
            adcodeinfo = data.get("districts")
            if not adcodeinfo:
                raise KeyError("Adcode not found")
            adcode = adcodeinfo[0].get("adcode")
            if not adcode:
                raise KeyError("Adcode not found")
            WeatherService.adcode_cache.set(city, adcode)
            return adcode
        except requests.RequestException:
            raise WeatherServiceUnavailable()
        except (ValueError, KeyError, IndexError) as e:
            raise WeatherNotFoundError(msg=str(e))
        except Exception as e:
            raise WeatherServiceException(msg=str(e))

    def get_local_adcode(self, city_name: str) -> str:
        adcode = self.adcode_index.get(city_name)
        return adcode if adcode else ""

    def get_forecasts(self, city: str) -> Dict[str, Any]:
        adcode = self.get_local_adcode(city)
        if not adcode:
            adcode = self.get_remote_adcode(city)
        forecasts = WeatherService.forecasts_cache.get(city)
        if forecasts:
            return forecasts
        try:
            response = requests.get(self.weather_api, params={
                "city": adcode,
                "extensions": "all",
                "key": self.api_key,
            })
            response.raise_for_status()
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                raise ValueError("Invalid JSON response")
            if "forecasts" not in data:
                raise KeyError("Invalid response structure")
            forecasts = data["forecasts"][0]
            WeatherService.forecasts_cache.set(city, forecasts)
            return forecasts
        except requests.RequestException as e:
            raise WeatherServiceUnavailable(msg=str(e))
        except (ValueError, KeyError, IndexError) as e:
            raise WeatherServiceException(msg=f"Failed to parse weather data: {str(e)}")
        except Exception as e:
            raise WeatherServiceException(msg=str(e))
