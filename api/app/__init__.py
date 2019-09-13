import json

from flask import Flask, make_response, render_template
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from ...config import config

db = SQLAlchemy()
from .models import user
from ..resources.driver import DriverList, Driver
from ..resources.team import TeamList, Team
from ..resources.user import UserList, User, UserLogin, UserRegister, UserLogout, TokenRefresh


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)

    api.add_resource(DriverList, '/drivers', '/drivers/')
    api.add_resource(Driver, '/drivers/<int:_id>')

    api.add_resource(TeamList, '/teams', '/teams/')
    api.add_resource(Team, '/teams/<int:_id>')

    api.add_resource(UserList, '/users', '/users/')
    api.add_resource(User, '/users/<user>')
    api.add_resource(UserRegister, '/register', '/register/')
    api.add_resource(UserLogin, '/login', '/login/')
    api.add_resource(UserLogout, '/logout', '/logout/')
    api.add_resource(TokenRefresh, '/refresh', '/refresh/')

    @jwt.user_loader_callback_loader
    def user_callback(identity):
        return user.UserModel.find_by_id(identity)

    @api.representation('application/json')
    def output_json(data, code, headers=None):
        resp = make_response(json.dumps(data), code)
        resp.headers.extend(headers or {})
        return resp

    return app
