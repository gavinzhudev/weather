import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS
from exceptions import http_error_handlers
from api import api_blueprint

def create_app():
    weather_app = Flask(__name__)
    return weather_app


def set_logger(app):
    app.logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

def register_blueprint(app):
    app.register_blueprint(api_blueprint)

application = create_app()
set_logger(application)
register_blueprint(application)
http_error_handlers(application)
CORS(application, supports_credentials=True)

if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=True, port=5000)
