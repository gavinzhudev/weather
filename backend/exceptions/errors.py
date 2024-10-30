from werkzeug.exceptions import *

def handle_bad_request(error):
    return {
        'message': 'Invalid request parameters',
        'errors': error.description,
        'status_code': 400,
    }, 400


def handle_unauthorized(error):
    return {
        'message': 'Unauthorized access',
        'errors': error.description,
        'status_code': 401
    }, 401


def handle_forbidden(error):
    return {
        'message': 'Access forbidden',
        'errors': error.description,
        'status_code': 403
    }, 403


def handle_not_found(error):
    return {
        'message': 'Resource not found',
        'errors': error.description,
        'status_code': 404
    }, 404


def handle_method_not_allowed(error):
    return {
        'message': 'Method not allowed',
        'errors': error.description,
        'status_code': 405
    }, 405


def handle_server_error(error):
    return {
        'message': 'Internal server error',
        'errors': error.description,
        'status_code': 500
    }, 500


def handle_bad_gateway(error):
    return {
        'message': 'Bad gateway',
        'errors': error.description,
        'status_code': 502
    }, 502


def handle_service_unavailable(error):
    return {
        'message': 'Service unavailable',
        'errors': error.description,
        'status_code': 503
    }, 503


def http_error_handlers(app):
    app.errorhandler(BadRequest)(handle_bad_request)
    app.errorhandler(Unauthorized)(handle_unauthorized)
    app.errorhandler(Forbidden)(handle_forbidden)
    app.errorhandler(NotFound)(handle_not_found)
    app.errorhandler(MethodNotAllowed)(handle_method_not_allowed)
    app.errorhandler(InternalServerError)(handle_server_error)
    app.errorhandler(BadGateway)(handle_bad_gateway)
    app.errorhandler(ServiceUnavailable)(handle_service_unavailable)
