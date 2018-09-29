import json

from flask import Flask, make_response
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import config
db = SQLAlchemy()
from api.resources.driver import DriverList, Driver
from api.resources.team import TeamList, Team
from api.resources.user import UserList, User, UserLogin, UserRegister, UserLogout, TokenRefresh


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)

    api.add_resource(DriverList, '/drivers', '/drivers/')
    api.add_resource(Driver, '/drivers/<int:id>')

    api.add_resource(TeamList, '/teams', '/teams/')
    api.add_resource(Team, '/teams/<int:id>')

    api.add_resource(UserList, '/users', '/users/')
    api.add_resource(User, '/users/<user>')
    api.add_resource(UserRegister, '/register', '/register/')
    api.add_resource(UserLogin, '/login', '/login/')
    api.add_resource(UserLogout, '/logout', '/logout/')
    api.add_resource(TokenRefresh, '/refresh', '/refresh/')

    @api.representation('application/json')
    def output_json(data, code, headers=None):
        resp = make_response(json.dumps(data), code)
        resp.headers.extend(headers or {})
        return resp

    return app