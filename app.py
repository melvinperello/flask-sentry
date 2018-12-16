from flask import Flask
from flask_restful import Api

from resources import PersonListResource
from resources import PersonResource
from resources import RecordListResource
from resources import RecordPersonResource
from resources import RecordResource


app = Flask(__name__)
api = Api(app)

api.add_resource(PersonListResource, '/api/person')
api.add_resource(PersonResource,'/api/person/<int:id>')
#
api.add_resource(RecordPersonResource, '/api/record/person/<int:person_id>')
api.add_resource(RecordListResource, '/api/record')
api.add_resource(RecordResource,'/api/record/<int:id>')


#if __name__ == '__main__':
#     app.run(debug=True,port='80')