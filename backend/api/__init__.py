from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)

from exceptions import http_error_handlers

http_error_handlers(api)

from flask_restx import fields

city_model = api.model('City', {
    "status_code": fields.Integer(description='HTTP Status Code', required=True, example=200),
    "data": fields.List(fields.List(fields.String), description='位置数据列表', required=True),
    "message": fields.String(description='Status description', required=True, example='success')
})

weather_model = api.model('City', {
    "status_code": fields.Integer(description='HTTP Status Code', required=True, example=200),
    "data": fields.List(fields.List(fields.String), description='', required=True),
    "message": fields.String(description='Status description', required=True, example='success')
})

error_fields = api.model('ErrorFields', {
    'err_msg': fields.String(required=True, description='error reason'),
    'err_code': fields.Integer(required=False, description='error code')
})

error_model = api.model('ErrorModel', {
    'status_code': fields.Integer(description='HTTP Status Code', required=True, example=400),
    'errors': fields.Nested(error_fields, description='Detailed error information'),
    'message': fields.String(description='Status description', required=True, example='error')
})

def error_decorators(func):
    decorators = [
        api.response(400, 'Invalid request parameters', error_model),
        api.response(404, 'Resource not found', error_model),
        api.response(500, 'Internal server error', error_model),
        api.response(502, 'Bad gateway', error_model),
        api.response(503, 'Service unavailable', error_model)
    ]
    for decorator in reversed(decorators):
        func = decorator(func)
    return func

from .weather import *
from .city import *
