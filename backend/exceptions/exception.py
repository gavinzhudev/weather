class ServiceException(Exception):
    code = -1
    msg = "Service Error"
    status = -1

    def __init__(self, *, code=None, msg=None, status=None):
        self.code = code if code is not None else self.code
        self.msg = msg if msg is not None else self.msg
        self.status = status if status is not None else self.status

    @property
    def errors(self):
        return {
            "err_code": self.code,
            "err_meg": self.msg
        }


class WeatherServiceException(ServiceException):
    code = 6100
    msg = "Weather Service Error"
    status = 500


class CityServiceException(ServiceException):
    code = 6200
    msg = "City Service Error"
    status = 500


def create_weather_exception(*, name, msg, code, status):
    return type(
        name,
        (WeatherServiceException,),
        {
            "msg": msg,
            "code": code,
            "status": status
        }
    )


def create_city_exception(*, name, msg, code, status):
    return type(
        name,
        (CityServiceException,),
        {
            "msg": msg,
            "code": code,
            "status": status
        }
    )


WeatherInternalServerError = create_weather_exception(
    name="WeatherInternalServerError",
    msg="WaterSerivce Internal Server Error",
    code=6101,
    status=500
)

WeatherNotFoundError = create_weather_exception(
    name="WeatherNotFound ",
    msg="Weather Res Not Found ",
    code=6102,
    status=404
)

WeatherServiceUnavailable = create_weather_exception(
    name="WeatherServiceUnavailable",
    msg="Weather Service Unavailable",
    code=6103,
    status=503
)

WeatherParamError = create_weather_exception(
    name="WeatherParamError ",
    msg="Weather Param Error",
    code=6104,
    status=400
)

CityInternalServerError = create_city_exception(
    name="CityInternalServerError",
    msg="CitySerivce Internal Server Error",
    code=6201,
    status=500
)

CityNotFoundError = create_city_exception(
    name="CityNotFound ",
    msg="City Res Not Found ",
    code=6202,
    status=404
)

CityServiceUnavailable = create_city_exception(
    name="City ServiceUnavailable",
    msg="City Service Unavailable",
    code=6203,
    status=503
)

CityParamError = create_city_exception(
    name="CityParamError ",
    msg="City Param Error",
    code=6204,
    status=400
)
