from exceptions import *
from . import cities

class CityService:


    def __init__(self):
        self.cities = cities

    def search_city(self, city_name: str, limit: int) -> list:
        search_result = []
        counter = 0
        for city_info in self.cities:
            if city_info[1] == city_info[2]:
                search_data = [city_info[1], city_info[3], city_info[4]]
            else:
                search_data = [city_info[1], city_info[2], city_info[3], city_info[4]]
            for field in search_data:
                if field.startswith(city_name, 0, len(city_name)):
                    counter += 1
                    search_result.append(city_info[0:3])
                    if counter == limit:
                        return search_result
        if not search_result:
            raise CityNotFoundError()
        return search_result
