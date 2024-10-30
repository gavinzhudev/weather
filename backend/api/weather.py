from flask import abort, jsonify
from flask_restx import Resource, reqparse
from . import api, weather_model, error_decorators
from exceptions import *



parser = reqparse.RequestParser()
parser.add_argument('city', type=str, required=True)


@api.route('/weather')
class Weather(Resource):
    @api.expect(parser)
    @api.response(200, 'Success', weather_model)
    @error_decorators
    def get(self):
        try:
            from service import WeatherService
            weather_service = WeatherService()
            args = parser.parse_args()
            city = args['city']
            weather = weather_service.get_forecasts(city)
            return jsonify({"status_code": 200, "data": weather, "message": "success"})
        except BadRequest as e:
            abort(400, {"err_msg": str(e)})
        except ServiceException as e:
            abort(e.status, e.errors)
        except Exception as e:
            api.logger.error(f"Unexpected error: {str(e)}")
            abort(500, {"err_msg": "Internal Server Error"})
