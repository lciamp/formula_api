from datetime import datetime
from api.app import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    is_admin = db.Column(db.Boolean(), default=False)

    def __init__(self, username, password, is_admin):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def json(self):
        return {
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
