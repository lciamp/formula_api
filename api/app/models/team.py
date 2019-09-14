from api.app import db


class TeamModel(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    base = db.Column(db.String(64))
    chief = db.Column(db.String(64))
    car = db.Column(db.String(64))
    power_unit = db.Column(db.String(64))
    since = db.Column(db.Integer)
    championships = db.Column(db.Integer, default=0)
    drivers = db.relationship('DriverModel', lazy='dynamic')

    def __init__(self, name, base, chief, car, power_unit, since=0, championships=0):
        self.name = name
        self.base = base
        self.chief = chief
        self.car = car
        self.power_unit = power_unit
        self.since = since
        self.championships = championships

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'base': self.base,
            'chief': self.chief,
            'car': self.car,
            'power_unit': self.power_unit,
            'founded': self.since,
            'championships': self.championships,
            'drivers': [d.json() for d in self.drivers.all()],
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()





