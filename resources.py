from flask_restful import Resource
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from db import session



from models import PersonRepository

parser = reqparse.RequestParser()
parser.add_argument('nameLast', type=str,required=True,help='Last Name is required')
parser.add_argument('nameFirst', type=str,required=True,help='First Name is required')
parser.add_argument('nameMiddle', type=str)
parser.add_argument('nameExt', type=str)

personFields = {
    'id': fields.Integer,
    'nameLast': fields.String,
    'nameFirst': fields.String,
    'nameMiddle': fields.String,
    'nameExt' : fields.String,
}


class PersonListResource(Resource):

    @marshal_with(personFields)
    def get(self):
        personList = session.query(PersonRepository).all()
        return personList

    @marshal_with(personFields)
    def post(self):
        parsed_args = parser.parse_args()

        person = PersonRepository()
        person.nameLast = parsed_args['nameLast']
        person.nameFirst = parsed_args['nameFirst']
        person.nameMiddle = parsed_args['nameMiddle']
        person.nameExt = parsed_args['nameExt']


        session.add(person)
        session.commit()
        return {},201


class PersonResource(Resource):

    @marshal_with(personFields)
    def get(self,id):
        person = session.query(PersonRepository).filter(PersonRepository.id == id).first()
        if not person:
            abort(404, message="Person {} doesn't exist".format(id))
        return person

    def put(self,id):
        # update
        pass

    def delete(self,id):
        # delete
        pass

class PersonRecordList(Resource):

    def get(self,person_id):
        # get all records of a person
        pass

    def post(self,person_id):
        # add new record for a person.
        pass


class RecordList(Resource):
    def get(self):
        pass

class Record(Resource):

    def get(self,id):
        pass

    def put(self,id):
        pass

    def delete(self,id):

        pass