from flask import Flask
from flask_restful import Api
from flaskr.resources.person import PersonResource,PersonListResource
from flaskr.resources.record import Record,RecordList


app = Flask(__name__)
api = Api(app)

api.add_resource(PersonListResource, '/person')
api.add_resource(PersonResource,'/person/<string:id>')
api.add_resource(RecordList, '/record')
api.add_resource(Record,'/record/<int:id>')


if __name__ == '__main__':
     app.run(debug=True,port='80')