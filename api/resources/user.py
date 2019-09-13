from flask_restful import Resource, marshal_with
from werkzeug.security import safe_str_cmp
from ..blacklist import BLACKLIST
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from ..app.models.user import UserModel
from .parsers import _user_parser
from .marshaling import user_fields


class UserList(Resource):
    @marshal_with(user_fields, envelope='users')
    def get(self):
        return UserModel.find_all(), 200


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': "User '{}' created successfully.".format(user.username)}, 201


class User(Resource):
    @classmethod
    @marshal_with(user_fields)
    def get(cls, user):
        if user.isdigit():
            user = UserModel.find_by_id(user)
        else:
            user = UserModel.find_by_name(user)
        return user

    @classmethod
    def delete(cls, user):
        if user.isdigit():
            user = UserModel.find_by_id(user)
        else:
            user = UserModel.find_by_name(user)
        if not user:
            return {'message': 'User not found.'}, 404
        user.delete_from_db()
        return {'message': "User '{}' deleted".format(user.username)}, 202


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid Credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # jti is JWT Token ID
        BLACKLIST.add(jti)
        return {'message': 'Logged out successfully.'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(current_user, fresh=False)
        return {'access_token': new_token}, 200
