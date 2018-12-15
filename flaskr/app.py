from flask import Flask
from flask_restful import Api
from flaskr.resources.person import Person,PersonList


app = Flask(__name__)
api = Api(app)

api.add_resource(PersonList, '/person')
api.add_resource(Person,'/person/<string:id>')


if __name__ == '__main__':
     app.run(debug=True,port='5002')