# driver - first_name, last_name number, team_id, country, podium, points, championships, birthday):
from datetime import date
#from app1 import db
from app.models import DriverModel
from app.models.team import TeamModel

DRIVERS = [
    ('Lewis', 'Hamilton', 44, 1, 'United Kingdom', 128, 2866, 4, date(1985, 1, 7)),
    ('Valtteri', 'Bottas', 77, 1, 'Finland', 28, 875, 0, date(1989, 8, 28)),

    ('Sebastian', 'Vettel', 5, 2, 'Germany', 107, 2651, 4, date(1987, 7, 3)),
    ('Kimi', 'Räikkönen', 7, 2, 'Finland', 100, 1729, 1, date(1979, 10, 17)),


    ('Daniel', 'Ricciardo', 3, 3, 'Australia', 29, 934, 0, date(1989, 1, 7)),
    ('Max', 'Verstappen', 33, 3, 'Netherlands', 16, 551, 0, date(1997, 9, 30)),

    ('Nico', 'Hulkenberg', 27, 4, 'Germany', 0, 457, 0, date(1987, 8, 19)),
    ('Carlos', 'Sainz', 55, 4, 'Spain', 0, 152, 0, date(1994, 9, 1)),

    ('Romain', 'Grosjean', 8, 5, 'Germany', 10, 371, 0, date(1986, 4, 17)),
    ('Kevin', 'Magnussen', 20, 5, 'Denmark', 1, 130, 0, date(1992, 10, 5)),

    ('Fernando', 'Alonso', 14, 6, 'Spain', 97, 1893, 2, date(1981, 7, 29)),
    ('Stoffel', 'Vandoorne', 2, 6, 'Belgium', 0, 22, 0, date(1992, 3, 26)),

    ('Sergio', 'Perez', 11, 7, 'Mexico', 8, 513, 0, date(1990, 1, 26)),
    ('Esteban', 'Ocon', 31, 7, 'France', 0, 132, 0, date(1996, 9, 17)),

    ('Pierre', 'Gasly', 10, 8, 'France', 0, 28, 0, date(1996, 2, 7)),
    ('Brendon', 'Hartley', 28, 8, 'New Zealand', 0, 2, 0, date(1989, 11, 10)),

    ('Marcus', 'Ericsson', 9, 9, 'Sweden', 0, 15, 0, date(1990, 9, 2)),
    ('Charles', 'Leclerc', 16, 9, 'Monaco', 0, 13, 0, date(1997, 10, 16)),

    ('Lance', 'Stroll', 18, 10, 'Canada', 1, 46, 0, date(1998, 10, 29)),
    ('Sergey', 'Sirotkin', 35, 10, 'Russian Federation', 0, 1, 0, date(1995, 8, 25)),
]

# team - name, base, chief, car, power_unit, since, championships

TEAMS = [
    ('Mercedes AMG Petronas Motorsport', 'Brackley, United Kingdom', 'Toto Wolff', 'W09', 'Mercedes', 1970, 4),
    ('Scuderia Ferrari', 'Maranello, Italy', 'Maurizio Arrivabene', 'SF71H', 'Ferrari', 1950, 16),
    ('Aston Martin Red Bull Racing', 'Milton Keynes, United Kingdom', 'Christian Horner', 'RB14', 'TAG Heuer', 1997, 4),
    ('Renault Sport Formula One Team', 'Enstone, United Kingdom', 'Cyril Abiteboul', 'R.S.18', 'Renault', 1986, 2),
    ('Haas F1 Team', 'Kannapolis, United States', 'Guenther Steiner', 'VF-18', 'Ferrari', 2016, 0),
    ('McLaren F1 Team', 'Woking, United Kingdom', 'Zak Brown', 'MCL33', 'Renault', 1966, 8),
    ('Racing Point Force India F1 Team', 'Silverstone, United Kingdom', 'Otmar Szafnauer', 'VJM11', 'Mercedes', 2018, 0),
    ('Red Bull Toro Rosso Honda', 'Faenza, Italy', 'Franz Tost', 'STR13', 'Honda', 1985, 0),
    ('Alfa Romeo Sauber F1 Team', 'Hinwil, Switzerland', 'Frédéric Vasseur', 'C37', 'Ferrari', 1993, 0),
    ('Williams Martini Racing', 'Grove, United Kingdom', 'Frank Williams', 'FW41', 'Mercedes', 1978, 9),
]


def add_teams():
    for team in TEAMS:
        t = TeamModel(*team)
        t.save_to_db()
    print('teams added to db.')


def add_drivers():
    for driver in DRIVERS:
        d = DriverModel(*driver)
        d.save_to_db()
    print('drivers added to db')
