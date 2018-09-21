from flask_restful import Resource, marshal
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)

from api.app.models import DriverModel
from .marshaling import driver_not_logged_fields, driver_fields
from .parsers import _driver_parser


class DriverList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        drivers = [d.json() for d in DriverModel.find_all()]
        if user_id:
            return marshal(DriverModel.find_all(), driver_fields, envelope='drivers'), 200
        resp = marshal(DriverModel.find_all(), driver_not_logged_fields, envelope='drivers')
        resp['message'] = 'More information if logged in.'
        return resp, 200

    @fresh_jwt_required
    def post(self):
        data = _driver_parser.parse_args()
        if DriverModel.find_by_number(data['number']):
            return {'message': "A driver with number '{}' already exists".format(data['number'])}, 400

        driver = DriverModel(**data)

        driver.save_to_db()

        return driver.json(), 201


#    return marshal(db_get_todo(), resource_fields), 200
class Driver(Resource):
    @jwt_optional
    def get(self, id):
        user_id = get_jwt_identity()
        driver = DriverModel.find_by_id(id)
        if driver:
            if user_id:
                return marshal(driver, driver_fields), 200
            resp = marshal(driver, driver_not_logged_fields)
            resp['message'] = 'more information if logged in.'
            return resp, 200
        return {'message': "DriverId '{}' not found".format(id)}, 404

    @jwt_required
    def put(self, id):
        data = _driver_parser.parse_args()
        driver = DriverModel.find_by_id(id)

        if driver:
            driver.first_name = data['first_name']
            driver.last_name = data['last_name']
            driver.number = data['number']
            driver.team_id = data['team_id']
            driver.country = data['country']
        else:
            driver = DriverModel(**data)

        driver.save_to_db()

        return marshal(driver, driver_fields), 202

    @fresh_jwt_required
    def delete(self, id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
        driver = DriverModel.find_by_id(id)
        if driver:
            driver.delete_from_db()

        return {'message': "DriverId '{}' deleted.".format(id)}, 202
