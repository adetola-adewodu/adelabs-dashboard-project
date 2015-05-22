__author__ = 'Adetola'

from flask.ext.restful import reqparse
from flask.ext.restful import marshal_with, marshal
from flask.ext.restful import fields, abort
from flask.ext.restful import Resource
from flask.ext.jsonpify import jsonify

from models import Trip, Schedule

import dateutil.parser
from datetime import datetime



parser = reqparse.RequestParser()
parser.add_argument('page', type=int)
parser.add_argument('perpage', type=int)
parser.add_argument('drivername', type=str)
parser.add_argument('date', type=str)
parser.add_argument('starttime', type=str)
parser.add_argument('endtime', type=str)
parser.add_argument('time', type=str)

HOUR_MINUTE_PATTERN = '%H:%M'

#Fields to marshall data
trip_fields = {
    'id': fields.Integer,
    'drivername': fields.String,
    'type': fields.String,
    'date': fields.DateTime,
    'tripdate': fields.DateTime,
    'triptime': fields.String,
    'datetime': fields.DateTime,
    'tripduration': fields.Integer,
    'dayofweek': fields.String,
    'description': fields.String,
    'trip' : fields.String,
    'gross_fare': fields.Float,
    'commission': fields.Float,
    'total_payment': fields.Float
}

trip_json_fields = {}
trip_json_fields['recordsTotal'] = fields.Integer
trip_json_fields['recordOnPage'] = fields.Integer
trip_json_fields['data'] = fields.Nested(trip_fields)


# Fields to marshall for schedule
schedule_fields = {
    'id': fields.Integer,
    'drivername': fields.String,
    'scheduledate': fields.String,
    'day': fields.Integer,
    'dayofweek': fields.String,
    'position': fields.String,
    'location': fields.String,
    'site': fields.String,
    'starttime':fields.String,
    'endtime':fields.String,
    'unpaidbreak': fields.Integer,
    'totalhours': fields.Integer,
    'hourlyrate': fields.Float,
    'laborcost': fields.Float,
    'notes': fields.String
}

schedule_json_fields = {}
schedule_json_fields['recordsTotal'] = fields.Integer
schedule_json_fields['recordOnPage'] = fields.Integer
schedule_json_fields['data'] = fields.Nested(schedule_fields)


# Trip List Resource
class TripListResource(Resource):
    def create_trip_query(self, parsed_args, query):
        driver_name = parsed_args['drivername']
        if driver_name:
            query = query.filter(Trip.drivername == driver_name)
        if parsed_args['date']:
            date = dateutil.parser.parse(parsed_args['date'])
            print date
            query = query.filter(Trip.tripdate == date)
        if parsed_args['time']:
            time = parsed_args['time']
            print time
            query = query.filter(Trip.time >= time)
        return query

    #@marshal_with(trip_json_fields)
    def get(self):

        trips_data = {}
        query = Trip.query

        parsed_args = parser.parse_args()
        # page = page argument if page arguement exists else use 1
        page = parsed_args['page'] if parsed_args['page'] else 1


        query = self.create_trip_query(parsed_args, query)
        trips_data["recordsTotal"] = query.count()
        per_page = parsed_args['perpage'] if parsed_args['perpage'] else 20
        query = query.paginate(page, per_page,True)
        trips_data["data"] = query.items
        trips_data['recordOnPage'] = len(trips_data["data"])
        return jsonify(marshal(trips_data, trip_json_fields))

class TripResource(Resource):

    def get(self, id):
        trip = Trip.query.filter(Trip.id == id).first()
        if not trip:
            abort(404, message="Trip {} doesn't exist".format(id))
        return jsonify(marshal(trip, trip_fields))


# Schedule List Resource
class ScheduleListResource(Resource):

    def create_schedule_query(self, parsed_args, query):
        driver_name = parsed_args['drivername']
        if driver_name:
            query = query.filter(Schedule.drivername == driver_name)
        if parsed_args['date']:
            date = dateutil.parser.parse(parsed_args['date'])
            query = query.filter(Schedule.scheduledate == date)
        if parsed_args['starttime']:
            start_time = datetime.strptime(parsed_args['starttime'], HOUR_MINUTE_PATTERN).time()
            query = query.filter(Schedule.starttime >= start_time)
        if parsed_args['endtime']:
            end_time = datetime.strptime(parsed_args['endtime'], HOUR_MINUTE_PATTERN).time()
            query = query.filter(Schedule.endtime <= end_time)
        return query


    def get(self):

        schedules_data = {}
        query = Schedule.query

        parsed_args = parser.parse_args()
        # page = page argument if page arguement exists else use 1
        page = parsed_args['page'] if parsed_args['page'] else 1

        query = self.create_schedule_query(parsed_args, query)

        schedules_data["recordsTotal"] = query.count()
        per_page = parsed_args['perpage'] if parsed_args['perpage'] else 20
        query = query.paginate(page, per_page,True)
        schedules_data["data"] = query.items
        schedules_data['recordOnPage'] = len(schedules_data["data"])

        return jsonify(marshal(schedules_data,schedule_json_fields))

class ScheduleResource(Resource):
    @marshal_with(schedule_fields)
    def get(self, id):
        schedule = Schedule.query.filter(Schedule.id == id).first()
        if not schedule:
            abort(404, message="Schedule {} doesn't exist".format(id))
        return schedule