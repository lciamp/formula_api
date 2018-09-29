
from api.app.decorators import db_check_or_return_500

from api.app import db

from datetime import date


class DriverModel(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64), unique=True, index=True)
    number = db.Column(db.Integer, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('TeamModel')
    country = db.Column(db.String(64))
    podium = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    championships = db.Column(db.Integer, default=0)
    birthday = db.Column(db.DateTime)

    def __init__(self, first_name, last_name, number, team_id, country,
                 podium=0,
                 points=0,
                 championships=0,
                 birthday=date(1990, 1, 1)):
        self.first_name = first_name
        self.last_name = last_name
        self.number = number
        self.team_id = team_id
        self.country = country
        self.podium = podium
        self.points = points
        self.championships = championships
        self.birthday = birthday

    def json(self):
        return {
            'id': self.id,
            'name': "{} {}".format(self.first_name, self.last_name),
            'number': self.number,
            'team_id': self.team_id,
            'country': self.country,
            'podiums': self.podium,
            'points': self.points,
            'championships': self.championships,
            'birthday': '{0.month}/{0.day}/{0.year}'.format(self.birthday),
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_number(cls, number):
        return cls.query.filter_by(number=number).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @db_check_or_return_500
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
