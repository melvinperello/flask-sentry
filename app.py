# Create Flask Application
from flask import Flask
app = Flask(__name__)

# Create Database Instance
from flask_sqlalchemy import SQLAlchemy
app.config.from_pyfile('sentry.cfg')
db = SQLAlchemy(app)

# Create API's Endpoint
from flask_restful import Api
api = Api(app)

# /person resources
from resources import PersonListResource,PersonResource
api.add_resource(PersonListResource, '/api/person')
api.add_resource(PersonResource,'/api/person/<int:id>')

# /record resources
from resources import RecordListResource,RecordPersonResource,RecordResource
api.add_resource(RecordPersonResource, '/api/record/person/<int:person_id>')
api.add_resource(RecordListResource, '/api/record')
api.add_resource(RecordResource,'/api/record/<int:id>')