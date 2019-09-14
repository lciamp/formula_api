from flask_restful import Resource, marshal, marshal_with
from flask_restful import Resource, marshal
from flask_jwt_extended import jwt_required
from api.app.models.team import TeamModel
from .parsers import _team_parser
from .marshaling import team_fields


class TeamList(Resource):
    @marshal_with(team_fields, envelope='teams')
    def get(self):
        return TeamModel.find_all(), 200


class Team(Resource):
    def get(self, _id):
        team = TeamModel.find_by_id(_id)
        if team:
            return marshal(team, team_fields), 200
        return {'message': "TeamId:{} not found".format(_id)}, 404

    @jwt_required
    def post(self, _id):
        data = _team_parser.parse_args()
        if TeamModel.find_by_id(_id):
            return {'message': "Team with id:{} already exists".format(_id)}, 400
        team = TeamModel(**data)
        team.save_to_db()
        return team.json(), 201

    @jwt_required
    def delete(self, _id):
        team = TeamModel.find_by_id(_id)
        if team:
            team.delete_from_db()
        return {'message': "Team id:{} deleted.".format(_id)}, 202
