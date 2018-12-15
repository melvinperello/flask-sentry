from flask_restful import Resource
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from db import session
from models import PersonRepository

from flask import request



#-------------------------------------------------------------------------------
# /person
#-------------------------------------------------------------------------------
personParser = reqparse.RequestParser()
personParser.add_argument('nameLast', type=str,required=True,help='Last Name is required')
personParser.add_argument('nameFirst', type=str,required=True,help='First Name is required')
personParser.add_argument('nameMiddle', type=str)
personParser.add_argument('nameExt', type=str)
personParser.add_argument('contactTel', type=str)
personParser.add_argument('contactMobile', type=str)
personParser.add_argument('contactEmail', type=str)

personFields = {
    'id': fields.Integer,
    'nameLast': fields.String,
    'nameFirst': fields.String,
    'nameMiddle': fields.String,
    'nameExt' : fields.String,
    'contactTel' : fields.String,
    'contactMobile' : fields.String,
    'contactEmail' : fields.String,
    'updatedAt' : fields.Integer,
    'updatedBy' : fields.String,
}
class PersonListResource(Resource):

    @marshal_with(personFields)
    def get(self):
        personList = session.query(PersonRepository).filter(PersonRepository.deletedAt == 0).all()
        if not personList:
            abort(404, message="List is empty")
        return personList

    @marshal_with(personFields)
    def post(self):
        parsed_args = personParser.parse_args()

        person = PersonRepository()
        person.nameLast = parsed_args['nameLast']
        person.nameFirst = parsed_args['nameFirst']
        person.nameMiddle = parsed_args['nameMiddle']
        person.nameExt = parsed_args['nameExt']
        person.contactTel = parsed_args['contactTel']
        person.contactMobile = parsed_args['contactMobile']
        person.contactEmail = parsed_args['contactEmail']

        session.add(person)
        session.commit()
        return person,201


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



#-------------------------------------------------------------------------------
# /record
#-------------------------------------------------------------------------------
recordParser = reqparse.RequestParser()
recordParser.add_argument('nameLast', type=str,required=True,help='Last Name is required')

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