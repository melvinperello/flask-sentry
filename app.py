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
api.add_resource(PersonListResource, '/api/person') # GET (ALL) POST
api.add_resource(PersonResource,'/api/person/<int:id>') # GET PUT DELETE

# /record resources
from resources import RecordPersonResource,RecordResource
api.add_resource(RecordPersonResource, '/api/record/person/<int:person_id>') # GET (ALL) POST (Time In)
api.add_resource(RecordResource,'/api/record/<int:id>') # GET PUT (Time Out) DELETE (Cancel)

@app.after_request
def after_request(response):
    response.headers['SENTRY_NODE'] = 'sg-node-dev'
    return response