from flask import jsonify
from flask_restx import Resource, reqparse, abort
from . import api, city_model, error_decorators
from exceptions import *
from service import CityService

city_service = CityService()

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)


@api.route('/city')
class City(Resource):
    @api.expect(parser)
    @api.response(200, 'Success', city_model)
    @error_decorators
    def get(self):
        try:
            args = parser.parse_args()
            name = args['name']
            data = city_service.search_city(name, 20)
            return jsonify({"code": 200, "data": data, "message": "success"})
        except BadRequest as e:
            abort(400, {'err_msg': str(e)})
        except ServiceException as e:
            abort(e.status, e.errors)
        except Exception as e:
            api.logger.error(f"Unexpected error: {str(e)}")
            abort(500, {"err_msg": str(e)})
