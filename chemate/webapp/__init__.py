import os

import flask_smorest
from flask import Flask


def create_app() -> Flask:
    from .api import game
    app = Flask('webapp', static_folder='chemate/webapp/static', static_url_path='')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')
    app.config['API_TITLE'] = 'Chemate'
    app.config['API_VERSION'] = '0.0.1'
    app.config['OPENAPI_VERSION'] = '3.0.2'

    restapi = flask_smorest.Api(app)
    restapi.register_blueprint(game.blueprint)
    return app


if __name__ == '__main__':
    create_app().run()
