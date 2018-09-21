from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from api.app.models.team import TeamModel
from .marshaling import team_fields


class TeamList(Resource):
    @marshal_with(team_fields, envelope='teams')
    def get(self):
        return TeamModel.find_all(), 200


class Team(Resource):
    @marshal_with(team_fields)
    def get(self, id):
        team = TeamModel.find_by_id(id)
        if team:
            return team, 200
        return {'message': "TeamId '{}' not found".format(id)}, 404

    @jwt_required
    def post(self, id):
        # TODO parser for team post
        if TeamModel.find_by_id(id):
            return {'message': "An store with name '{}' already exists".format(id)}, 400
        store = TeamModel(id)
        store.save_to_db()
        return store.json(), 201

    @jwt_required
    def delete(self, id):
        team = TeamModel.find_by_id(id)
        if team:
            team.delete_from_db()
        return {'message': "Team '{}' deleted.".format(id)}, 202
