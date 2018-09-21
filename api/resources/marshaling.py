from flask_restful import fields


team_driver_fields = {
    'id': fields.Integer(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'number': fields.Integer(),
    'points': fields.Integer(),
}

team_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'base': fields.String(),
    'chief': fields.String(),
    'car': fields.String(),
    'power_unit': fields.String(),
    'since': fields.String(),
    'championships': fields.Integer(),
    'drivers': fields.List(fields.Nested(team_driver_fields))
}

driver_team_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'base': fields.String(),
    'chief': fields.String(),
    'car': fields.String(),
    'power_unit': fields.String(),
    'since': fields.String(),
    'championships': fields.Integer(),
}
driver_fields = {
    'id': fields.Integer(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'number': fields.Integer(),
    'country': fields.String(),
    'podiums': fields.Integer(attribute='podium'),
    'points': fields.Integer(),
    'championships': fields.Integer(),
    'birthday': fields.DateTime(),
    'team': fields.Nested(driver_team_fields)
}

driver_not_logged_fields = {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'number': fields.Integer(),
}

user_fields = {
    'id': fields.Integer(),
    'username': fields.String(),
    'member_since': fields.DateTime(),
    'is_admin': fields.Boolean()
}