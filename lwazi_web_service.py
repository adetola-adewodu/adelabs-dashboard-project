from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

import os


if os.environ.has_key("DATABASE_URL"):
    POSTGRES_URI = os.environ["DATABASE_URL"]
else:
    from config import database_settings
    settings = database_settings["heroku"]
    POSTGRES_URI = "postgresql+psycopg2://" + settings["USERNAME"] +":"+ settings["PASSWORD"] + "@" + settings["URL"] +"/"+ settings["DATABASE"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
db = SQLAlchemy(app) # Creates connection with sqlalchemy database uri
api = Api(app)

@app.after_request
def before_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

from resources import TripListResource,TripResource
from resources import ScheduleResource,ScheduleListResource

# Trip Resources
api.add_resource(TripListResource, '/trips', endpoint='trips')
api.add_resource(TripResource, '/trips/<string:id>', endpoint='trip')

# Schedule Resources
api.add_resource(ScheduleListResource, '/schedules', endpoint='schedules')
api.add_resource(ScheduleResource, '/schedules/<string:id>', endpoint='schedule')