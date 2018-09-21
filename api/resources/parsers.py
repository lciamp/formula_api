from flask_restful import reqparse


_driver_parser = reqparse.RequestParser()
_driver_parser.add_argument('first_name',
                            required=True,
                            location='json',
                            help="first name field can not be left blank."
                            )
_driver_parser.add_argument('last_name',
                            type=str,
                            location='json',
                            required=True,
                            help="last_name field can not be left blank."
                            )
_driver_parser.add_argument('country',
                            type=str,
                            location='json',
                            required=False,
                            help="country field can not be left blank."
                            )
_driver_parser.add_argument('number',
                            type=int,
                            location='json',
                            required=True,
                            help="number field can not be left blank."
                            )
_driver_parser.add_argument('team_id',
                            type=int,
                            location='json',
                            required=True,
                            help="team_id field can not be left blank."
                            )


_team_parser = reqparse.RequestParser()
_team_parser.add_argument('name',
                          type=str,
                          required=True,
                          location='json',
                          help="name field can not be left blank."
                          )
_team_parser.add_argument('base',
                          type=str,
                          required=True,
                          location='json',
                          help="base field can not be left blank."
                          )
_team_parser.add_argument('car',
                          type=str,
                          required=True,
                          location='json',
                          help="car field can not be left blank."
                          )
_team_parser.add_argument('power_unit',
                          type=str,
                          required=True,
                          location='json',
                          help="power_unit field can not be left blank."
                          )

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          location='json',
                          help="Username can not be blank"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          location='json',
                          help="Password can not be blank"
                          )
_user_parser.add_argument('is_admin',
                          type=bool,
                          required=False,
                          location='json',
                          help="is_admin can not be blank"
                          )